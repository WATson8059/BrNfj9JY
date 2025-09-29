# 代码生成时间: 2025-09-29 16:27:53
import re
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import JSON

# 自动生成API文档的工具类
class ApiDocGenerator:
    def __init__(self, config):
        self.config = config
        self.routes = []
        self.views = []

    def add_route(self, name, pattern, view):
        """ 添加路由到生成器中 """
        self.routes.append((name, pattern, view))
        self.config.add_route(name, pattern)

    def add_view(self, view):
        """ 添加视图到生成器中 """
        self.views.append(view)

    def generate(self):
        """ 生成API文档 """
        docs = []
        for name, pattern, view in self.routes:
            doc = {
                'name': name,
                'pattern': pattern,
                'view': view,
                'methods': []
            }
            for method in ['GET', 'POST', 'PUT', 'DELETE']:
                if hasattr(view, method.lower()):
                    doc['methods'].append(method)
            docs.append(doc)
        return docs

# Pyramid配置
def main(global_config, **settings):
    """ 配置Pyramid应用 """
    config = Configurator(settings=settings)
    doc_generator = ApiDocGenerator(config)

    # 注册API视图和路由
    @view_config(route_name='example_api', renderer='json')
    def example_api(request):
        """ 示例API视图 """
        return {'message': 'Hello, API!'}

    doc_generator.add_route('example_api', '/example', example_api)
    doc_generator.add_view(example_api)

    # 注册API文档生成器视图
    @view_config(route_name='api_docs', renderer='json')
    def api_docs(request):
        """ 生成API文档的视图 """
        try:
            return doc_generator.generate()
        except Exception as e:
            return {'error': str(e)}

    config.add_route('api_docs', '/docs')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    server.serve_forever()