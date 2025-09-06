# 代码生成时间: 2025-09-06 10:19:07
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from PIL import Image
import os
import requests
from io import BytesIO
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.security import Allow, AuthenticatedRole, Everyone, NO_PERMISSION_REQUIRED
from pyramid.authentication import AuthTktAuthenticationPolicy, CallbackAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.request import Request
from pyramid.session import SignedCookieSessionFactoryConfig
from pyramid.exceptions import ConfigurationError

# 配置 Pyramid 应用
with Configurator(
    authn_policy=CallbackAuthenticationPolicy(
        callback=lambda username, password, request: username == 'user' and password == 'pass'
    ),
    authz_policy=ACLAuthorizationPolicy(),
    session_factory=SignedCookieSessionFactoryConfig('secret')
) as config:
    # 设置 Pyramid 视图
    config.add_route('resize_images', '/resize_images')
    config.scan()


def resize_images(request):
    # 接收图片 URL
    image_url = request.matchdict['image_url']
    # 接收目标尺寸参数
    target_width = int(request.params.get('width', 0))
    target_height = int(request.params.get('height', 0))

    # 错误处理
    if not image_url or target_width == 0 or target_height == 0:
        raise HTTPBadRequest('Image URL and dimensions are required.')

    try:
        # 下载图片
        response = requests.get(image_url)
        response.raise_for_status()

        # 打开图片并调整尺寸
        image = Image.open(BytesIO(response.content))
        resized_image = image.resize((target_width, target_height))

        # 保存调整尺寸后的图片
        output_format = image.format or 'JPEG'
        output_buffer = BytesIO()
        resized_image.save(output_buffer, format=output_format)
        output_buffer.seek(0)

        # 返回调整尺寸后的图片
        return Response(
            output_buffer,
            headers=[('Content-Type', f'image/{output_format.lower()}')],
            request=request
        )
    except Exception as e:
        # 错误处理
        return Response(f'An error occurred: {e}', status=500)

# Pyramid 视图配置
@view_config(route_name='resize_images')
def view_resize_images(request):
    # 调用 resize_images 函数并渲染 HTML 模板
    return render_to_response(
        'resize_images.jinja2',
        {'image_url': request.matchdict['image_url'], 'target_width': request.params.get('width'), 'target_height': request.params.get('height')},
        request
    )
    
# 运行 Pyramid 应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from pyramid.paster import bootstrap

    config = Configurator()
    config.include('pyramid_chameleon.zpt')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()