from decorators import Transactional
from models.user import User
from services import BaseService
from mexception import AssertTool
from services.enums.user_error_enum import UserErrorEnum

class UserService(BaseService):
    """
    用户模块业务处理类
    """
    def login(self, user_name, password):
        """
        用户密码登录
        :param user_name:
        :param password:
        :return:
        """
        u = self.db.session.query(User).filter(User.user_name == user_name).first()
        if u is None:
            AssertTool.raise_biz(UserErrorEnum.U80009001)
        if u.password != password:
            AssertTool.raise_biz(UserErrorEnum.U80009002)
        res = u.to_dict(camel=True)
        del res['password']
        del res['createTime']
        del res['updateTime']
        del res['isDeleted']
        return res
    
    @Transactional()
    def save_batch(self, form_list):
        """
        批量插入用户-开启事务
        :param form_list:
        :return:
        """
        # # 使用with的话，会自动执行session.commit()，如异常自动执行session.rollback()
        # with self.db.session.begin():  # 开启事物
        #     for form in form_list:
        #         model = User(**form)
        #         self.db.session.add(model)
        #         # flush会将session中的数据刷到数据库中，使数据库主键自增；但不会写到磁盘里
        #         self.db.session.flush()
        
        for form in form_list:
            model = User(**form)
            self.db.session.add(model)
            # flush会将session中的数据刷到数据库中，使数据库主键自增；但不会写到磁盘里
            self.db.session.flush()

    def save_batch_no_trans(self, form_list):
        """
        批量插入用户-未开启事务
        :param form_list:
        :return:
        """
        for form in form_list:
            model = User(**form)
            self.db.session.add(model)
            self.db.session.commit()