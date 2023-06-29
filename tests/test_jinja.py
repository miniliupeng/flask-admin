import logging

from jinja2 import Environment, FileSystemLoader


class TestJinja:
    def test_value(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        template = """
        {{table.tableName}}-{{table.comment}}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    def test_if(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        template = """
        {% if table.tableName == 't_role'%}
        我是角色表
        {%endif%}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    def test_if_elif(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        template = """
        {% if table.tableName == 't_user'%}
        我是用户表
        {% elif table.tableName == 't_role'%}
        我是角色表
        {%endif%}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    def test_if_elif_else(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        template = """
        {% if table.tableName == 't_user'%}
        我是用户表
        {% elif table.tableName == 't_access_token'%}
        我是token表
        {% else %}
        我是角色表
        {%endif%}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    def test_for(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        template = """
        {% for column in table.columns %}
        {{column.name}}-{{column.comment}}
        {% endfor %}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    def test_for_if(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        template = """
        {% for column in table.columns %}
            {%if column.name not in ['id','create_time','update_time','is_deleted']%}
                {{column.name}}-{{column.comment}}
            {% endif %}
        {% endfor %}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    def test_filter(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        template = """
        {{table.tableName}}------{{table.tableName | lower }}
        {{table.tableName}}------{{table.tableName | replace('t_','') }}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    def test_my_fun(self, m_table):
        env = Environment(loader=FileSystemLoader('generator/templates'))
        # 增加自定义过滤器-my_fun
        env.filters['my_fun'] = self.my_fun
        template = """
        {{ table.comment | my_fun }}
        """
        templateData = {
            'table': m_table
        }
        s = env.from_string(template).render(templateData)
        logging.info(s)

    @staticmethod
    def my_fun(text):
        return "=="+text+"=="