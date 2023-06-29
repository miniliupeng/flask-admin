from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from tools import underline_to_camel, hump_to_underline

db = SQLAlchemy()

class BaseModel(db.Model):
    """
    普通模型基类
    """
    __abstract__ = True
    id = db.Column(db.BigInteger, primary_key=True, comment="主键")
    create_time = db.Column(db.DateTime, name="create_time", default=datetime.now, comment="创建时间")
    update_time = db.Column(db.DateTime, name="update_time", default=datetime.now, onupdate=datetime.now,
                            comment="更新时间")
    is_deleted = db.Column(db.Boolean, name="is_deleted", default=False, comment="逻辑删除:0=未删除,1=删除")

    def __init__(self, **kwargs):
        """
        构造函数，将dict=>obj
        :param kwargs: 校验表单的**form.data
        """
        for (key, value) in kwargs.items():
            underline_key = hump_to_underline(key)
            if hasattr(self, underline_key):
                self.__dict__.update({
                    underline_key: value
                })

    def to_dict(self, camel=True):
        """
        对象转成dict
        :param camel: 是否转成小驼峰，默认True
        :return:
        """
        m_dict = {}
        if self is not None:
            for c in self.__table__.columns:
                key = c.name
                if hasattr(self, key):
                    value = getattr(self, key)
                    if value is not None:
                        if camel:
                            m_dict[underline_to_camel(key)] = value
                        else:
                            m_dict[key] = value

        return m_dict

    @staticmethod
    def to_page(page):
        # print(page.page) # 当前页码-从1开始
        # print(page.per_page) # 每页大小
        # print(page.total)    # 总记录数
        # print(page.items)    # 数据集
        if page is None:
            return None
        rows = []
        for u in page.items:
            rows.append(u.to_dict(camel=True))
        return {
            "recordCount": page.total,
            "totalPage": int((page.total - 1) / page.per_page) + 1,
            "pageSize": page.per_page,
            "pageNum": page.page,
            "rows": rows
        }

class TreeModel(BaseModel):
    """
    树型表模型基类
    """
    __abstract__ = True
    parent_id = db.Column(db.BigInteger, primary_key=True, default=0, comment="父ID")
    name = db.Column(db.String(64), name="name", nullable=False, comment="名称")
    sort = db.Column(db.BigInteger, name="sort", default=99, nullable=False, comment="排序")
                     