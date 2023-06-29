import datetime
import json
import uuid

from flask import request, current_app, g
from flask_redis import FlaskRedis

from models import BaseModel, db

redis_client = FlaskRedis()


class AbstractTokenStrategy:
    """
    token存储策略抽象类
    """
    # token 过期时间- 单位是s  # 2小时
    TOKEN_EXPIRE_TIMEOUT = 60 * 60 * 2
    # token-key
    TOKEN_KEY = "token"
    # token 前辍
    TOKEN_KEY_PREFIX = "flaskapp:"
    # 超级管理员id
    SUPER_ADMIN_ID = 1

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
        else:
            self.init_app(current_app)

    def init_app(self, app):
        if app.config.get('TOKEN_EXPIRE_TIMEOUT'):
            self.TOKEN_EXPIRE_TIMEOUT = app.config.get('TOKEN_EXPIRE_TIMEOUT')
        if app.config.get('TOKEN_KEY'):
            self.TOKEN_KEY = app.config.get('TOKEN_KEY')
        if app.config.get('TOKEN_KEY_PREFIX'):
            self.TOKEN_KEY_PREFIX = app.config.get('TOKEN_KEY_PREFIX')
        if app.config.get('SUPER_ADMIN_ID'):
            self.SUPER_ADMIN_ID = app.config.get('SUPER_ADMIN_ID')

    def __new__(cls, *args, **kwargs):
        """
        设置成单例模式
        :param args:
        :param kwargs:
        """
        if not hasattr(cls, '_instance'):
            orig = super(AbstractTokenStrategy, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def set(self, data):
        """
        存储token
        :param data:
        :return:
        """
        pass

    def get(self, token):
        """
        获取token
        :param token:
        :return:
        """
        pass

    def remove(self, token):
        """
        删除token
        :param token:
        :return:
        """
        pass


class TokenStrategyFactory:

    @staticmethod
    def get_instance():
        token_strategy = current_app.config.get("TOKEN_STRATEGY", "cache")
        if token_strategy == 'redis':
            return RedisTokenStrategy()
        elif token_strategy == 'mysql':
            return MysqlTokenStrategy()
        else:
            return CacheTokenStrategy()

    @staticmethod
    def create_token(data=None):
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        return suid

    """
    校验token是否存在
    """

    @staticmethod
    def check_token(access=None):
        """
        核实token-如果权限标识存在，则校验是否存在权限标识
        :param access: 权限标识
        :return:
        """
        token_strategy = TokenStrategyFactory.get_instance()
        token = request.headers.get(token_strategy.TOKEN_KEY, "")
        data = token_strategy.get(token)
        if data is not None:
            # 将当前用户信息注入到这一次请求中，方便全局使用
            g.current_user = data
            if data.get("userId") is not token_strategy.SUPER_ADMIN_ID and access is not None:
                return access in data.get("perms", "").split(",")
            return True
        else:
            return False



class CacheTokenStrategy(AbstractTokenStrategy):
    """
    缓存Token存储策略
    """
    from cacheout import LFUCache  # 最小频率使用机制
    cache = LFUCache(maxsize=1000)

    def set(self, data):
        token = data.get("token", TokenStrategyFactory.create_token(data))
        data['token'] = token
        self.cache.set(token, json.dumps(data, ensure_ascii=False), ttl=self.TOKEN_EXPIRE_TIMEOUT)
        return data

    def get(self, token):
        data = self.cache.get(token)
        if data is None:
            return None
        # 重新设置，延长存活时间
        self.cache.set(token, data, ttl=self.TOKEN_EXPIRE_TIMEOUT)
        return json.loads(data)

    def remove(self, token):
        if token is None:
            token = request.headers.get(self.TOKEN_KEY, "")
        self.cache.delete(token)


class AccessToken(BaseModel):
    """
    access_token存储表
    """
    __tablename__ = "t_access_token"
    __table_args__ = ({"comment": "Token"})
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    user_id = db.Column(db.Integer, name="user_id", unique=False, nullable=False, comment="用户id")
    user_name = db.Column(db.String(32), name="user_name", unique=False, nullable=False, comment="用户名")
    token = db.Column(db.String(40), name="token", unique=True, nullable=False, comment="token")
    perms = db.Column(db.String(1000), name="perms", unique=False, nullable=True, comment="权限集合")


class MysqlTokenStrategy(AbstractTokenStrategy):
    """
    mysql Token存储策略
    """

    def set(self, data):
        accessToken = AccessToken()
        accessToken.token = data.get("token", TokenStrategyFactory.create_token(data))
        accessToken.user_id = data.get("userId", data.get("id"))
        accessToken.user_name = data.get("userName", "")
        accessToken.perms = data.get("perms", "")
        db.session.add(accessToken)
        db.session.commit()
        data['token'] = accessToken.token
        return data

    def get(self, token):
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=self.TOKEN_EXPIRE_TIMEOUT)
        expireTime = now - delta
        accessToken = AccessToken.query.filter_by(token=token).filter(AccessToken.update_time > expireTime).first()
        if accessToken is None:
            return None
        else:
            # 更新时间,基类已经做了自动更新更新时间，这里只修改一个字段触发更新操作即可
            AccessToken.query.filter_by(id=accessToken.id).update({
                AccessToken.is_deleted: accessToken.is_deleted
            })
            # 提交事务
            db.session.commit()
            return AccessToken.to_dict(accessToken)

    def remove(self, token):
        if token is None:
            token = request.headers.get(self.TOKEN_KEY, "")
        AccessToken.query.filter_by(token=token).delete()


class RedisTokenStrategy(AbstractTokenStrategy):
    """
    Redis Token存储策略
    """

    def set(self, data):
        token = data.get('token', TokenStrategyFactory.create_token(data))
        data['token'] = token
        token = self.TOKEN_KEY_PREFIX + token
        p = redis_client.pipeline()
        p.set(token, json.dumps(data, ensure_ascii=False))
        p.expire(token, self.TOKEN_EXPIRE_TIMEOUT)
        p.execute()
        return data

    def get(self, token):
        data = redis_client.get(self.TOKEN_KEY_PREFIX + token)
        if data is None:
            return None
        p = redis_client.pipeline()
        p.expire(self.TOKEN_KEY_PREFIX + token, self.TOKEN_EXPIRE_TIMEOUT)
        p.execute()
        return json.loads(data.decode("utf-8"))

    def remove(self, token):
        if token is None:
            token = request.headers.get(self.TOKEN_KEY, "")
        p = redis_client.pipeline()
        p.delete(self.TOKEN_KEY_PREFIX + token)
        p.execute()