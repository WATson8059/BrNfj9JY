# 代码生成时间: 2025-09-04 10:36:36
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pyramid.events import NewRequest, NewResponse


# 创建数据库连接池管理器
class DBConnectionManager:
    def __init__(self, settings):
        # 从配置中获取数据库连接信息
        self.db_url = settings['sqlalchemy.url']
        # 创建数据库引擎，使用连接池
        self.engine = create_engine(self.db_url, pool_recycle=3600)
        # 为数据库引擎创建一个会话工厂
        Session = sessionmaker(bind=self.engine)
        # 使用scoped_session来确保每个请求有一个唯一的会话
        self.Session = scoped_session(Session)

    def open_session(self):
        """获取一个新的数据库会话。"""
        return self.Session()

    def close_session(self, session):
        """关闭数据库会话。"""
        session.close()

    def commit(self, session):
        """提交数据库会话中的所有更改。"""
        session.commit()

    def rollback(self, session):
        """回滚数据库会话中的所有更改。"""
        session.rollback()


# Pyramid事件处理器，用于在请求结束后关闭数据库会话。
def close_session_on_request_end(event):
    """在请求结束后关闭数据库会话。"""
    request = event.request
    session = getattr(request, 'db_session', None)
    if session:
        request.registry.db_manager.close_session(session)

# Pyramid配置函数
def main(global_config, **settings):
    config = Configurator(settings=settings)

    # 创建数据库连接池管理器
    db_manager = DBConnectionManager(settings)
    config.registry.db_manager = db_manager

    # 在请求开始时打开一个新的数据库会话
    config.add_subscriber(DBConnectionManager.open_session, NewRequest)
    # 在请求结束后关闭数据库会话
    config.add_subscriber(close_session_on_request_end, NewResponse)

    # 扫描视图并添加它们到配置中
    config.scan()
    return config.make_wsgi_app()


if __name__ == '__main__':
    # 运行程序，注意：需要提供正确的配置文件
    from wsgiref.simple_server import make_server
    from pyramid.paster import bootstrap

    settings = bootstrap('development.ini')
    app = main(settings)
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()