# 代码生成时间: 2025-10-08 17:30:47
import os
import shutil
from datetime import datetime

# FolderOrganizer class to organize files in a directory
class FolderOrganizer:
    def __init__(self, directory):
        """Initialize the FolderOrganizer with a directory path."""
        self.directory = directory
        if not os.path.exists(directory):
            raise ValueError(f'The directory {directory} does not exist.')
        self.today = datetime.now().strftime('%Y-%m-%d')

    def organize(self):
        """Organize all files in the directory into subdirectories based on file type."""
        if not os.path.isdir(self.directory):
            raise NotADirectoryError(f'The path {self.directory} is not a directory.')

        # Create a list to hold file paths
        files_to_organize = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

        for file_path in files_to_organize:
            file_extension = os.path.splitext(file_path)[1]
            if file_extension:
                target_directory = os.path.join(self.directory, file_extension[1:].upper(), self.today)
                os.makedirs(target_directory, exist_ok=True)
                shutil.move(file_path, target_directory)

    def run(self):
        "