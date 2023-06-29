
from flask import Flask, request
from flask_migrate import Migrate
from sqlalchemy import text

from config import getConfig
from controllers import R
from controllers.role_controller import role
from controllers.user_controller import user
from mauth.mtoken import redis_client
from models import db

from mlogging import LoggingConfig
from mlogging.request_log import RequestLog

from mexception import ExceptionConfig

app = Flask(__name__)

# 注册用户模块
app.register_blueprint(user)
# 注册角色模块
app.register_blueprint(role)

# Flask中新增数据库配置
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

# 执行数据库迁移相关操作。flask db指令不能直接使用，需要获取Migrate实例，这里注册Migrate实例
migrate = Migrate(app, db)

# 配置代码生成器-仅开发环境配置
if app.config.get("ENV") == "dev":
    from generator import CodeGenerator
    CodeGenerator(app)

# @app.before_request
def auth():
    # 简单处理一下，非白名单路由，提示登录
    if request.path not in app.config['WHITE_LIST']:
        return R.fail("请先登录")
    
@app.route("/ex/test")
def ex_test():
    """
    测试其他异常
    :return:
    """
    a = 3 / 0
    return a
    
@app.route("/db/test")
def db_test():
    cursor = db.session.execute(text('select * from sys_user'))
    result = cursor.fetchall()
    if len(result) > 0:
        u = result[0]
        return R.data({
            "id": u.id,
            "userName": u.user_name
        })
    return R.fail("无记录")

@app.route("/config/test")
def config_test():
    """
    配置测试
    :return:
    """
    return R.data({
        'APP_AUTHOR': app.config['APP_AUTHOR'],
        "ENV": app.config['ENV']
    })





@app.errorhandler(404)
def error_404(e):
    """
    404异常处理
    :param e:
    :return:
    """
    return R.fail("请求地址不存在")


@app.errorhandler(Exception)
def error(e):
    """
    其他异常处理
    :param e: 异常
    :return:
    """
    return R.fail(str(e))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
