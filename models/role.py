from models import db, BaseModel


class Role(BaseModel):
    __tablename__ = "t_role"
    __table_args__ = ({"comment": "角色"})
    name = db.Column(db.String(32), unique=False, nullable=True, comment="角色名称")
    remark = db.Column(db.String(100), unique=False, nullable=True, comment="备注")
    role_key = db.Column(db.String(32), unique=False, nullable=True, comment="角色标识")