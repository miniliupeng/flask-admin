添加环境变量
export LOG_HANDLER=TimedRotatingFileHandler

查看
echo $LOG_HANDLER

删除
unset LOG_HANDLER


测试
pytest
指定测试某个文件
pytest -q tests/test_demo1.py

# 默认无日志输出
pytest tests/test_user_model.py
# 输出日志
pytest tests/test_user_model.py  --log-cli-level=info

文件名称规范：以test_开头
类名称：以Test开头
类测试方法：以test_开头

关于@pytest.fixture的一些说明
fixture的scope参数
scope参数有四种，分别是'function','module','class','session'，默认为function。

function：每个test都运行，默认是function的scope
class：每个class的所有test只运行一次
module：每个module的所有test只运行一次
session：每个session只运行一次


生成 requirements.txt
pip freeze > ./requirements.txt