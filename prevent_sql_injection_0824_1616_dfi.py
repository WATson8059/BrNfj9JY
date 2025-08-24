# 代码生成时间: 2025-08-24 16:16:34
from pyramid.config import Configurator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from pyramid.view import view_config
from pyramid.response import Response
import logging
from pyramid.security import remember, forget, authenticated_userid, Allow


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建数据库连接
DBAPI = 'postgresql'
USERNAME = 'your_username'
PASSWORD = 'your_password'
HOST = 'localhost'
DBNAME = 'your_db'
DATABASE_URL = f"{DBAPI}://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Pyramid配置
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.add_route('home', '/')
        config.add_route('prevent_injection', '/prevent_injection')
        config.scan()


# 定义模型基类
class BaseMixin:
    __abstract__ = True

    def as_dict(self):
        return self.__dict__


# 定义用户模型
class User(BaseMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))


# 定义视图
@view_config(route_name='prevent_injection', renderer='string')
def prevent_sql_injection(request):
    """防止SQL注入的视图函数"""
    session = Session()
    try:
        # 使用预编译语句防止SQL注入
        query = text("SELECT * FROM users WHERE name = :name")
        result = session.execute(query, {'name': 'Alice'})
        user = result.fetchone()

        if user:
            return f"User {user.name} found."
        else:
            return "No user found."
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return Response("An error occurred.", status=500)
    finally:
        session.close()


# 启动程序
if __name__ == '__main__':
    main()
