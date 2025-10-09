# 代码生成时间: 2025-10-10 01:49:49
import psutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 系统性能监控工具
class SystemPerformanceMonitor:
    def __init__(self):
        pass

    # 获取CPU使用率
    def get_cpu_usage(self):
        """
        获取CPU使用率
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            return cpu_usage
        except Exception as e:
            # 错误处理
            print(f"Error getting CPU usage: {e}")
            return None

    # 获取内存使用情况
    def get_memory_usage(self):
        """
        获取内存使用情况
        """
        try:
            memory = psutil.virtual_memory()
            used_memory = memory.used / memory.total * 100
            return used_memory
        except Exception as e:
            # 错误处理
            print(f"Error getting memory usage: {e}")
            return None

    # 获取磁盘使用情况
    def get_disk_usage(self):
        """
        获取磁盘使用情况
        """
        try:
            disk_usage = psutil.disk_usage('/')
            used_disk = disk_usage.used / disk_usage.total * 100
            return used_disk
        except Exception as e:
            # 错误处理
            print(f"Error getting disk usage: {e}")
            return None

# Pyramid视图函数
@view_config(route_name='system_performance', renderer='json')
def system_performance(request):
    """
    Pyramid视图函数，返回系统性能监控数据
    """
    monitor = SystemPerformanceMonitor()
    cpu_usage = monitor.get_cpu_usage()
    memory_usage = monitor.get_memory_usage()
    disk_usage = monitor.get_disk_usage()

    data = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage
    }

    return data

# Pyramid配置
def main(global_config, **settings):
    """
    Pyramid配置函数
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')  # 支持Chameleon模板引擎
    config.add_route('system_performance', '/system-performance')
    config.scan()
    return config.make_wsgi_app()
