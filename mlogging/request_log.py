import datetime
import os
import threading

from flask import request, g


class RequestLog:
    """
    请求日志处理
    """
    # 是否启用请求日志
    request_log_enable = False
    # 不做请求日志的接口列表，例：['/user/get','/user/list']
    ignore_list = []

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.request_log_enable = app.config.get("REQUEST_LOG_ENABLE")
        if app.config.get('IGNORE_LIST'):
            self.ignore_list = app.config.get('IGNORE_LIST')
        if self.request_log_enable:
            self.app.before_request(self._before_request)
            self.app.after_request(self._after_request)

    def _before_request(self):
        if request.path not in self.ignore_list:
            g.ip = request.remote_addr  # 客户端ip
            g.url = request.url  # 请求地址
            g.start_time = datetime.datetime.now()  # 请求开始时间
            g.process = os.getpid()  # 进程id
            g.thread = threading.currentThread().ident  # 线程id
            if request.is_json:
                g.body = request.get_json()  # 请求正文参数
            else:
                g.body = request.get_data()
                if g.body:
                    g.body = str(g.body, encoding="utf8")
                    g.body = g.body.replace("\n\r", "")

    def _after_request(self, response):
        if request.path not in self.ignore_list:
            g.res_data = str(response.data, encoding="utf8")  # 响应数据
            g.end_time = datetime.datetime.now()  # 请求结束时间
            g.interval = g.end_time - g.start_time  # 请求处理时长
            g.interval = str(g.interval).replace("0:00:", "")
            if hasattr(g, 'current_user'):  # 当前登录用户信息
                self.app.logger.info(
                    f"[{g.current_user}][{g.ip}][{g.url}][{g.start_time}][{g.process}][{g.thread}][{g.body}][{g.res_data}][{g.end_time}][{g.interval}]")
            else:
                self.app.logger.info(
                    f"[][{g.ip}][{g.url}][{g.start_time}][{g.process}][{g.thread}][{g.body}][{g.res_data}][{g.end_time}][{g.interval}]")
        return response