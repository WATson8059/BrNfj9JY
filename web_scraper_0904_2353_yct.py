# 代码生成时间: 2025-09-04 23:53:34
import requests
from bs4 import BeautifulSoup
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPClientError

"""
A Pyramid web application that serves as a web content scraper.
This scraper fetches the content of a webpage and returns it.
"""

# Define a function to fetch and parse web content
def fetch_web_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors
        return f"HTTP Error: {e}"
    except requests.exceptions.RequestException as e:
        # Handle other requests-related errors
        return f"Error: {e}"
    except Exception as e:
        # Handle other exceptions
        return f"An error occurred: {e}"

# Pyramid view configuration
@view_config(route_name='web_scraper', renderer='json')
def web_scraper_view(request):
    # Get the URL from the request parameters
    url = request.params.get('url')
    if not url:
        # If URL is not provided, return a client error
        raise HTTPClientError(detail="URL parameter is required")
    
    # Call the function to fetch and parse web content
    result = fetch_web_content(url)
    
    # Return the result as a JSON response
    return {'content': result}

# Pyramid main function to start the application
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    It's the entry point of the Pyramid application.
    """
    from pyramid.config import Configurator
    from pyramid.paster import bootstrap
    
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('web_scraper', '/web_scraper')
    config.scan()
    
    return config.make_wsgi_app()