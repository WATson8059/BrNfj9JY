# 代码生成时间: 2025-10-13 18:25:22
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import logging

# 设置日志
logger = logging.getLogger(__name__)

# 定义智能家居控制类
class SmartHomeControl:
    def __init__(self):
        self.devices = {}  # 存储设备状态

    def turn_on(self, device_name):
        """ 打开设备 """
        if device_name in self.devices:
            self.devices[device_name] = True
            return f"{device_name} is turned on."
        else:
            return f"{device_name} not found."

    def turn_off(self, device_name):
        """ 关闭设备 """
        if device_name in self.devices:
            self.devices[device_name] = False
            return f"{device_name} is turned off."
        else:
            return f"{device_name} not found."

    def status(self, device_name):
        """ 获取设备状态 """
        if device_name in self.devices:
            return f"{device_name} is {'on' if self.devices[device_name] else 'off'}."
        else:
            return f"{device_name} not found."

# 创建智能家居控制实例
smart_home_control = SmartHomeControl()

# 配置 Pyramid 应用
def main(global_config, **settings):
    """ 配置 Pyramid 应用 """
    config = Configurator(settings=settings)

    # 添加视图和路由
    config.add_route('turn_on', '/turn_on/{device_name}')
    config.add_view(turn_on_view, route_name='turn_on')
    config.add_route('turn_off', '/turn_off/{device_name}')
    config.add_view(turn_off_view, route_name='turn_off')
    config.add_route('status', '/status/{device_name}')
    config.add_view(status_view, route_name='status')

    return config.make_wsgi_app()

# 定义视图函数
@view_config(route_name='turn_on', renderer='json')
def turn_on_view(request):
    device_name = request.matchdict['device_name']
    message = smart_home_control.turn_on(device_name)
    return {'message': message}

@view_config(route_name='turn_off', renderer='json')
def turn_off_view(request):
    device_name = request.matchdict['device_name']
    message = smart_home_control.turn_off(device_name)
    return {'message': message}

@view_config(route_name='status', renderer='json')
def status_view(request):
    device_name = request.matchdict['device_name']
    message = smart_home_control.status(device_name)
    return {'message': message}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = main({})
    app.registry.settings['pyramid.reload_templates'] = True
    from wsgiref.simple_server import make_server
    srv = make_server('0.0.0.0', 6543, app)
    srv.serve_forever()