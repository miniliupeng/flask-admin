import pytest
from flask import Flask

from config import getConfig
from controllers.role_controller import role
from controllers.user_controller import user
from generator import CodeGenerator
from mauth.mtoken import redis_client, TokenStrategyFactory
from mexception import ExceptionConfig
from mlogging import LoggingConfig
from mlogging.request_log import RequestLog
from models import db

app = Flask(__name__)

# 注册用户模块
app.register_blueprint(user)
# 注册角色模块
app.register_blueprint(role)

# 从配置对象中加载
app.config.from_object(getConfig())

# 初始化db
db.init_app(app)
# 初始化redis
redis_client.init_app(app)
# 配置日志
LoggingConfig(app)
# 配置请求日志
RequestLog(app)
# 配置异常处理
ExceptionConfig(app)


@pytest.fixture
def client():
    # 装备一个客户端给test_控制层方法使用
    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        yield client  # this is where the testing happens!
        ctx.pop()


@pytest.fixture
def auth_client():
    """
    装备一个已授权的客户端给test_控制层方法使用
    :return:
    """
    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        token_strategy = TokenStrategyFactory.get_instance()
        data = token_strategy.set({
            "userId": 1,
            "userName": "admin"
        })
        # HTTP_KEY的方式存入全局请求头
        client.environ_base['HTTP_TOKEN'] = data.get('token')
        yield client  # this is where the testing happens!
        ctx.pop()


@pytest.fixture
def m_db():
    """
    装配db对象给test_模型层和服务逻辑层方法使用
    :return:
    """
    with app.app_context():
        yield db
        
@pytest.fixture(scope='class')
def m_table():
    """
    装配m_table对象给test_模型层和服务逻辑层方法使用
    :return:
    """
    with app.app_context():
        code_generator = CodeGenerator(app)
        table = code_generator.build_table('t_role')
        yield table