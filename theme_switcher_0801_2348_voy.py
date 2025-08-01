# 代码生成时间: 2025-08-01 23:48:28
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.request import Request
from pyramid.security import Authenticated
from pyramid.settings import asbool
from pyramid.threadlocal import get_current_request
import json

# 主题切换视图
@view_config(route_name='switch_theme', request_method='POST', renderer='json')
def switch_theme(request: Request):
    # 获取当前主题
    current_theme = request.registry.settings.get('default_theme', 'light')
    
    # 从POST请求中获取新主题
    new_theme = request.json.get('theme')
    
    # 如果新主题与当前主题不同，更新主题
    if new_theme and new_theme != current_theme:
        # 将新主题保存到用户会话
        request.session['theme'] = new_theme
        return {'status': 'success', 'message': f'Theme switched to {new_theme}'}
    else:
        return {'status': 'error', 'message': 'No theme change requested or invalid theme'}

# 配置Pyramid应用
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    with Configurator(settings=settings) as config:
        # 添加路由
        config.add_route('switch_theme', '/switch_theme')
        # 添加视图
        config.add_view(switch_theme, route_name='switch_theme')
        # 配置默认主题
        config.registry.settings['default_theme'] = 'light'
        
    return config.make_wsgi_app()

# 主函数，用于运行Pyramid应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(global_config={}, **{
        'reload_all': True,
        'debug_all': True,
        'default_theme': 'light'
    })
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()