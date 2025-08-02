# 代码生成时间: 2025-08-02 17:48:30
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.request import Request
import os
import mimetypes
from docx2txt import docx2txt
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

# 文档转换器视图函数
@view_config(route_name='convert_document', renderer='json')
def convert_document(request: Request):
    # 获取上传的文件
    file = request.POST['file']
    if not file:
        return {'error': 'No file provided'}

    try:
        # 获取文件名和文件扩展名
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()

        # 支持的文档格式
        supported_formats = ('.docx',)

        # 检查文件格式是否支持
        if ext not in supported_formats:
            return {'error': 'Unsupported file format'}

        # 文档转换
        converted_text = convert_document_to_text(file)

        # 返回转换结果
        return {'message': 'Document converted successfully', 'content': converted_text}
    except Exception as e:
        # 错误处理
        logging.error(f'Error converting document: {str(e)}')
        return {'error': 'Error converting document'}

# 转换文档到文本
def convert_document_to_text(file):
    # 读取文件内容
    file_content = file.file.read()

    # 使用docx2txt库转换文档
    return docx2txt(file_content)

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()

# 路由配置
def includeme(config):
    config.add_route('convert_document', '/document/convert')
    config.scan()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    logging.info('Serving on http://localhost:6543')
    server.serve_forever()