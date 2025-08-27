# 代码生成时间: 2025-08-28 06:49:45
# test_data_generator.py
"""
This module provides a simple test data generator for Pyramid framework applications.
It generates test data for demonstration and testing purposes.
"""

import random
import string
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request

# Define a function to generate random test data
def generate_test_data():
    data = {
        'first_name': ''.join(random.choices(string.ascii_uppercase, k=5)),
        'last_name': ''.join(random.choices(string.ascii_uppercase, k=5)),
        'email': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com",
        'age': random.randint(18, 60),
        'username': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
        'password': ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%^&*()", k=12))
    }
    return data

# Pyramid view configuration
@view_config(route_name='generate_test_data', renderer='json')
def generate_test_data_view(request: Request):
    """
    View function to generate and return test data.
    Parameters:
    - request (Request): The Pyramid request object.
    Returns:
    - Response: A JSON response with the generated test data.
    """
    try:
        test_data = generate_test_data()
        return {'data': test_data}
    except Exception as e:
        return Response(
            json_body={'error': str(e)},
            status=500,
            content_type='application/json'
        )
