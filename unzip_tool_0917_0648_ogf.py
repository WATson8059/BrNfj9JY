# 代码生成时间: 2025-09-17 06:48:32
from pyramid.config import Configurator
from pyramid.view import view_config
import zipfile
import os

class UnzipTool:
    """A utility class for unzipping files."""
    def __init__(self):
        pass

    def unzip(self, src, dest):
        """Unzips a zip file from the source path to the destination path.
        
        :param src: The path to the zip file
        :param dest: The destination directory where the files will be unzipped
        :return: True if successful, False otherwise
        """
        try:
            with zipfile.ZipFile(src, 'r') as zip_ref:
                zip_ref.extractall(dest)
            return True
        except zipfile.BadZipFile:
            # Handle the case where the file is not a zip file
            return False
        except FileNotFoundError:
            # Handle the case where the source file does not exist
            return False
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f"An error occurred: {e}")
            return False

@view_config(route_name='unzip', renderer='json')
def unzip_view(request):
    "