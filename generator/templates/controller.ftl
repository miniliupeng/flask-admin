from flask import Blueprint

from controllers import R
from mauth import HasPerm
from models.{{table.shortTableName}} import {{table.tableHumpName}}
from services.{{table.shortTableName}}_service import {{table.tableHumpName}}Service
from validators import BasePageForm
from validators.id_validator import IdForm, IdsForm
from validators.{{table.shortTableName}}_validator import {{table.tableHumpName}}Form

# 声明一个蓝图
{{table.shortTableName}} = Blueprint('{{table.shortTableName}}', __name__, url_prefix="/{{table.shortTableName}}")

# 声明一个{{table.comment}}业务服务
{{table.shortTableName}}_service = {{table.tableHumpName}}Service(model={{table.tableHumpName}})


@{{table.shortTableName}}.route("/get", methods=['POST'])
@HasPerm(access="{{table.shortTableName}}:get", name="通过id获取{{table.comment}}信息")
def {{table.shortTableName}}_get():
    """
    通过id获取{{table.comment}}信息
    :return:
    """
    form = IdForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # 或者直接拿id值 id=form.id.data
    # u = {{table.tableHumpName}}.query.filter_by(id=form.id.data).first()
    # 通过主键查询
    u = {{table.shortTableName}}_service.get(form)
    if u is not None:
        return R.data(u.to_dict(camel=True))
    else:
        return R.fail("该记录不存在")


@{{table.shortTableName}}.route("/list", methods=['POST'])
@HasPerm(access="{{table.shortTableName}}:list", name="分页查询{{table.comment}}列表")
def {{table.shortTableName}}_list():
    """
    分页查询{{table.comment}}列表
    :return:
    """
    form = BasePageForm()
    form.validate_for_api()
    return R.data({{table.shortTableName}}_service.list(form))


@{{table.shortTableName}}.route("/save", methods=['POST'])
@HasPerm(access="{{table.shortTableName}}:save", name="添加{{table.comment}}")
def {{table.shortTableName}}_save():
    """
    添加{{table.comment}}
    :return:
    """
    form = {{table.tableHumpName}}Form()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # print(form.data)
    {{table.shortTableName}}_service.save(form)
    return R.success("添加{{table.comment}}成功")


@{{table.shortTableName}}.route("/update", methods=['POST'])
@HasPerm(access="{{table.shortTableName}}:update", name="修改{{table.comment}}")
def {{table.shortTableName}}_update():
    """
    修改{{table.comment}}
    :return:
    """
    form = {{table.tableHumpName}}Form()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # print(form.data)
    {{table.shortTableName}}_service.update(form)
    return R.success("修改{{table.comment}}成功")


@{{table.shortTableName}}.route("/delete", methods=['POST'])
@HasPerm(access="{{table.shortTableName}}:delete", name="删除{{table.comment}}")
def {{table.shortTableName}}_delete():
    """
    删除{{table.comment}}
    :return:
    """
    form = IdsForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # print(form.data)
    {{table.shortTableName}}_service.delete(form)
    return R.success("删除{{table.comment}}成功")
