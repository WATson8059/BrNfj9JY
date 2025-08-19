# 代码生成时间: 2025-08-19 19:40:41
import os
from PIL import Image
from pyramid.view import view_config
from pyramid.response import Response

# Define a view to handle the image resizing
@view_config(route_name='image_resize', renderer='json')
def image_resize(request):
    # Retrieve the target path and new size from request parameters
    target_path = request.params.get('target_path')
    new_size = request.params.get('new_size')
    
    # Validate input parameters
    if not target_path or not new_size:
        return Response(json_body={'error': 'Missing target path or new size'}, status=400)
    
    try:
        # Parse the new size
        new_size = tuple(map(int, new_size.split('x')))
    except ValueError:
        return Response(json_body={'error': 'Invalid size format. Use 