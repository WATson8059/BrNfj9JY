# 代码生成时间: 2025-09-21 11:55:57
import os
import glob
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.request import Request
from pyramid.session import *

# 定义全局配置字典
settings = {
    'reload_all': True,  # 开发时自动重载应用
}

# 定义错误处理视图
@view_config(context=Exception, renderer="json")
def error_view(exc, request):  # 错误处理函数
    return {"error": exc.message, "traceback": exc.traceback}


# 定义批量重命名视图
@view_config(route_name='batch_rename', renderer="json")
def batch_rename_view(request: Request) -> dict:  # 批量重命名视图函数
    # 获取请求数据，包含文件路径和新文件名模式
    path = request.matchdict.get('path')
    new_pattern = request.matchdict.get('new_pattern')
    
    try:  # 尝试执行批量重命名
        if not path or not new_pattern:  # 检查参数是否完整
            raise ValueError("Both 'path' and 'new_pattern' are required.")
        
        files = glob.glob(os.path.join(path, "*"))  # 获取文件列表
        renamed_files = []
        
        for count, file_path in enumerate(files, start=1):  # 枚举文件
            file_name = os.path.basename(file_path)  # 获取文件名
            new_name = f"{new_pattern}{count}{os.path.splitext(file_name)[1]}"  # 生成新文件名
            new_path = os.path.join(path, new_name)  # 构造新文件路径
            os.rename(file_path, new_path)  # 重命名文件
            renamed_files.append(new_name)  # 添加到重命名列表
        
        return {"renamed_files": renamed_files}  # 返回重命名结果
    except Exception as e:  # 捕获并处理异常
        return {"error": str(e)}

# 应用配置
def main(global_config, **settings):  # 主函数
    with Configurator(settings=settings) as config:  # 配置环境
        config.include('.pyramid_route')  # 包括路由配置
        config.scan()  # 扫描当前目录下的视图函数
        config.add_route('batch_rename', 'batch_rename/{path}/{new_pattern}')  # 添加路由
        config.add_view(batch_rename_view, route_name='batch_rename')  # 添加视图
        return config.make_wsgi_app()  # 返回WSGI应用

if __name__ == "__main__":  # 程序入口
    main({})  # 启动应用