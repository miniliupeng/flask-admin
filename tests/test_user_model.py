from models.user import User


class TestUserModel:
    """
    User模型测试
    """
    def test_by_user_name_query(self, m_db):
        """
        通过用户名查询测试
        :param m_db:
        :return:
        """
        u = m_db.session.query(User).filter(User.user_name == "admin").first()
        assert u