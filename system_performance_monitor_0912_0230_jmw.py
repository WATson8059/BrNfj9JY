# 代码生成时间: 2025-09-12 02:30:31
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from twisted.internet import reactor
import psutil
import json


# Define a custom exception for errors
class MonitoringError(Exception):
    pass


class SystemPerformanceMonitor:
    """Class to monitor system performance."""

    def __init__(self, config):
        self.config = config

    @view_config(route_name='monitor', renderer='json')
    def monitor(self):
        """Endpoint to get system performance metrics."""
        try:
            # Collect system performance metrics
            metrics = {
                'cpu': psutil.cpu_percent(),
                'memory': psutil.virtual_memory().percent,
                'disk': psutil.disk_usage('/').percent,
                'network': psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            }
            return metrics
        except Exception as e:
            # Handle any unexpected errors
            raise MonitoringError(f"An error occurred: {e}")


def includeme(config):
    """Include the system performance monitor."""
    config.scan()


if __name__ == '__main__':
    # Set up the Pyramid configuration
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.includeme(includeme)
        config.add_route('monitor', '/monitor')
        config.add_view(SystemPerformanceMonitor, route_name='monitor')
        app = config.make_wsgi_app()
        
    # Run the Pyramid application
    reactor.listenTCP(6543, app)
    reactor.run()
