from flask import Blueprint

from controllers import R
from mauth import HasPerm
from models.role import Role
from services.role_service import RoleService
from validators import BasePageForm
from validators.id_validator import IdForm, IdsForm
from validators.role_validator import RoleForm

# 声明一个蓝图
role = Blueprint('role', __name__, url_prefix="/role")

# 声明一个角色业务服务
role_service = RoleService(model=Role)


@role.route("/get", methods=['POST'])
@HasPerm(access="role:get", name="通过id获取角色信息")
def role_get():
    """
    通过id获取角色信息
    :return:
    """
    form = IdForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # 或者直接拿id值 id=form.id.data
    # u = Role.query.filter_by(id=form.id.data).first()
    # 通过主键查询
    u = role_service.get(form)
    if u is not None:
        return R.data(u.to_dict(camel=True))
    else:
        return R.fail("该记录不存在")


@role.route("/list", methods=['POST'])
@HasPerm(access="role:list", name="分页查询角色列表")
def role_list():
    """
    分页查询角色列表
    :return:
    """
    form = BasePageForm()
    form.validate_for_api()
    return R.data(role_service.list(form))


@role.route("/save", methods=['POST'])
@HasPerm(access="role:save", name="添加角色")
def role_save():
    """
    添加角色
    :return:
    """
    form = RoleForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # print(form.data)
    role_service.save(form)
    return R.success("添加角色成功")


@role.route("/update", methods=['POST'])
@HasPerm(access="role:update", name="修改角色")
def role_update():
    """
    修改角色
    :return:
    """
    form = RoleForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # print(form.data)
    role_service.update(form)
    return R.success("修改角色成功")


@role.route("/delete", methods=['POST'])
@HasPerm(access="role:delete", name="删除角色")
def role_delete():
    """
    删除角色
    :return:
    """
    form = IdsForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # print(form.data)
    role_service.delete(form)
    return R.success("删除角色成功")