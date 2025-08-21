# 代码生成时间: 2025-08-21 10:32:07
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import math
def calculate(request):
    """
    Handle POST request for mathematical operations.
    The request should contain 'operation' and 'numbers'
    where 'operation' is a string like 'add', 'subtract', etc.,
    and 'numbers' is a list of numbers to perform the operation on.
    """
    operation = request.json.get('operation')
    numbers = request.json.get('numbers')
    if not operation or not numbers:
        return Response('Invalid request', status=400)
    try:
        if operation == 'add':
            result = sum(numbers)
        elif operation == 'subtract':
            result = numbers[0] - sum(numbers[1:])
        elif operation == 'multiply':
            result = math.prod(numbers)
        elif operation == 'divide':
            if numbers[1] == 0:
                return Response('Cannot divide by zero', status=500)
            result = numbers[0] / numbers[1]
        else:
            return Response(f'Unsupported operation: {operation}', status=400)
        return Response(f'Result: {result}')
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)

@view_config(route_name='calculate', request_method='POST', renderer='json')
def calculate_view(context, request):
    """
    View function for handling POST requests to perform calculations.
    """
    return calculate(request)

def main(global_config, **settings):
    """
    This function sets up the Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('calculate', '/calculate')
    config.scan()
    return config.make_wsgi_app()
