# 代码生成时间: 2025-09-08 17:01:21
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import os
from docx import Document
from docx.shared import Inches
import zipfile

"""
Document Converter Pyramid Application.

This application allows users to convert a Microsoft Word document (.docx)
into a plain text file.
"""


# Define a route and view for converting documents
@view_config(route_name='convert', renderer='json')
def convert_document(request):
    # Check if the document is uploaded
    if 'document' not in request.POST:
        return {'error': 'No document provided.'}

    # Retrieve the uploaded file
    doc_file = request.POST['document'].file

    # Check the file extension
    if not doc_file.filename.endswith('.docx'):
        return {'error': 'Only .docx files are accepted.'}

    # Create a temporary directory to store the document
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    temp_file_path = os.path.join(temp_dir, doc_file.filename)
    doc_file.save(temp_file_path)

    try:
        # Convert the document to plain text
        document = Document(temp_file_path)
        plain_text = ''
        for paragraph in document.paragraphs:
            plain_text += paragraph.text + '
'

        # Remove the temporary file
        os.remove(temp_file_path)

        # Return the plain text
        return {'plain_text': plain_text}
    except Exception as e:
        # Remove the temporary file on error
        os.remove(temp_file_path)
        return {'error': str(e)}

# Configure the Pyramid application
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('convert', '/convert')
    config.scan()
    return config.make_wsgi_app()
