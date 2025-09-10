# 代码生成时间: 2025-09-10 18:34:12
from pyramid.config import Configurator
from pyramid.response import Response
import json

"""
A Pyramid application that acts as a JSON data formatter.
It takes JSON data as input and returns a formatted JSON response.
"""

def json_formatter(request):
    """
    A view function that takes JSON data from the request body,
    tries to parse it and returns a formatted JSON response.
    """
    try:
        # Attempt to parse the incoming JSON data from the request body
        data = json.loads(request.json_body)
        
        # Format the JSON data with indentation for better readability
        formatted_json = json.dumps(data, indent=4)
        
        # Return a JSON response with the formatted data
        return Response(formatted_json, content_type='application/json')
    except json.JSONDecodeError as e:
        # Return a JSON error response if the input is not valid JSON
        return Response(json.dumps({'error': 'Invalid JSON input', 'details': str(e)}), content_type='application/json', status=400)

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    It's the entry point of our application.
    """
    with Configurator(settings=settings) as config:
        # Add the 'json_formatter' view to the route '/'
        config.add_route('json_formatter', '/')
        config.add_view(json_formatter, route_name='json_formatter')
        
        # Scan for @view_config decorators and apply them
        config.scan()
        return config.make_wsgi_app()

if __name__ == '__main__':
    main({})