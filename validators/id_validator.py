from wtforms import IntegerField, validators, FieldList

from validators import BaseForm


class IdForm(BaseForm):
    """
    校验规则：主键只能为>0的整数{"id": 1}
    """
    id = IntegerField("id", [validators.DataRequired(message="id不能为空")])


class IdsForm(BaseForm):
    """
    校验规则：ids集合>0{"ids": [1,3,4]}
    """
    ids = FieldList(IntegerField("id",[validators.DataRequired(message="id不能为空")]), min_entries=1)