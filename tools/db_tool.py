from flask import request

from models import db
from tools import hump_to_underline


class DbTool:
    """
    db工具
    """
    @staticmethod
    def get_condition_params():
        """
        获取自定义查询参数
        :return:
        """
        data = request.get_json()
        res = []
        for (key, value) in data.items():
            if key.startswith("m_"):
                arr = key.split("_")
                if len(arr) == 3:
                    res.append({
                        "table": None,
                        "op": arr[1],
                        "key": arr[2],
                        "value": value
                    })
                elif len(arr) == 4:
                    res.append({
                        "table": arr[1],
                        "op": arr[2],
                        "key": arr[3],
                        "value": value
                    })
        return res

    @staticmethod
    def filter_by_custom(model):
        """
        单表-自定义查询条件
        :param model:
        :return:
        """
        conditions = DbTool.get_condition_params()
        q = db.session.query(model)
        for item in conditions:
            key = hump_to_underline(item.get('key'))
            if not hasattr(model, key):
                continue
            op = item.get('op', 'EQ')
            value = item.get('value')
            if op == 'EQ':
                q = q.filter(getattr(model, key) == value)
            elif op == 'NE':
                q = q.filter(getattr(model, key) != value)
            elif op == 'GT':
                q = q.filter(getattr(model, key) > value)
            elif op == 'GE':
                q = q.filter(getattr(model, key) >= value)
            elif op == 'LT':
                q = q.filter(getattr(model, key) < value)
            elif op == 'LE':
                q = q.filter(getattr(model, key) <= value)
            elif op == 'BT':
                if isinstance(value,list) and len(value) == 2:
                    q = q.filter(getattr(model, key).between(value[0], value[1]))
            elif op == 'LIKE':
                q = q.filter(getattr(model, key).like('%' + value + '%'))
            elif op == 'NLIKE':
                q = q.filter(getattr(model, key).notlike('%' + value + '%'))
            elif op == 'LLIKE':
                q = q.filter(getattr(model, key).like('%' + value))
            elif op == 'RLIKE':
                q = q.filter(getattr(model, key).like(value + '%'))
            elif op == 'IN':
                if isinstance(value, list):
                    q = q.filter(getattr(model, key).in_(value))
            elif op == 'NIN':
                if isinstance(value, list):
                    q = q.filter(getattr(model, key).notin_(value))
        return q