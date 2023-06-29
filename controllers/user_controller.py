from flask import Blueprint, request, current_app

from controllers import R
from mauth import HasPerm, TokenStrategyFactory
from models.user import User
from services.user_service import UserService
from validators import BasePageForm
from validators.id_validator import IdForm, IdsForm
from validators.user_validator import UserForm, LoginForm

# 声明一个蓝图
user = Blueprint('user', __name__, url_prefix="/user")


# 声明一个用户业务服务
user_service = UserService(model=User)

@user.route("/get", methods=['POST'])
@HasPerm(access="user:get", name="通过id获取用户信息")
def user_get():
    """
    通过id获取用户信息
    :return:
    """
    form = IdForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # 或者直接拿id值 id=form.id.data
    # u = User.query.filter_by(id=form.id.data).first()
    # 通过主键查询
    
    # u = User.query.get(form.id.data)
    
    u = user_service.get(form)
    if u is not None:
        # return R.data({
        #     "id": u.id,
        #     "userName": u.user_name,
        #     "realName": u.real_name
        # })
        return R.data(u.to_dict(camel=True))
    else:
        return R.fail("该记录不存在")


@user.route("/list", methods=['POST'])
@HasPerm(access="user:list", name="分页查询用户列表")
def user_list():
    """
    分页查询用户列表
    :return:
    """
    form = BasePageForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # 可通过form.pageNum.data获取pageNum
    # 可通过form.pageSize.data获取pageSize
    
    # user_obj=User.query.filter().paginate(page=form.pageNum.data, per_page=form.pageSize.data, error_out=False)
    
    # user_obj = DbTool.filter_by_custom(User).paginate(page=form.pageNum.data, per_page=form.pageSize.data, error_out=False)
    
    # print(user_obj.page) # 当前页码-从1开始
    # print(user_obj.per_page) # 每页大小
    # print(user_obj.total)    # 总记录数
    # print(user_obj.items)    # 数据集
    
    # return R.data(User.to_page(user_obj))
    
    return R.data(user_service.list(form))


@user.route("/save", methods=['POST'])
@HasPerm(access="user:save", name="添加用户")
def user_save():
    """
    添加用户
    :return:
    """
    form = UserForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # u = User()
    # u.user_name = form.data.get("userName")
    # u.real_name = form.data.get("realName")
    # u.password = form.data.get("password")
    
    # u = User(**form.data)
    # db.session.add(u)
    # db.session.commit()
    
    user_service.save(form)
    return R.success("添加用户成功")


@user.route("/update", methods=['POST'])
@HasPerm(access="user:update", name="修改用户")
def user_update():
    """
    修改用户
    :return:
    """
    form = UserForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    
    # u = User(**form.data)
    # User.query.filter_by(id=form.id.data).update(u.to_dict(camel=False))
    # db.session.commit()
    
    user_service.update(form)
    return R.success("修改用户成功")


@user.route("/delete", methods=['POST'])
@HasPerm(access="user:delete", name="删除用户")
def user_delete():
    """
    删除用户
    :return:
    """
    form = IdsForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    
    # User.query.filter(User.id.in_(form.ids.data)).delete()
    # db.session.commit()
    
    user_service.delete(form)
    return R.success("删除用户成功")


@user.route("/login", methods=['POST'])
def user_login():
    """
    登录
    :return:
    """
    form = LoginForm()
    form.validate_for_api()
    # 可通过form.data获取所有提交参数
    # print(form.data)
    res = user_service.login(form.userName.data, form.password.data)
    current_app.logger.info("[{id}][{userName}][登录系统]".format(**res))
    token_strategy = TokenStrategyFactory.get_instance()
    return R.data(token_strategy.set({
        "userId": res.get("id"),
        "userName": res.get("userName")
    }))

@user.route('/logout')
def user_logout():
    """
    退出
    :return:
    """
    token_strategy = TokenStrategyFactory.get_instance()
    token_strategy.remove(None)
    return R.success()

@user.route("/saveBatch", methods=['POST'])
def user_save_batch():
    """
    批量插入用户-开启事务
    :return:
    """
    # 复杂的表单校验-wtforms支持不是很好，这里先不校验
    user_service.save_batch(request.get_json())
    return R.success("添加成功")


@user.route("/saveBatchNoTrans", methods=['POST'])
def user_save_batch_no_trans():
    """
    批量插入用户-未开启事务
    :return:
    """
    # 复杂的表单校验-wtforms支持不是很好，这里先不校验
    user_service.save_batch_no_trans(request.get_json())
    return R.success("添加成功")