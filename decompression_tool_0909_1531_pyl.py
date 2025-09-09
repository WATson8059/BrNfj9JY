# 代码生成时间: 2025-09-09 15:31:54
# decompression_tool.py
# A Pyramid web application that serves as a file decompression tool.

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import zipfile
import tarfile
import shutil
import os

"""
This module provides a simple web application for decompressing files.
It can handle zip and tar.gz archives and extract them into a specified directory.
"""

# Configuration for the Pyramid app
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('decompress', '/decompress')
    config.scan()
    return config.make_wsgi_app()


# Decompression view function
@view_config(route_name='decompress', renderer='json', request_method='POST')
def decompress_file(request):
    """
    Decompresses a file sent to the server.
    The request should have a multipart/form-data content type
    with a file part named 'file'.
    """
    try:
        # Get the uploaded file from the request
        file_data = request.params['file'].file
        filename = request.params['file'].filename

        # Define the extraction directory
        extraction_path = 'extracted_files'
        os.makedirs(extraction_path, exist_ok=True)

        # Check the file type and call the appropriate decompression function
        if filename.endswith('.zip'):
            extract_zip(file_data, extraction_path)
        elif filename.endswith('.tar.gz') or filename.endswith('.tgz'):
            extract_tar_gz(file_data, extraction_path)
        else:
            return {'error': 'Unsupported file type'}

        # Return a success message
        return {'message': 'File decompressed successfully'}
    except Exception as e:
        # Handle any errors that occur during the process
        return {'error': str(e)}


def extract_zip(file_data, extraction_path):
    """
    Extracts a zip archive to the specified extraction path.
    """
    with zipfile.ZipFile(file_data, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)


def extract_tar_gz(file_data, extraction_path):
    """
    Extracts a tar.gz archive to the specified extraction path.
    """
    with tarfile.open(fileobj=file_data, mode='r:gz') as tar_ref:
        tar_ref.extractall(extraction_path)


def includeme(config):
    """
    Pyramid includeme function to setup the decompression tool.
    """
    config.add_route('decompress', '/decompress')
    config.scan('.decompression_tool')
