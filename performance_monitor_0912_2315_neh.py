# 代码生成时间: 2025-09-12 23:15:36
import os
import psutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 性能监控工具类
class SystemPerformanceMonitor:
    def __init__(self):
        pass

    # 获取CPU使用率
    def get_cpu_usage(self):
        """
        返回CPU使用率（百分比）
        """
        return psutil.cpu_percent()

    # 获取内存使用情况
    def get_memory_usage(self):
        """
        返回内存使用信息（包括总量、已用、可用、使用率）
        """
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'used': mem.used,
            'available': mem.available,
            'percent': mem.percent
        }

    # 获取磁盘使用情况
    def get_disk_usage(self, path='/'):
        """
        返回指定路径的磁盘使用情况
        :param path: 路径
        """
        disk_usage = psutil.disk_usage(path)
        return {
            'total': disk_usage.total,
            'used': disk_usage.used,
            'available': disk_usage.free,
            'percent': disk_usage.percent
        }

# Pyramid视图函数
@view_config(route_name='cpu_usage', renderer='json')
def cpu_usage(request):
    """
    返回CPU使用率
    """
    monitor = SystemPerformanceMonitor()
    try:
        cpu_usage = monitor.get_cpu_usage()
        return {'cpu_usage': cpu_usage}
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

@view_config(route_name='memory_usage', renderer='json')
def memory_usage(request):
    """
    返回内存使用情况
    """
    monitor = SystemPerformanceMonitor()
    try:
        memory_usage = monitor.get_memory_usage()
        return memory_usage
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

@view_config(route_name='disk_usage', renderer='json')
def disk_usage(request):
    """
    返回磁盘使用情况
    :param path: 路径
    """
    monitor = SystemPerformanceMonitor()
    path = request.matchdict.get('path', '/')
    try:
        disk_usage = monitor.get_disk_usage(path)
        return disk_usage
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

# Pyramid配置函数
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('cpu_usage', '/cpu_usage')
    config.add_route('memory_usage', '/memory_usage')
    config.add_route('disk_usage', '/disk_usage/{path}')
    config.scan()
    return config.make_wsgi_app()