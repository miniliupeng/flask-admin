from flask import request
from wtforms import Form, validators, IntegerField


class BaseForm(Form):
    """
    校验基类
    """

    def __init__(self, data=None):
        if data:
            super(BaseForm, self).__init__(data=data)
        else:
            data = request.get_json()
            args = request.args.to_dict()
            super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise Exception(self.errors)
        return self


class BasePageForm(BaseForm):
    """
    基础的分页参数类
    """
    pageNum = IntegerField("pageNum", [validators.DataRequired(message="页码不能为空")])
    pageSize = IntegerField("pageSize", [validators.DataRequired(message="每页条数不能为空")])
