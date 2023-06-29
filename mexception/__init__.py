from enum import Enum

from werkzeug.exceptions import HTTPException

from controllers import R


class ExceptionConfig:
    """
    异常处理配置
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        @app.errorhandler(HTTPException)
        def error_http(e):
            """
            HTTP异常处理(401,403,404,500等)
            :param e: 异常
            :return:
            """
            app.logger.error(e)
            return R.fail(e.description, code=e.code)

        @app.errorhandler(BizException)
        def error_biz(e):
            """
            业务异常处理
            :param e: 异常
            :return:
            """
            app.logger.error(e)
            return R.fail(e.msg, e.code)

        @app.errorhandler(Exception)
        def error(e):
            """
            其他异常处理
            :param e: 异常
            :return:
            """
            app.logger.error(e)
            return R.fail(GlobalErrorEnum.GL99999999.msg, code=GlobalErrorEnum.GL99999999.code)


class ErrorEnum(Enum):
    """
    错误码基类
    """

    def __new__(cls, code, msg):
        obj = object.__new__(cls)
        obj.code = code
        obj.msg = msg
        return obj


class GlobalErrorEnum(ErrorEnum):
    """
    全局错误码
    """
    GL99999999 = (99999999, "服务器异常")
    GL99990100 = (99990100, "参数异常")
    GL99990401 = (99990401, "未授权")
    GL99990500 = (99990500, "未知异常")
    GL99990403 = (99990403, "token过期或不存在")
    GL99990404 = (99990404, "找不到指定资源")
    GL99990406 = (99990406, "无访问权限")
    GL99990001 = (99990001, "注解使用错误")
    GL99990002 = (99990002, "微服务不在线,或者网络超时")
    GL99990003 = (99990003, "没有数据")
    GL99990004 = (99990004, "演示账号，无写权限")
    GL99990005 = (99990005, "数据库插入异常")
    GL99990006 = (99990006, "文件后辍不允许")
    GL99990007 = (99990007, "文件上传异常")
    GL99990008 = (99990008, "文件上传配置不存在")
    GL99990009 = (99990009, "文件超过上传最大值")
    GL99990010 = (99990010, "审核不通过原因不能为空")
    GL99990011 = (99990011, "图片验证码生成异常")
    GL99990012 = (99990012, "图片验证码错误或不存在")
    GL99990013 = (99990013, "演示站无访问权限")


class BizException(Exception):
    """
    业务异常
    """

    def __init__(self, error: ErrorEnum):
        self.code = error.code
        self.msg = error.msg


class AssertTool:
    """
    断言工具
    """

    @staticmethod
    def raise_biz(error_enum: ErrorEnum):
        raise BizException(error_enum)