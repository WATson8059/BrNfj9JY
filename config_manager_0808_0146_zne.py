# 代码生成时间: 2025-08-08 01:46:29
# config_manager.py

"""
配置文件管理器模块，用于加载、保存和更新金字塔框架的配置文件。
"""
from pyramid.config import Configurator
import json
from pyramid.exceptions import ConfigurationError



def load_config(config_path):
    """
    加载配置文件
    
    :param config_path: 配置文件的路径
    :return: 配置字典
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        raise ConfigurationError("配置文件未找到")
    except json.JSONDecodeError:
        raise ConfigurationError("配置文件格式错误")


def save_config(config_path, config):
    """
    保存配置文件
    
    :param config_path: 配置文件的路径
    :param config: 配置字典
    :return: None
    """
    try:
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        raise ConfigurationError(f"保存配置文件出错: {str(e)}")


def update_config(config_path, updates):
    """
    更新配置文件
    
    :param config_path: 配置文件的路径
    :param updates: 需要更新的配置项
    :return: 更新后的配置字典
    """
    try:
        with open(config_path, 'r+') as file:
            config = json.load(file)
            config.update(updates)
            file.seek(0)
            json.dump(config, file, indent=4)
            file.truncate()
            return config
    except FileNotFoundError:
        raise ConfigurationError("配置文件未找到")
    except json.JSONDecodeError:
        raise ConfigurationError("配置文件格式错误")
    except Exception as e:
        raise ConfigurationError(f"更新配置文件出错: {str(e)}")

# 示例用法
if __name__ == '__main__':
    configurator = Configurator()
    config_path = 'config.json'
    
    # 加载配置
    config = load_config(config_path)
    
    # 更新配置
    updates = {'new_key': 'new_value'}
    updated_config = update_config(config_path, updates)
    
    # 保存配置
    save_config(config_path, updated_config)