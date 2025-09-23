# 代码生成时间: 2025-09-23 16:44:19
from pyramid.config import Configurator
from pyramid.response import Response
import json

"""
ConfigManager: A Pyramid application that manages configuration files.
"""


class ConfigManager:
    def __init__(self, config):
        self.config = config

    def load_config(self, filename):
        """
        Load a configuration file.
        
        :param filename: The name of the configuration file.
        :return: A dictionary containing the configuration data.
        :raises FileNotFoundError: If the file does not exist.
        :raises json.JSONDecodeError: If the file is not a valid JSON.
        """
        try:
            with open(filename, 'r') as file:
                config_data = json.load(file)
            return config_data
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{filename}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Configuration file '{filename}' is not a valid JSON.")

    def save_config(self, filename, config_data):
        """
        Save configuration data to a file.
        
        :param filename: The name of the configuration file.
        :param config_data: A dictionary containing the configuration data.
        :raises TypeError: If config_data is not a dictionary.
        """
        if not isinstance(config_data, dict):
            raise TypeError("config_data must be a dictionary.")
        try:
            with open(filename, 'w') as file:
                json.dump(config_data, file, indent=4)
        except Exception as e:
            raise IOError(f"Failed to write to file '{filename}': {e}")

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.set_root_factory('pyramid.renderers')
        config.add_route('load_config', '/config/load/*filename')
        config.add_view('load_config_view', route_name='load_config', renderer='json')
        config.add_route('save_config', '/config/save/*filename')
        config.add_view('save_config_view', route_name='save_config', renderer='json')

        app = config.make_wsgi_app()
        return app

def load_config_view(request):
    """
    Load a configuration file and return its contents.
    """
    filename = request.matchdict['filename']
    config_manager = ConfigManager(request.registry.settings)
    try:
        config_data = config_manager.load_config(filename)
        return {'status': 'success', 'config': config_data}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def save_config_view(request):
    """
    Save configuration data to a file.
    """
    filename = request.matchdict['filename']
    config_data = request.json_body
    config_manager = ConfigManager(request.registry.settings)
    try:
        config_manager.save_config(filename, config_data)
        return {'status': 'success', 'message': 'Configuration saved successfully.'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}