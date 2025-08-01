# 代码生成时间: 2025-08-01 13:13:00
import os
import re

"""
A utility program to rename files in bulk using the Pyramid framework.
This program will be run as a standalone Python script.
"""


def rename_files(directory, pattern, replacement):
    """
    Rename files in the specified directory based on a regular expression pattern and replacement.

    :param directory: The directory path where files are located.
    :param pattern: A regular expression pattern to match file names.
    :param replacement: The string to replace the matched pattern.
    """
    for filename in os.listdir(directory):
        if re.search(pattern, filename):
            new_name = re.sub(pattern, replacement, filename)
            # Construct the full path to the file
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_name)
            # Check if the new name already exists to avoid file overwrite
            if not os.path.exists(new_file):
                try:
                    os.rename(old_file, new_file)
                    print(f"Renamed '{filename}' to '{new_name}'")
                except OSError as e:
                    print(f"Error renaming '{filename}': {e.strerror}")
            else:
                print(f"Skipped '{filename}': '{new_name}' already exists")
        else:
            print(f"No change for '{filename}'")


def main():
    "