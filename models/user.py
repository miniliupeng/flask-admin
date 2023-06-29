from models import db, BaseModel


class User(BaseModel):
    __tablename__ = "t_user"
    __table_args__ = ({"comment": "用户"})
    user_name = db.Column(db.String(32), name="user_name", unique=True, nullable=False, comment="用户名")
    real_name = db.Column(db.String(32), name="real_name", unique=False, nullable=False, comment="姓名")
    password = db.Column(db.String(64), name="password", unique=False, nullable=False, comment="密码")