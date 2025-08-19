# 代码生成时间: 2025-08-20 03:09:06
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.session import check_authorization_token
from pyramid.view import view_config
import json

# 存储主题的键
THEME_KEY = 'theme'

# 允许的主题列表
ALLOWED_THEMES = ['light', 'dark', 'colorful']

# 错误响应函数
def error_response(message, status_code):
    response = Response(json.dumps({'error': message}), content_type='application/json')
    response.status_code = status_code
    return response

# 主题切换视图
@view_config(route_name='switch_theme', renderer='json')
def switch_theme(request: Request) -> Response:
    """
    处理主题切换请求的视图函数。
    根据请求中的参数切换主题，并返回相应的响应。
    """
    try:
        # 获取请求参数
        theme = request.params.get('theme', 'light')
        # 验证主题是否在允许的列表中
        if theme not in ALLOWED_THEMES:
            return error_response("Invalid theme specified.", 400)
        
        # 设置会话中的主题
        request.session[THEME_KEY] = theme
        
        # 返回成功响应
        return Response(json.dumps({'message': 'Theme switched successfully.', 'theme': theme}), content_type='application/json')
    
    except Exception as e:
        # 处理任何异常并返回500内部服务器错误
        return error_response(f"An error occurred: {str(e)}", 500)

# 配置函数
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        # 扫描视图函数
        config.scan()
        # 添加路由
        config.add_route('switch_theme', '/switch_theme')
        # 添加视图
        config.add_view(switch_theme, route_name='switch_theme')

# 运行程序的主函数
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({
        'pyramid.reload_templates': True,
        'pyramid.debug_all': True,
        'pyramid.default_locale_name': 'en'
    })
    server = make_server('0.0.0.0', 6543, app)
    print('Server started on http://0.0.0.0:6543/')
    server.serve_forever()