# 代码生成时间: 2025-08-16 12:26:38
# inventory_management.py

"""
Inventory Management System using Pyramid Framework.
"""

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.renderers import render_to_response
import json

# Define a simple in-memory database for demonstration purposes
INVENTORY_DB = {
    'items': [
        {'id': 1, 'name': 'Apple', 'quantity': 100},
        {'id': 2, 'name': 'Banana', 'quantity': 150},
        {'id': 3, 'name': 'Cherry', 'quantity': 200},
    ]
}

def add_item(request):
    """
    Add a new item to the inventory.
    """
    data = request.json_body
    if not data or 'name' not in data or 'quantity' not in data:
        return HTTPBadRequest('Missing item details', comment='Provide item name and quantity')
    
    new_item = {'id': len(INVENTORY_DB['items']) + 1, 'name': data['name'], 'quantity': data['quantity']}
    INVENTORY_DB['items'].append(new_item)
    return Response(json.dumps(new_item), content_type='application/json')


def get_item(request):
    """
    Retrieve an item from the inventory by ID.
    """
    item_id = request.matchdict['id']
    item = next((item for item in INVENTORY_DB['items'] if item['id'] == int(item_id)), None)
    if item is None:
        return HTTPNotFound('Item not found')
    return Response(json.dumps(item), content_type='application/json')


def update_item(request):
    """
    Update an existing item in the inventory.
    """
    item_id = request.matchdict['id']
    item = next((item for item in INVENTORY_DB['items'] if item['id'] == int(item_id)), None)
    if item is None:
        return HTTPNotFound('Item not found')
    
    data = request.json_body
    if data:
        item['name'] = data.get('name', item['name'])
        item['quantity'] = data.get('quantity', item['quantity'])
    return Response(json.dumps(item), content_type='application/json')


def delete_item(request):
    """
    Delete an item from the inventory by ID.
    """
    item_id = request.matchdict['id']
    item = next((item for item in INVENTORY_DB['items'] if item['id'] == int(item_id)), None)
    if item is None:
        return HTTPNotFound('Item not found')
    INVENTORY_DB['items'] = [i for i in INVENTORY_DB['items'] if i['id'] != int(item_id)]
    return Response(json.dumps({'message': f'Item {item_id} deleted'}), content_type='application/json')

# Pyramid configuration
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('add_item', '/add_item')
    config.add_route('get_item', '/get_item/{id}')
    config.add_route('update_item', '/update_item/{id}')
    config.add_route('delete_item', '/delete_item/{id}')
    
    config.scan()
    return config.make_wsgi_app()

# Register the view functions with Pyramid
@view_config(route_name='add_item', renderer='json')
def view_add_item(request):
    return add_item(request)

@view_config(route_name='get_item', renderer='json')
def view_get_item(request):
    return get_item(request)

@view_config(route_name='update_item', renderer='json')
def view_update_item(request):
    return update_item(request)

@view_config(route_name='delete_item', renderer='json')
def view_delete_item(request):
    return delete_item(request)