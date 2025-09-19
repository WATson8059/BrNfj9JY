# 代码生成时间: 2025-09-20 01:50:52
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.security import allow_guest, Authenticated
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import remember, forget
from pyramid.interfaces import IAuthenticationPolicy
from zope.interface import implementer

# 配置 Pyramid 应用
def main(global_config, **settings):
    config = Configurator(settings=settings)

    # 设置密钥和密钥验证器
    secret = 'your-secret'
    config.set_secret(secret)
    authn_policy = AuthTktAuthenticationPolicy(secret)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # 设置会话工厂
    session_factory = SignedCookieSessionFactory(secret)
    config.set_session_factory(session_factory)

    # 添加视图
    config.add_route('login', '/login')
    config.scan()
    return config.make_wsgi_app()

# 登录视图
@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    # 获取用户名和密码
    username = request.params.get('username')
    password = request.params.get('password')

    # 验证用户名和密码
    if username != 'admin' or password != 'secret':
        return {'error': 'Invalid credentials'}

    # 如果验证成功，返回认证令牌
    auth_header = remember(request, username)
    return {
        'status': 'success',
        'auth_token': auth_header
    }

# 注销视图
@view_config(request_method='POST')
def logout(request):
    # 忘记用户
    forget(request)
    return {'status': 'success'}

# 自定义认证策略
@implementer(IAuthenticationPolicy)
class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        try:
            # 尝试从请求中获取认证的用户名
            user = request.authenticated_userid
            if user:
                return user
        except AttributeError:
            pass
        return None

    # 重写认证方法
    def unauthenticated_userid(self, request):
        # 检查请求中的认证令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            auth_tkt = auth_header.split(' ')[1]
            user = self.decode(auth_tkt)
            if user:
                return user
        return None
