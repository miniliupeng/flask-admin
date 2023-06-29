from functools import wraps


class Transactional(object):
    """
    事务装饰器类
    """
    def __init__(self, db=None):
        if db is None:
            from models import db
            self.db = db
        else:
            self.db = db

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            # 开始事务，with上下文管理器，会自动commit和rollback
            with self.db.session.begin():
                # 调用具体的方法
                res = func(*args, **kwargs)
                return res

        return wrapped_function