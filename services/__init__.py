from decorators import Transactional
from tools.db_tool import DbTool


class BaseService(object):
    """
    业务逻辑怪基类
    """

    def __init__(self, db=None, model=None):
        if db is not None:
            self.db = db
        else:
            from models import db
            self.db = db
        if model is not None:
            self.model = model
        else:
            raise Exception("model不能为空")

    def get(self, form):
        """
        通过id获取用户信息
        :param form:
        :return:
        """
        model = self.db.session.query(self.model).get(form.id.data)
        return model

    def list(self, form):
        """
        分页查询用户列表
        :param form:
        :return:
        """
        # 可通过form.data获取所有提交参数
        # 可通过form.pageNum.data获取pageNum
        # 可通过form.pageSize.data获取pageSize
        # page=self.db.query(User).filter().paginate(form.pageNum.data, form.pageSize.data,False)
        page = DbTool.filter_by_custom(self.model).paginate(form.pageNum.data, form.pageSize.data, False)
        return self.model.to_page(page)

    @Transactional()
    def save(self, form):
        """
        添加用户
        :param form:
        :return:
        """
        model = self.model(**form.data)
        self.db.session.add(model)

    @Transactional()
    def update(self, form):
        """
        修改用户
        :param form:
        :return:
        """
        model = self.model(**form.data)
        self.db.session.query(self.model).filter_by(id=form.id.data).update(model.to_dict(camel=False))

    @Transactional()
    def delete(self, form):
        """
        删除用户
        :param form:
        :return:
        """
        self.db.session.query(self.model).filter(self.model.id.in_(form.ids.data)).delete()