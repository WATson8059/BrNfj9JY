# 代码生成时间: 2025-09-03 12:29:50
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from datetime import datetime

# 数据库配置
DATABASE_URL = "sqlite:///example.db"  # 这里使用SQLite作为示例

# 创建SQLAlchemy Engine和Base
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# 定义关联表
association_table = Table(
    'association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    roles = relationship('Role', secondary=association_table, backref=backref('users'))

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship('User', secondary=association_table, backref=backref('roles'))

    def __repr__(self):
        return f"<Role(name={self.name})>"

# 初始化数据库
def init_db():
    Base.metadata.create_all(engine)

# 示例：添加用户和角色
def add_user_and_role():
    try:
        admin_role = session.query(Role).filter_by(name='Admin').first()
        if not admin_role:
            admin_role = Role(name='Admin')
            session.add(admin_role)
        session.commit()

        user = User(name='John Doe', email='john.doe@example.com')
        session.add(user)
        session.commit()

        user.roles.append(admin_role)
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception(f"An error occurred: {e}")

# 示例：查询用户及其角色
def query_user_with_roles(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            roles = [role.name for role in user.roles]
            return f"User {user.name} has roles: {roles}"
        else:
            return "User not found."
    except Exception as e:
        raise Exception(f"An error occurred during query: {e}")

# 调用初始化数据库函数
init_db()

# 调用添加用户和角色函数
add_user_and_role()

# 调用查询用户及其角色函数（示例）
# print(query_user_with_roles(1))
