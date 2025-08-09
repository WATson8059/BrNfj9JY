# 代码生成时间: 2025-08-09 10:14:04
#!/usr/bin/env python

"""
File Backup and Sync Tool using Python and Pyramid Framework
Author: [Your Name]
"""

import os
import shutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# Define a simple logger
def setup_logger():
    from logging import getLogger
    from logging import FileHandler
    from logging import Formatter
    from logging import DEBUG

    logger = getLogger(__name__)
    handler = FileHandler('backup_sync.log')
    handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    return logger

# Define the backup function
def backup_files(source_dir, backup_dir):
    """Backup files from source directory to backup directory"""
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(backup_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        return True
    except Exception as e:
        logger.error(f'Error backing up files: {e}')
        return False

# Define the sync function
def sync_files(source_dir, target_dir):
    """Sync files from source directory to target directory"""
    try:
        for root, dirs, files in os.walk(source_dir):
            for name in files:
                source_file = os.path.join(root, name)
                target_file = os.path.join(target_dir, os.path.relpath(source_file, source_dir))
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(source_file, target_file)
        return True
    except Exception as e:
        logger.error(f'Error syncing files: {e}')
        return False

# Pyramid route configuration
def main(global_config, **settings):
    """Main function to configure Pyramid application"""
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.scan()
    return config.make_wsgi_app()

# Pyramid views
@view_config(route_name='backup', renderer='json')
def backup_view(request):
    """View function to handle backup requests"""
    source_dir = request.params.get('source_dir')
    backup_dir = request.params.get('backup_dir')
    if not source_dir or not backup_dir:
        return {'error': 'Source and backup directories are required'}
    return {'success': backup_files(source_dir, backup_dir)}

@view_config(route_name='sync', renderer='json')
def sync_view(request):
    """View function to handle sync requests"""
    source_dir = request.params.get('source_dir')
    target_dir = request.params.get('target_dir')
    if not source_dir or not target_dir:
        return {'error': 'Source and target directories are required'}
    return {'success': sync_files(source_dir, target_dir)}

# Set up the logger
logger = setup_logger()

if __name__ == '__main__':
    logger.info('Starting the file backup and sync tool')
    main({})
