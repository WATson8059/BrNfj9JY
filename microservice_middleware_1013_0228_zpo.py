# 代码生成时间: 2025-10-13 02:28:23
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import requests

# 微服务通信中间件
class MicroServiceMiddleware:
    def __init__(self, config):
        self.config = config
        self.service_url = self.config.registry.settings['service_url']
        
    # 发送请求到微服务
    def call_service(self, endpoint, method, data=None):
        try:
            url = f"{self.service_url}/{endpoint}"
            if method == 'GET':
                response = requests.get(url, params=data)
            elif method == 'POST':
                response = requests.post(url, json=data)
            else:
                raise ValueError("Invalid HTTP method")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            raise Exception(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            raise Exception(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            raise Exception(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            raise Exception(f"Oops: Something Else: {err}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

# Pyramid视图函数
@view_config(route_name='service_request', renderer='json')
def service_request(request):
    # 获取请求参数
    endpoint = request.matchdict['endpoint']
    method = request.method
    data = request.json_body if method == 'POST' else None

    # 实例化中间件
    middleware = MicroServiceMiddleware(request.registry)

    # 发送请求到微服务
    response_data = middleware.call_service(endpoint, method, data)

    # 返回响应
    return Response(json_body=response_data)

# 主配置函数
def main(global_config, **settings):
    config = Configurator(settings=settings)
    # 添加路由
    config.add_route('service_request', '/service/{endpoint}')
    # 扫描视图函数
    config.scan()
    return config.make_wsgi_app()
