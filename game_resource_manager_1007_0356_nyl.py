# 代码生成时间: 2025-10-07 03:56:29
# game_resource_manager.py

"""
A Pyramid application for managing game resources.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.request import Request

# Define a simple game resource model
class GameResource:
    def __init__(self, id, name, quantity):
        self.id = id
        self.name = name
        self.quantity = quantity

# Define a resource manager to handle game resources
class ResourceManager:
    def __init__(self):
        self.resources = {}

    def add_resource(self, resource):
        if resource.id in self.resources:
            raise ValueError("Resource with the same ID already exists.")
        self.resources[resource.id] = resource

    def remove_resource(self, resource_id):
        if resource_id not in self.resources:
            raise KeyError("Resource not found.")
        del self.resources[resource_id]

    def update_resource(self, resource_id, new_name=None, new_quantity=None):
        if resource_id not in self.resources:
            raise KeyError("Resource not found.")
        if new_name:
            self.resources[resource_id].name = new_name
        if new_quantity:
            self.resources[resource_id].quantity = new_quantity

    def get_resource(self, resource_id):
        return self.resources.get(resource_id)

# Pyramid view functions
@view_config(route_name='add_resource', request_method='POST')
def add_resource_view(request: Request):
    try:
        resource_id = request.json['id']
        resource_name = request.json['name']
        resource_quantity = request.json['quantity']
        resource = GameResource(resource_id, resource_name, resource_quantity)
        request.context.resource_manager.add_resource(resource)
        return Response(json={"message": "Resource added successfully."})
    except KeyError as e:
        return Response(json={"error": str(e)}, status=400)
    except ValueError as e:
        return Response(json={"error": str(e)}, status=400)

@view_config(route_name='remove_resource', request_method='POST')
def remove_resource_view(request: Request):
    try:
        resource_id = request.json['id']
        request.context.resource_manager.remove_resource(resource_id)
        return Response(json={"message": "Resource removed successfully."})
    except KeyError as e:
        return Response(json={"error": str(e)}, status=400)

@view_config(route_name='update_resource', request_method='PUT')
def update_resource_view(request: Request):
    try:
        resource_id = request.json['id']
        new_name = request.json.get('name')
        new_quantity = request.json.get('quantity')
        request.context.resource_manager.update_resource(resource_id, new_name, new_quantity)
        return Response(json={"message": "Resource updated successfully."})
    except KeyError as e:
        return Response(json={"error": str(e)}, status=400)

@view_config(route_name='get_resource', request_method='GET')
def get_resource_view(request: Request):
    try:
        resource_id = request.matchdict['id']
        resource = request.context.resource_manager.get_resource(resource_id)
        if resource:
            return Response(json={"id": resource.id, "name": resource.name, "quantity": resource.quantity})
        else:
            return Response(json={"error": "Resource not found."}, status=404)
    except Exception as e:
        return Response(json={"error": str(e)}, status=500)

# Pyramid main function
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    
    # Create a resource manager instance and attach it to the request context
    resource_manager = ResourceManager()
    config.registry.resource_manager = resource_manager
    
    config.add_route('add_resource', '/add_resource')
    config.add_view(add_resource_view, route_name='add_resource')
    config.add_route('remove_resource', '/remove_resource')
    config.add_view(remove_resource_view, route_name='remove_resource')
    config.add_route('update_resource', '/update_resource')
    config.add_view(update_resource_view, route_name='update_resource')
    config.add_route('get_resource', '/get_resource/{id}')
    config.add_view(get_resource_view, route_name='get_resource')
    
    return config.make_wsgi_app()