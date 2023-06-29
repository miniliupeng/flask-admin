import os
from urllib import parse


class BaseConfig:
    """
    基础配置
    """
    DEBUG = True  # 调试模式
    APP_AUTHOR = "lp"   # 作者
    WHITE_LIST = ['/user/get', '/user/list', '/ex/test', '/ex/other', "/db/test", "/config/test"]   # 权限白名单
    DB_HOST = os.getenv("DB_HOST", "localhost")  # 数据库ip
    DB_PORT = os.getenv("DB_PORT", "3306")  # 数据库端口
    DB_NAME = os.getenv("DB_NAME", "flaskapp")  # 数据库名称
    DB_USER = os.getenv("DB_USER", "root")  # 数据库用户
    DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")  # 数据库密码
    # 数据库相关配置开始
    # 防止密码中有特殊字符，需要使用parse.quote_plus进行转义
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{parse.quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_timeout': 90,
        'pool_recycle': 7200,
        'max_overflow': 1024
    }
    # 数据库相关配置结束
    JSON_AS_ASCII = False  # 禁止中文转义'
    
    # ------redis相关配置------
    # 环境变量中获取数据库REDIS_HOST
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    # 环境变量中获取数据库REDIS_PORT
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    # 环境变量中获取数据库REDIS_PASSWORD
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    # REDIS_URL = "redis://:password@localhost:6379/0" --->flask-redis需要该配置
    REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
    # ------redis相关配置------
    
    # ------token相关配置------
    # token 过期时间- 单位是s  # 2小时
    TOKEN_EXPIRE_TIMEOUT = int(os.getenv("TOKEN_EXPIRE_TIMEOUT", 60 * 60 * 2))
    # token-key
    TOKEN_KEY = os.getenv("TOKEN_KEY", "token")
    # token 前辍
    TOKEN_KEY_PREFIX = os.getenv("TOKEN_KEY", "flaskapp:")
    # 超级管理员id
    SUPER_ADMIN_ID = os.getenv("SUPER_ADMIN_ID", 1)
    # Token存储策略
    TOKEN_STRATEGY = os.getenv("TOKEN_STRATEGY", "cache")
    # ------token相关配置------
    
    # ------日志相关配置------
    # 日志格式输出配置
    LOG_FORMATTER = os.getenv("LOG_FORMATTER", "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    # 日志等级DEBUG/INFO/WARN/ERROR
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    # 日志存放目录-文件日志默认存放在项目根目录下的logs目录下
    LOG_PATH = os.getenv("LOG_PATH", None)
    # 日志处理器StreamHandler/TimedRotatingFileHandler/RotatingFileHandler
    LOG_HANDLER = os.getenv("LOG_HANDLER", "StreamHandler")
    # 日志文件最大值默认10M
    LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 1024 * 1024 * 10))
    # # 保留日志文件数
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 30))
    # ------日志相关配置------
    
    # ------请求日志配置------
    # 是否启用请求日志记录
    REQUEST_LOG_ENABLE = bool(os.getenv("REQUEST_LOG_ENABLE", True))
    # 不做请求日志的接口，例：['/user/get','/user/list']
    IGNORE_LIST = []
    # ------请求日志配置------
    
class Development(BaseConfig):
    PORT = 6000
    DEBUG = True
    ENV = "dev"
    TESTING = True
    SQLALCHEMY_ECHO = True  # 打印SQL


class Test(BaseConfig):
    PORT = 5000
    DEBUG = True
    ENV = "test"
    TESTING = True


class Production(BaseConfig):
    PORT = 5000
    DEBUG = False
    ENV = "prod"
    TESTING = False


def getConfig():
    # 从环境变量中加载ENV
    env = os.getenv("ENV", "dev")
    if env == "test":
        return Test
    elif env == "prod" or env == "production":
        return Production
    else:
        return Development