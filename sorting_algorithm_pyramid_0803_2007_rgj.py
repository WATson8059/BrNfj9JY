# 代码生成时间: 2025-08-03 20:07:09
from pyramid.config import Configurator
from pyramid.view import view_config
import logging

# 设置日志记录器
log = logging.getLogger(__name__)

def bubble_sort(arr):
    # 冒泡排序算法实现
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(arr):
    # 选择排序算法实现
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

@view_config(route_name='sort', request_method='GET')
def sort_view(request):
    # 排序视图处理函数
    try:
        # 从请求参数获取要排序的数组
        arr = request.params.get('arr', '')
        if not arr:
            raise ValueError("Missing 'arr' parameter.")
        arr = [int(num) for num in arr.split(',')]
        
        # 默认使用冒泡排序
        sort_func = bubble_sort
        
        # 检查请求参数是否指定排序算法
        sort_algo = request.params.get('algo', 'bubble')
        if sort_algo == 'selection':
            sort_func = selection_sort
        
        # 执行排序并返回结果
        sorted_arr = sort_func(arr)
        return {'sorted_arr': sorted_arr}
    except ValueError as e:
        # 处理错误并返回错误信息
        log.error(f"Error occurred: {e}")
        raise

def main(global_config, **settings):
    """
    Pyramid WSGI 应用入口点。
    
    :param global_config: 全局配置字典
    :param settings: 应用设置字典
    """
    config = Configurator(settings=settings)
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    # 程序入口点
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    log.info('Server starting on http://0.0.0.0:6543')
    server.serve_forever()