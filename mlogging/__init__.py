import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from flask.logging import default_handler


class LoggingConfig:
    """
    日志配置
    """
    # 日志输出格式配置
    formatter = "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s"
    # 日志等级
    log_level = "DEBUG"
    # 文件日志默认存放在项目根目录下的logs目录下
    log_path = None
    # 日志处理器配置StreamHandler/TimedRotatingFileHandler/RotatingFileHandler
    log_handler = "StreamHandler"
    # 日志文件最大值默认10M
    max_bytes = 1024 * 1024 * 10
    # 保留日志文件数
    backup_count = 30

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if app.config.get("LOG_FORMATTER"):
            self.formatter = app.config.get("LOG_FORMATTER")
        if app.config.get("LOG_LEVEL"):
            self.log_level = app.config.get("LOG_LEVEL")
        self.log_path = os.path.join(app.root_path, 'logs')
        if app.config.get("LOG_PATH"):
            self.log_path = app.config.get("LOG_PATH")
        if app.config.get("LOG_HANDLER"):
            self.log_handler = app.config.get("LOG_HANDLER")
        if app.config.get("LOG_MAX_BYTES"):
            self.max_bytes = app.config.get("LOG_MAX_BYTES")
        if app.config.get("LOG_BACKUP_COUNT"):
            self.backup_count = app.config.get("LOG_BACKUP_COUNT")
        # 设置flask-logger的日志级别
        self.app.logger.setLevel(self.get_level())
        # 删除默认的日志处理器-控制台输出
        self.app.logger.removeHandler(default_handler)
        if self.log_handler.lower() == "TimedRotatingFileHandler".lower():
            self.app.logger.addHandler(self.build_timed_rotating_file_handler())
        elif self.log_handler.lower() == "RotatingFileHandler".lower():
            self.app.logger.addHandler(self.build_rotating_file_handler())
        else:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(self.formatter))
            self.app.logger.addHandler(handler)

    def build_rotating_file_handler(self):
        """
        按照日志大小进行切分
        :return:
        """
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        handler = RotatingFileHandler(os.path.join(self.log_path, 'flask.log'), maxBytes=self.max_bytes,
                                      backupCount=self.backup_count)
        handler.setLevel(self.get_level())
        handler.setFormatter(logging.Formatter(self.formatter))
        return handler

    def build_timed_rotating_file_handler(self):
        """
        按照日期进行切分
        :return:
        """
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        handler = TimedRotatingFileHandler(os.path.join(self.log_path, 'flask.log'), when="D", interval=1,
                                           backupCount=self.backup_count, encoding="UTF-8",
                                           delay=False, utc=True)
        handler.setLevel(self.get_level())
        handler.setFormatter(logging.Formatter(self.formatter))
        return handler

    def get_level(self):
        """
        获取日志输出级别
        :return:
        """
        if self.log_level.lower() == "INFO".lower():
            return logging.INFO
        elif self.log_level.lower() == "WARN":
            return logging.WARN
        elif self.log_level.lower() == "ERROR":
            return logging.ERROR
        elif self.log_level.lower() == "FATAL":
            return logging.FATAL
        else:
            return logging.DEBUG