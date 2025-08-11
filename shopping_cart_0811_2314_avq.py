# 代码生成时间: 2025-08-11 23:14:32
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request
from pyramid.exceptions import NotFound
import json

"""
Shopping Cart application using Pyramid framework.
This application provides basic shopping cart functionality.
"""

# Define a simple in-memory 'database' to store cart items
# In a real-world scenario, you would use a database
cart_items = {}

"""
Decorator to handle JSON request and response.
This decorator sets the request and response content type to JSON.
"""
def json_request(response=None):
    def decorator(func):
        def wrapped_function(request, *arg, **kw):
            if request.method == 'POST':
                data = request.json_body
            else:
                data = {}
            result = func(request, data, *arg, **kw)
            if isinstance(result, str):
                resp = Response(result)
                resp.content_type = 'application/json'
                return resp
            elif isinstance(result, dict):
                return json.dumps(result)
            else:
                return result
        return wrapped_function
    return decorator

"""
View function to handle GET request to retrieve the shopping cart items.
"""
@json_request()
def get_cart(request, data):
    user_id = request.matchdict.get('user_id')
    if not user_id:
        return {'error': 'User ID is required'}
    cart = cart_items.get(user_id, [])
    return {'items': cart}

"""
View function to handle POST request to add an item to the shopping cart.
"""
@json_request()
def add_item(request, data):
    user_id = request.matchdict.get('user_id')
    item = data.get('item')
    if not user_id or not item:
        return {'error': 'User ID and item are required'}
    if user_id not in cart_items:
        cart_items[user_id] = []
    cart_items[user_id].append(item)
    return {'message': 'Item added to cart'}

"""
Main function to setup the Pyramid application.
"""
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('get_cart', '/cart/{user_id}')
    config.add_view(get_cart, route_name='get_cart', renderer='json')
    config.add_route('add_item', '/cart/{user_id}/add')
    config.add_view(add_item, route_name='add_item', renderer='json')
    return config.make_wsgi_app()
