# 代码生成时间: 2025-07-31 13:23:00
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from pyramid.config import Configurator
from pyramid.paster import get_appsettings

# 数据模型基类
Base = declarative_base()

# 用户数据模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

# 数据库会话管理
def get_engine(settings, name_override=None):
    return create_engine(settings['sqlalchemy.url'])

def get_session_factory(engine, autocommit=True, autoflush=True):
    Session = sessionmaker(bind=engine, autocommit=autocommit, autoflush=autoflush)
    return Session

def get_session(request):
    if not hasattr(request, 'session'):
        request.session = request.registry['session_factory']()
    return request.session

# Pyramid配置
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('.models')
    
    # 数据库配置
    engine = get_engine(settings)
    SessionFactory = get_session_factory(engine)
    config.registry['session_factory'] = SessionFactory
    config.add_request_method(get_session, name='db_session', reify=True)
    
    # 扫描模型并创建表
    Base.metadata.create_all(bind=engine)
    
    # 添加路由
    config.add_route('home', '/')
    config.add_route('add_user', '/add_user')
    
    # 添加视图
    config.scan()
    
    return config.make_wsgi_app()
