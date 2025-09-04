# 代码生成时间: 2025-09-04 15:04:05
# image_resizer.py

"""
An image resizer application using the PYRAMID framework.
This application allows users to batch resize images.
"""

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.request import Request
from PIL import Image
import os
import io

# Define a constant for image upload directory
UPLOAD_FOLDER = '/path/to/upload/folder'

# Define a constant for image allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Check if the file is an allowed extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request: Request):
    """
    The index view for the application.
    """
    return {}

@view_config(route_name='upload', renderer='json')
def upload(request: Request):
    """
    Handle file uploads and resize images.
    """
    file = request.POST['file']
    if file.filename and allowed_file(file.filename):
        try:
            # Open the image
            img = Image.open(file.file)
            # Resize the image
            img = img.resize((800, 600))
            # Save the resized image
            img.save(os.path.join(UPLOAD_FOLDER, file.filename))
            return {'success': True, 'message': 'Image uploaded and resized successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    else:
        return {'success': False, 'message': 'Invalid file type'}

# Initialize the Pyramid application
def main(global_config, **settings):
    """
    Pyramid main function to setup the application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('index', '/')
    config.add_route('upload', '/upload')
    config.scan()
    return config.make_wsgi_app()
