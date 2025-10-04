# 代码生成时间: 2025-10-05 03:17:22
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.request import Request
import os

# 定义供应商模型
class Supplier:
    def __init__(self, id, name, contact_info):
        self.id = id
        self.name = name
        self.contact_info = contact_info

# 数据库存储（简化为字典）
# 添加错误处理
suppliers_db = {}

# 添加供应商
def add_supplier(request: Request):
    try:
        id = request.matchdict['id']
        name = request.matchdict['name']
# 改进用户体验
        contact_info = request.matchdict['contact_info']
        supplier = Supplier(id, name, contact_info)
        suppliers_db[id] = supplier
        return Response("Supplier added successfully")
    except Exception as e:
        return Response(f"Error adding supplier: {e}", status=500)

# 获取供应商信息
@view_config(route_name='get_supplier')
def get_supplier(request: Request):
    try:
        id = request.matchdict['id']
        supplier = suppliers_db.get(id)
        if supplier:
            return Response(
                f"Supplier Name: {supplier.name}, Contact Info: {supplier.contact_info}"
            )
        else:
            return Response("Supplier not found", status=404)
    except Exception as e:
        return Response(f"Error retrieving supplier: {e}", status=500)

# 配置 Pyramid 应用
def main(global_config, **settings):
    config = Configurator(settings=settings)

    # 添加路由和视图
    config.add_route('add_supplier', '/supplier/add/{id}/{name}/{contact_info}')
    config.add_view(add_supplier, route_name='add_supplier', renderer='string')
    config.add_route('get_supplier', '/supplier/{id}')
# 增强安全性
    config.add_view(get_supplier, route_name='get_supplier', renderer='string')

    # 扫描视图
# TODO: 优化性能
    config.scan()

    return config.make_wsgi_app()

# 运行应用
if __name__ == '__main__':
# FIXME: 处理边界情况
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()