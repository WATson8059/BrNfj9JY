# 代码生成时间: 2025-08-07 14:38:14
import os
from PIL import Image
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import Allow, Authenticated
from pyramid.security import DENY_ALL, ALL_PERMISSIONS

# 定义一个视图类，用于处理图片尺寸调整请求
class ImageResizer:
    def __init__(self, request):
        self.request = request

    # 视图方法，处理POST请求，调整图片尺寸
    @view_config(route_name='resize_image', request_method='POST', permission=Authenticated)
    def resize_image(self):
        # 获取请求中的图片文件
        file = self.request.POST['file'].file
        # 获取请求参数，指定新的图片尺寸
        new_width = int(self.request.params.get('width', 0))
        new_height = int(self.request.params.get('height', 0))

        # 检查新尺寸是否合法
        if new_width <= 0 or new_height <= 0:
            return Response('Invalid image dimensions', status=400)

        try:
            # 打开图片文件
            with Image.open(file) as img:
                # 调整图片尺寸
                resized_img = img.resize((new_width, new_height))

                # 保存调整后的图片
                output = BytesIO()
                resized_img.save(output, format=img.format)
                output.seek(0)

                # 返回调整后的图片内容
                return Response(output.read(), content_type='image/jpeg')
        except IOError:
            # 处理图片打开失败的错误
            return Response('Failed to open image file', status=500)

# Pyramid配置
def includeme(config):
    config.add_route('resize_image', '/resize_image')
    config.scan()

# Pyramid配置文件示例
# pyramids.ini
# [server:main]
# use = egg:gunicorn#gunicorn
# host = 0.0.0.0
# port = 6543

# [app:main]
# use = egg:myapp#myapp
# pyramid.reload_templates = true
