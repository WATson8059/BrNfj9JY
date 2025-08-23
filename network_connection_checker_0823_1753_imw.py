# 代码生成时间: 2025-08-23 17:53:02
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import requests


# 定义网络连接状态检查函数
def check_network_connection(url):
    try:
        # 发送HTTP HEAD请求检查网络连接状态
        response = requests.head(url)
        # 返回状态码和响应时间
        return {
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    except requests.ConnectionError:
        # 网络连接错误
        return {'error': 'Network connection error'}
    except requests.Timeout:
        # 请求超时
        return {'error': 'Request timed out'}
    except requests.RequestException as e:
        # 其他请求异常
        return {'error': str(e)}


# Pyramid视图函数，用于网络连接检查
@view_config(route_name='check_connection', renderer='json')
def network_check_view(request):
    # 从请求中获取URL参数
    url = request.params.get('url')
    if not url:
        return Response(json_body={'error': 'URL parameter is required'}, status=400)
    
    # 检查网络连接状态
    result = check_network_connection(url)
    return Response(json_body=result)


# Pyramid配置器
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.add_route('check_connection', '/check_connection')
    config.scan()
    return config.make_wsgi_app()
