# 代码生成时间: 2025-08-22 11:23:36
from pyramid.config import Configurator
# 扩展功能模块
from pyramid.view import view_config
from pyramid.security import Authenticated
from pyramid.authentication import AuthTktAuthenticationPolicy
# 增强安全性
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
# NOTE: 重要实现细节

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库模型
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
# 优化算法效率
    username = Column(String, unique=True)
# TODO: 优化性能
    password = Column(String)

# Pyramid配置
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('.routes')
    config.include('.models')

    # 配置数据库连接
    engine = create_engine(settings['sqlalchemy.url'])
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    config.registry['dbsession'] = DBSession

    # 配置认证策略
    authn_policy = AuthTktAuthenticationPolicy(
        secret=settings['auth.secret']
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # 配置会话工厂
# 改进用户体验
    session_factory = SignedCookieSessionFactory(settings['session.secret'])
    config.set_session_factory(session_factory)

    # 配置视图
    config.scan('.views')

    return config.make_wsgi_app()

# 登录视图
@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
    """ Handle login. """
    if request.method == 'POST':
        username = request.params['username']
        password = request.params['password']
# TODO: 优化性能

        # 验证用户
# FIXME: 处理边界情况
        user = DBSession.query(User).filter_by(username=username).first()
        if user and user.password == password:
            login_user(request, user)
            return HTTPFound(location=request.route_url('home'))
# 扩展功能模块
        else:
            request.session.flash('Invalid username or password')
    return {}

# 登录用户
def login_user(request, user):
    """ Login a user given a user object. """
    headers = remember(request, user.id)
    return HTTPFound(location=request.route_url('home'), headers=headers)

# 路由配置
class Routes:
    def __init__(self, config):
        config.add_route('home', '/')
        config.add_route('login', '/login')

# 数据库模型配置
class Models:
    def __init__(self, config):
        config.scan('.models')
        config.include('.models')
        
# 模板视图配置
class Views:
    def __init__(self, config):
        config.scan('.views')
# 改进用户体验