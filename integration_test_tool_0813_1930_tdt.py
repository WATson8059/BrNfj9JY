# 代码生成时间: 2025-08-13 19:30:46
# integration_test_tool.py

"""
Integration test tool for Pyramid framework applications.
This tool provides a simple way to run integration tests for a Pyramid application.
"""

from pyramid.config import Configurator
from pyramid.testing import DummyRequest
from webtest import TestApp

# Define a simple view function for demonstration purposes
def hello_world(request):
    """
    A simple view function that returns a 'Hello World' response.
    """
    return 'Hello World'

# Create a Pyramid configurator
config = Configurator(settings={})

# Add the view function to the configuration
config.add_route('hello', '/')
config.add_view(hello_world, route_name='hello')

# Create a WSGI application
app = config.make_wsgi_app()

# Create a TestApp for integration testing
test_app = TestApp(app)

# Define an integration test function
def test_hello_world():
    """
    Test the 'Hello World' view function.
    """
    # Create a dummy request to simulate a GET request to the '/' route
    request = DummyRequest()
    # Simulate the GET request using the TestApp
    response = test_app.get('/', status=200)
    # Check if the response body is 'Hello World'
    assert response.text == 'Hello World'

# Run the integration test
if __name__ == '__main__':
    test_hello_world()
