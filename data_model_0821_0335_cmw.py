# 代码生成时间: 2025-08-21 03:35:36
from pyramid.config import Configurator
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import register

# 数据模型基类
Base = declarative_base()

# 示例用户模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # 构造函数
    def __init__(self, name, email, is_active=True):
        self.name = name
        self.email = email
        self.is_active = is_active
        self.created_at = DateTime.now()

    # 字符串表示
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

# 数据库会话工厂
def get_session():
    # 使用SQLite内存数据库，实际部署时请替换为适当的数据库配置
    engine = create_engine('sqlite:///:memory:')
    Session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return Session

# Pyramid配置函数
def main(global_config, **settings):
    """
    Pyramid WSGI应用程序的配置函数。
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    # 注册数据库会话
    register(config, engine=create_engine('sqlite:///:memory:'))
    # 配置路由和视图
    # config.add_route('home', '/')
    # config.add_view(my_view, route_name='home')
    app = config.make_wsgi_app()
    return app