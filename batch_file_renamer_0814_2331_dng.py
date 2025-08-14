# 代码生成时间: 2025-08-14 23:31:13
import os
import re
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.settings import asbool

# 定义一个函数来格式化文件名
def format_filename(original_name, prefix, suffix, index):
    """
    Format the filename by adding a prefix, suffix and an index.
    
    :param original_name: The original filename without path.
    :param prefix: The prefix to be added to the filename.
    :param suffix: The suffix to be added to the filename.
    :param index: The index to be used in the filename.
    :return: The formatted filename.
    """
    return f"{prefix}{original_name}_{index}{suffix}"

# 定义一个函数来重命名文件
def rename_files_in_directory(directory, prefix, suffix, start_index=1):
    """
    Rename files in a given directory by adding a prefix and suffix with an index.
    
    :param directory: The directory path where files are located.
    :param prefix: The prefix to be added to the filenames.
    :param suffix: The suffix to be added to the filenames.
    :param start_index: The starting index for the filename numbering.
    :return: A list of renamed files.
    """
    renamed_files = []
    index = start_index
    for filename in os.listdir(directory):
        try:
            # Check if the file has a valid extension
            if not re.match(r'.*\.[^.]+$', filename):
                continue
            # Create the new filename
            new_filename = format_filename(filename, prefix, suffix, index)
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            # Add the renamed file to the list
            renamed_files.append(new_filename)
            index += 1
        except OSError as e:
            # Handle any OS related errors
            print(f"Error renaming file {filename} to {new_filename}: {e}")
    return renamed_files

# Pyramid view for renaming files
@view_config(route_name='rename_files', renderer='json')
def rename_files(request):
    """
    Pyramid view function to rename files in a directory.
    
    :param request: The Pyramid request object.
    :return: A JSON response with the list of renamed files.
    """
    directory = request.params.get('directory')
    prefix = request.params.get('prefix', '')
    suffix = request.params.get('suffix', '')
    start_index = int(request.params.get('start_index', 1))
    
    if not directory:
        return Response('{"errors":["No directory provided"]}', content_type='application/json')
    
    try:
        # Normalize the directory path
        directory = os.path.normpath(directory)
        # Check if the directory exists
        if not os.path.exists(directory):
            return Response('{"errors":["Directory does not exist"]}', content_type='application/json')
    except Exception as e:
        return Response(f'{{"errors":["{e}"]}}', content_type='application/json')
    
    renamed_files = rename_files_in_directory(directory, prefix, suffix, start_index)
    return Response({'renamed_files': renamed_files}, content_type='application/json')
