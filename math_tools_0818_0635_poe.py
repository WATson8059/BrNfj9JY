# 代码生成时间: 2025-08-18 06:35:39
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPInternalServerError
import math


# 定义数学工具集类
class MathTools(object):
    '''
    数学计算工具集
    提供基本的数学运算功能
    '''

    def add(self, a, b):
        """
        两个数相加
        :param a: 第一个数
        :param b: 第二个数
        :return: 两个数的和
        """
        return a + b

    def subtract(self, a, b):
        """
        两个数相减
        :param a: 第一个数
        :param b: 第二个数
        :return: 两个数的差
        """
        return a - b

    def multiply(self, a, b):
        """
        两个数相乘
        :param a: 第一个数
        :param b: 第二个数
        :return: 两个数的积
        """
        return a * b

    def divide(self, a, b):
        """
        两个数相除
        :param a: 第一个数
        :param b: 第二个数
        :return: 两个数的商
        :raises ValueError: 除数不能为0
        """
        if b == 0:
            raise ValueError('除数不能为0')
        return a / b

    def power(self, a, b):
        """
        幂运算
        :param a: 底数
        :param b: 指数
        :return: 幂运算的结果
        """
        return a ** b


# 定义视图函数
@view_config(route_name='add', renderer='json')
def add_view(request):
    try:
        a = float(request.params.get('a', 0))
        b = float(request.params.get('b', 0))
        result = MathTools().add(a, b)
        return {'result': result}
    except (ValueError, TypeError) as e:
        return HTTPInternalServerError(json_body={'error': str(e)})

@view_config(route_name='subtract', renderer='json')
def subtract_view(request):
    try:
        a = float(request.params.get('a', 0))
        b = float(request.params.get('b', 0))
        result = MathTools().subtract(a, b)
        return {'result': result}
    except (ValueError, TypeError) as e:
        return HTTPInternalServerError(json_body={'error': str(e)})

@view_config(route_name='multiply', renderer='json')
def multiply_view(request):
    try:
        a = float(request.params.get('a', 0))
        b = float(request.params.get('b', 0))
        result = MathTools().multiply(a, b)
        return {'result': result}
    except (ValueError, TypeError) as e:
        return HTTPInternalServerError(json_body={'error': str(e)})

@view_config(route_name='divide', renderer='json')
def divide_view(request):
    try:
        a = float(request.params.get('a', 0))
        b = float(request.params.get('b', 0))
        result = MathTools().divide(a, b)
        return {'result': result}
    except ValueError as e:
        return HTTPInternalServerError(json_body={'error': str(e)})

@view_config(route_name='power', renderer='json')
def power_view(request):
    try:
        a = float(request.params.get('a', 0))
        b = float(request.params.get('b', 0))
        result = MathTools().power(a, b)
        return {'result': result}
    except (ValueError, TypeError) as e:
        return HTTPInternalServerError(json_body={'error': str(e)})
