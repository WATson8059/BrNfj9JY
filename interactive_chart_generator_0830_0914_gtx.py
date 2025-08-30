# 代码生成时间: 2025-08-30 09:14:00
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
import json

# 定义一个视图函数来生成交互式图表
@view_config(route_name='generate_chart', request_method='GET')
def generate_chart(request):
    "