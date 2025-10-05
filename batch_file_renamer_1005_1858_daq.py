# 代码生成时间: 2025-10-05 18:58:45
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 定义批量文件重命名工具的主要类
class BatchFileRenamer:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    # 列出文件夹中的所有文件
    def list_files(self):
        return [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]

    # 重命名文件
    def rename_files(self, new_names):
        try:
            old_names = self.list_files()
            if len(old_names) != len(new_names):
                raise ValueError("The number of new names must match the number of old names.")
            for old_name, new_name in zip(old_names, new_names):
                os.rename(os.path.join(self.folder_path, old_name), os.path.join(self.folder_path, new_name))
            return True
        except Exception as e:
            return str(e)

# Pyramid视图函数用于接收请求并处理文件重命名
@view_config(route_name='rename', request_method='POST', renderer='json')
def rename_files(request):
    # 获取请求中的参数
    folder_path = request.params.get('folder_path')
    new_names = request.params.get('new_names')

    # 检查参数有效性
    if not folder_path or not new_names:
        return {"error": "Missing required parameters."}

    # 创建批量文件重命名工具实例
    renamer = BatchFileRenamer(folder_path)

    # 尝试重命名文件
    result = renamer.rename_files(new_names.split(','))

    # 返回结果
    if isinstance(result, bool):
        return {"success": "Files renamed successfully."}
    else:
        return {"error": result}

# Pyramid配置
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # 添加路由和视图
    config.add_route('rename', '/rename')
    config.scan()
    return config.make_wsgi_app()

# 运行应用程序
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 8080, app)
    print("Serving on http://0.0.0.0:8080")
    server.serve_forever()