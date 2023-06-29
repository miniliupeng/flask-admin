from models import db, BaseModel


class {{table.tableHumpName}}(BaseModel):
    __tablename__ = "{{table.tableName}}"
    __table_args__ = ({"comment": "{{table.comment}}"}){% for column in table.columns %}{%if column.name not in ['id','create_time','update_time','is_deleted']%}
    {{column.name}} = db.Column(db.{{column.type}}({% if column.length is not none%}{{column.length}}{%endif%}), unique={% if column.unique is not none%}True{% else %}False{%endif%}, nullable={% if column.nullable is not none%}True{% else %}False{%endif%}, comment="{{column.comment}}"){%endif%}{% endfor %}