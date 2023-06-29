import json


class TestUserController:
    """
    用户控制层单元测试类
    """
    def test_user_login(self, client):
        """
        测试登录
        :param client:
        :return:
        """
        res = client.post('/user/login', data=json.dumps({
            "userName": "admin",
            "password": "123456"
        }), content_type='application/json')
        assert res.json.get('code') == 0

    def test_user_get(self, auth_client):
        """
        注册通过id获取用户信息
        :param auth_client:
        :return:
        """
        res = auth_client.post('/user/get', data=json.dumps({
            "id": 1
        }), content_type='application/json')
        assert res.json.get('code') == 0