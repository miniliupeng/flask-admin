import wtforms

from validators import BaseForm, BasePageForm


class RoleForm(BaseForm):
    """
    角色表单校验类
    """
    id = wtforms.IntegerField()
    name = wtforms.StringField("角色名称", [wtforms.validators.DataRequired(message="角色名称不能为空")])
    remark = wtforms.StringField("备注")
    roleKey = wtforms.StringField("角色标识", [wtforms.validators.DataRequired(message="角色标识不能为空")])


class RolePageForm(BasePageForm):
    """
    角色分页校验类
    """
    pass