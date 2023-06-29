from wtforms import IntegerField, StringField, validators, PasswordField

from validators import BaseForm


class UserForm(BaseForm):
    """
    用户表单校验类
    """
    id = IntegerField()
    userName = StringField("用户名", [validators.DataRequired(message="用户名不能为空")])
    realName = StringField("姓名", [validators.DataRequired(message="姓名不能为空")])
    password = PasswordField("密码", [validators.DataRequired(message="密码不能为空")])
    confirmPassword = StringField("确认密码", [validators.EqualTo("password", message="两密码不一致")])

    @staticmethod
    def validate_userName(form, field):
        if field.data == "error":
            raise Exception("自定义方法校验测试")
        
    @staticmethod
    def validate_realName(form, field):
        if field.data == "刘鹏":
            raise Exception("自定义方法校验测试")
        

class LoginForm(BaseForm):
    """
    用户名密码登录
    """
    userName = StringField("用户名", [validators.DataRequired(message="用户名不能为空")])
    password = PasswordField("密码", [validators.DataRequired(message="密码不能为空")])