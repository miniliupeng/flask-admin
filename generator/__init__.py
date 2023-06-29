import json
import os
import re

import click
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import MetaData

from tools import underline_to_camel, underline_to_hump, underline_to_short


class CodeGenerator:
    """
    代码生成器
    """
    db = None
    engine = None
    table_list = []
    gen_cli = AppGroup('code', help="代码生成相关命令")
    config = None

    def __init__(self, app=None):
        self.app = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.init_config()
        self.db = SQLAlchemy(app)
        self.engine = self.db.engine
        self.init_cli()

    def print_table(self):
        """
        打印元数据信息
        :return:
        """
        for table in self.table_list:
            self.app.logger.info(json.dumps(table, sort_keys=False, ensure_ascii=False))

    def build_table(self, tableName: str = "", ignorePrefix: str = "t_"):
        """
        根据表名称构建元数据-重新组织元数据
        :param tableName: 表名称
        :param ignorePrefix: 转小驼峰和大驼峰时要忽略的表前辍，默认t_
        :return:
        """
        tableName = tableName.replace("%", "")
        MetaData_obj = MetaData()
        MetaData_obj.reflect(bind=self.engine)
        tables = MetaData_obj.tables
        self.table_list = []
        for table in tables.values():
            if not table.name.startswith(tableName):
                continue
            columns = []
            m_table = {
                "tableName": table.name,
                "tableCamelName": underline_to_camel(table.name.replace(ignorePrefix, "")),
                "tableHumpName": underline_to_hump(table.name.replace(ignorePrefix, "")),
                "shortTableName": table.name.replace(ignorePrefix, ""),
                "comment": table.comment,
                "columns": columns
            }
            for col in table.columns:
                m_type = str(col.type.get_dbapi_type)
                # <bound method Integer.get_dbapi_type of INTEGER(display_width=11)>
                # <bound method String.get_dbapi_type of VARCHAR(length=32)>
                # <bound method DateTime.get_dbapi_type of DATETIME()>
                r = re.findall('.+method (.+)\.get_dbapi_type', m_type)
                m_type = r[0]
                columns.append({
                    "name": col.name,
                    "camelName": underline_to_camel(col.name),
                    "comment": col.comment,
                    "primaryKey": col.primary_key,
                    "nullable": col.nullable,
                    "default": col.default,
                    "index": col.index,
                    "unique": col.unique,
                    "autoincrement": col.autoincrement is True,
                    "length": getattr(col.type, 'display_width', getattr(col.type, 'length', None)),
                    "type": m_type
                })
            self.table_list.append(m_table)
            return m_table

    def init_cli(self):
        """
        注册代码生成相关命令
        :return:
        """

        @self.gen_cli.command('gen', help="代码生成")
        @click.option('-t', required=True, help="要代码生成的表")
        @click.option('-ignore_prefix', default="t_", required=False, help="忽略的表前辍")
        def gen(t, ignore_prefix):
            self.build_table(t, ignorePrefix=ignore_prefix)
            self.gen_code()

        @self.gen_cli.command('show', help="查看元数据")
        @click.option('-t', required=True, help="要查看元数据的表")
        @click.option('-ignore_prefix', default="t_", help="忽略的表前辍")
        def show(t, ignore_prefix):
            self.build_table(t, ignorePrefix=ignore_prefix)
            self.print_table()

        self.app.cli.add_command(self.gen_cli)

    def init_config(self):
        """
        加载配置文件
        :return:
        """
        with open("generator/config.json", "r") as f:
            self.config = json.load(f)

    def gen_code(self):
        """
        生成代码
        """
        env = Environment(loader=FileSystemLoader('generator/templates'))
        templates = self.config['templates']
        for table in self.table_list:
            templateData = {}
            templateData.update(self.config)
            templateData.update({"table": table})
            for item in templates:
                if not item.get("selected"):
                    break
                template = env.get_template(item['templateFile'])
                path = self.config['targetProject'] + item['targetPath']
                # 配置参数替换-模板引擎
                path = env.from_string(path).render(templateData)
                # 替换包名为目录
                path = path.replace(".", "/")
                if not os.path.exists(path):
                    os.makedirs(path)
                # 配置参数替换-模板引擎
                targetFileName = env.from_string(item['targetFileName']).render(templateData)
                dist = path + targetFileName

                if os.path.exists(dist):
                    if item.get("covered"):
                        with open(dist, 'w', encoding=item.get("encoding")) as f:
                            html = template.render(templateData)
                            f.write(html)
                            print(f"{templateData['table']['tableName']}表代码生成成功-覆盖：{dist}")
                    else:
                        print(f"{dist}文件已存在，不覆盖")
                else:
                    with open(dist, 'w', encoding=item['encoding']) as f:
                        html = template.render(templateData)
                        f.write(html)
                        print(f"{templateData['table']['tableName']}表代码生成成功-新生成：{dist}")
        return 1