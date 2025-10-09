# 代码生成时间: 2025-10-09 17:40:04
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import json

# Inventory 数据模型
class InventoryItem:
    def __init__(self, item_id, name, quantity):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity

    @classmethod
    def from_json(cls, data):
        return cls(data['item_id'], data['name'], data['quantity'])

# 库存管理系统
class InventoryManagement:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        if item.item_id in self.items:
            raise ValueError("Item already exists.")
        self.items[item.item_id] = item

    def remove_item(self, item_id):
        if item_id not in self.items:
            raise ValueError("Item not found.")
        del self.items[item_id]

    def update_item(self, item):
        if item.item_id not in self.items:
            raise ValueError("Item not found.")
        self.items[item.item_id] = item

    def get_item(self, item_id):
        return self.items.get(item_id, None)

    def list_items(self):
        return list(self.items.values())

# Pyramid 视图配置
def inventory_add(request):
    try:
        data = json.loads(request.body)
        item = InventoryItem.from_json(data)
        inventory.add_item(item)
        return Response("Item added successfully.")
    except ValueError as e:
        return Response(str(e), status=400)

@view_config(route_name='inventory_add', request_method='POST')
def add_item_view(request):
    return inventory_add(request)

def inventory_remove(request):
    try:
        item_id = request.matchdict['item_id']
        inventory.remove_item(item_id)
        return Response("Item removed successfully.")
    except ValueError as e:
        return Response(str(e), status=400)

@view_config(route_name='inventory_remove', request_method='DELETE')
def remove_item_view(request):
    return inventory_remove(request)

def inventory_update(request):
    try:
        data = json.loads(request.body)
        item = InventoryItem.from_json(data)
        inventory.update_item(item)
        return Response("Item updated successfully.")
    except ValueError as e:
        return Response(str(e), status=400)

@view_config(route_name='inventory_update', request_method='PUT')
def update_item_view(request):
    return inventory_update(request)

def inventory_get(request):
    try:
        item_id = request.matchdict['item_id']
        item = inventory.get_item(item_id)
        if item:
            return Response(json.dumps(vars(item)))
        else:
            return Response("Item not found.", status=404)
    except Exception as e:
        return Response(str(e), status=500)

@view_config(route_name='inventory_get', request_method='GET')
def get_item_view(request):
    return inventory_get(request)

def inventory_list(request):
    try:
        items = inventory.list_items()
        return Response(json.dumps([vars(item) for item in items]))
    except Exception as e:
        return Response(str(e), status=500)

@view_config(route_name='inventory_list', request_method='GET')
def list_items_view(request):
    return inventory_list(request)

# 配置 Pyramid 应用
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # 创建库存管理实例
    inventory = InventoryManagement()

    # 添加视图
    config.add_route('inventory_add', '/inventory/add')
    config.add_view(add_item_view, route_name='inventory_add')
    config.add_route('inventory_remove', '/inventory/{item_id}/remove')
    config.add_view(remove_item_view, route_name='inventory_remove')
    config.add_route('inventory_update', '/inventory/update')
    config.add_view(update_item_view, route_name='inventory_update')
    config.add_route('inventory_get', '/inventory/{item_id}')
    config.add_view(get_item_view, route_name='inventory_get')
    config.add_route('inventory_list', '/inventory/list')
    config.add_view(list_items_view, route_name='inventory_list')

    # 扫描当前目录的视图
    config.scan()

    return config.make_wsgi_app()