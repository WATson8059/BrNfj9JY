# 代码生成时间: 2025-08-15 12:35:55
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import pandas as pd
import numpy as np

# 数据清洗服务类
class DataCleaningService:
    """
    一个简单的数据清洗和预处理工具类。
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def handle_missing_values(self, strategy='drop'):
        """
        处理缺失值。
        :param strategy: 策略，可以是'drop'或'fill'。
        :return: 处理后的DataFrame。
        """
        if strategy == 'drop':
            return self.dataframe.dropna()
        elif strategy == 'fill':
            return self.dataframe.fillna(self.dataframe.mean())
        else:
            raise ValueError("Unsupported strategy. Use 'drop' or 'fill'.")

    def normalize_data(self):
        """
        对数据进行归一化处理。
        :return: 归一化后的DataFrame。
        """
        return (self.dataframe - self.dataframe.mean()) / self.dataframe.std()

    def encode_categorical_variables(self):
        """
        对分类变量进行编码。
        :return: 编码后的DataFrame。
        "