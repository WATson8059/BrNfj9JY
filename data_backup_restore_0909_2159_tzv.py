# 代码生成时间: 2025-09-09 21:59:19
import os
import shutil
import tempfile
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 数据备份恢复类
class DataBackupRestore:
    def __init__(self, backup_directory, data_directory):
        self.backup_directory = backup_directory
        self.data_directory = data_directory

    def backup_data(self):
        """备份数据目录"""
        try:
            backup_path = os.path.join(self.backup_directory, 'data_backup.zip')
            with tempfile.NamedTemporaryFile(suffix='.zip') as tmp_file:
                shutil.make_archive(tmp_file.name, 'zip', self.data_directory)
                shutil.move(tmp_file.name + '.zip', backup_path)
                return Response('Data backup successful.')
        except Exception as e:
            return Response(f'Error during backup: {e}', status=500)

    def restore_data(self, backup_file):
        """从备份文件恢复数据"""
        try:
            backup_path = os.path.join(self.backup_directory, backup_file)
            with tempfile.NamedTemporaryFile() as tmp_file:
                shutil.copy(backup_path, tmp_file.name)
                shutil.unpack_archive(tmp_file.name, self.data_directory, 'zip')
                return Response('Data restore successful.')
        except Exception as e:
            return Response(f'Error during restore: {e}', status=500)

# Pyramid视图配置
@view_config(route_name='backup', request_method='POST')
def backup_view(request):
    "