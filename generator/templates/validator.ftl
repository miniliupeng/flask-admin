import wtforms

from validators import BaseForm, BasePageForm


class {{table.tableHumpName}}Form(BaseForm):
    """
    {{table.comment}}表单校验类
    """
    id = wtforms.IntegerField(){% for column in table.columns %}{%if column.name not in ['id','create_time','update_time','is_deleted']%}
    {{column.camelName}} = wtforms.StringField("{{column.comment}}"{%if not column.nullable%}, [wtforms.validators.DataRequired(message="{{column.comment}}不能为空")]{%endif%}){%endif%}{% endfor %}


class {{table.tableHumpName}}PageForm(BasePageForm):
    """
    {{table.comment}}分页校验类
    """
    pass