# 代码生成时间: 2025-08-04 07:48:35
import urllib.parse
from pyramid.view import view_config
from pyramid.request import Request
def is_valid_url(url: str) -> bool:
    # 尝试解析URL，如果抛出ValueError，则URL无效
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def check_url(request: Request) -> str:
    # 获取URL参数
    url = request.params.get('url')
    if not url:
        # 如果没有提供URL参数，返回错误信息
        return "Error: URL parameter is missing."
    # 验证URL是否有效
    if is_valid_url(url):
        return f"URL '{url}' is valid."
    else:
        return f"URL '{url}' is invalid."

def includeme(config):
    # 配置路由，将URL参数传递给check_url函数
    config.add_route('validate_url', '/validate_url')
    config.add_view(check_url, route_name='validate_url', request_method='GET', renderer='string')

# 配置文件可以如下定义：
# with open('development.ini', 'w') as f:
#     f.write("""
# [server:main]
# use = egg:waitress#main
# listen = 0.0.0.0:6543

# [app:main]
# use = egg:{{filename.split('.')[0]}}
# full_stack = true

# [loggers]
# keys = root

# [handlers]
# keys = console

# [formatters]
# keys = generic

# [logger_root]
# level = INFO
# handlers = console

# [handler_console]
# class = StreamHandler
# args = (sys.stderr,)
# level = NOTSET
# formatter = generic

# [formatter_generic]
# format = %(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s
# datefmt = %H:%M:%S
# """)