# 代码生成时间: 2025-09-05 14:33:58
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, Everyone, Deny
from pyramid.view import view_config

# 设置密钥和认证策略
SECRET = 'your-secret-key-here'
authn_policy = AuthTktAuthenticationPolicy(secret=SECRET)
authz_policy = ACLAuthorizationPolicy()

# 创建配置器
config = Configurator(settings={'pyramid.secret': SECRET},
                       authentication_policy=authn_policy,
                       authorization_policy=authz_policy)

# 定义访问控制列表
class ACL:
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'group:admins', 'edit'),
        (Deny, Everyone, 'edit')
    ]

# 定义视图函数
@view_config(route_name='home')
def home(request):
    # 检查用户是否有权限访问视图
    if not request.has_permission('view'):
        raise Exception("Access denied")
    # 返回主页内容
    return "Welcome to the home page."

@view_config(route_name='admin')
def admin(request):
    # 检查用户是否有权限访问视图
    if not request.has_permission('edit'):
        raise Exception("Access denied")
    # 返回管理员页面内容
    return "Welcome to the admin page."

# 将视图函数和路由关联
config.add_route('home', '/')
config.add_route('admin', '/admin')
config.scan()

# 运行应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    print('Serving on port 6543...')
    server.serve_forever()