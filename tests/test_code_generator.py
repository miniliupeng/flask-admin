import logging

from sqlalchemy import MetaData


class TestCodeGenerator:
    """
    代码生成器单元测试类
    """
    def test_MetaData(self, m_db):
        """
        简单的测试获取元数据
        :param m_db:
        :return:
        """
        MetaData_obj = MetaData()
        MetaData_obj.reflect(bind=m_db.engine, only=["t_role"])
        tables = MetaData_obj.tables
        for table in tables.values():
            logging.info(f"表名称：{table.name}")
            logging.info(f"表注释：{table.comment}")
            logging.info(f"列名,数据类型,是否主键,是否可为空,默认值,是否索引,是否自增")
            for col in table.columns:
                logging.info(f"{col.name},{col.type},{col.primary_key},"
                             f"{col.nullable},{col.default},"
                             f"{col.index},{col.autoincrement}")