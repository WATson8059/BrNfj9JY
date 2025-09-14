# 代码生成时间: 2025-09-15 07:34:14
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO)

# 定义定时任务
def timed_task():
    logging.info('定时任务执行')

# 应用配置
def main(global_config, **settings):
    config = Configurator(settings=settings)

    # 设置定时任务调度器
    scheduler = BackgroundScheduler()
    scheduler.add_job(timed_task, 'interval', seconds=10)  # 每10秒执行一次
    scheduler.start()

    # 定义视图
    @view_config(route_name='home', renderer='json')
    def home(request):
        return {'message': '定时任务调度器运行中'}

    # 添加视图
    config.add_route('home', '/')
    config.scan()

    # 配置应用
    return config.make_wsgi_app()
