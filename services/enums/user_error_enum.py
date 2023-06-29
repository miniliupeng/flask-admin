from mexception import ErrorEnum


class UserErrorEnum(ErrorEnum):
    """
    用户模块错误码
    """
    U80009001 = (80009001, "用户不存在")
    U80009002 = (80009002, "用户名或者密码错误")