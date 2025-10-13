# 代码生成时间: 2025-10-14 01:50:33
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.renderers import render_to_response
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 设置数据库信息
DB_URL = 'sqlite:///medical_equipment.db'

# 初始化数据库引擎
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 创建数据模型基类
Base = declarative_base()

# 定义医疗设备模型
class MedicalEquipment(Base):
    __tablename__ = 'medical_equipment'
    id = Column(Integer, Sequence('equipment_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow)

# 创建表
Base.metadata.create_all(engine)

# 医疗设备管理视图
class MedicalEquipmentViews:
    def __init__(self, request):
        self.request = request

    # 添加医疗设备
    @view_config(route_name='add_equipment', renderer='json')
    def add_equipment(self):
        data = self.request.json_body
        try:
            equipment = MedicalEquipment(
                name=data['name'],
                type=data['type'],
                quantity=data['quantity'],
                price=data['price']
            )
            session.add(equipment)
            session.commit()
            return {'status': 'success', 'message': 'Equipment added successfully'}
        except Exception as e:
            session.rollback()
            return {'status': 'error', 'message': str(e)}

    # 获取所有医疗设备
    @view_config(route_name='get_equipments', renderer='json')
    def get_equipments(self):
        try:
            equipments = session.query(MedicalEquipment).all()
            return [{'id': eq.id, 'name': eq.name, 'type': eq.type, 'quantity': eq.quantity, 'price': eq.price} for eq in equipments]
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # 更新医疗设备信息
    @view_config(route_name='update_equipment', renderer='json')
    def update_equipment(self):
        data = self.request.json_body
        try:
            equipment = session.query(MedicalEquipment).filter_by(id=data['id']).first()
            if equipment:
                equipment.name = data['name']
                equipment.type = data['type']
                equipment.quantity = data['quantity']
                equipment.price = data['price']
                session.commit()
                return {'status': 'success', 'message': 'Equipment updated successfully'}
            else:
                return {'status': 'error', 'message': 'Equipment not found'}
        except Exception as e:
            session.rollback()
            return {'status': 'error', 'message': str(e)}

    # 删除医疗设备
    @view_config(route_name='delete_equipment', renderer='json')
    def delete_equipment(self):
        data = self.request.json_body
        try:
            equipment = session.query(MedicalEquipment).filter_by(id=data['id']).first()
            if equipment:
                session.delete(equipment)
                session.commit()
                return {'status': 'success', 'message': 'Equipment deleted successfully'}
            else:
                return {'status': 'error', 'message': 'Equipment not found'}
        except Exception as e:
            session.rollback()
            return {'status': 'error', 'message': str(e)}

# 设置路由和视图
def main(global_config, **settings):
    """
    设置Pyramid应用的配置。
    """
    with Configurator(settings=settings) as config:
        # 添加视图
        config.add_route('add_equipment', '/add_equipment')
        config.add_view(MedicalEquipmentViews, attr='add_equipment', route_name='add_equipment')
        config.add_route('get_equipments', '/get_equipments')
        config.add_view(MedicalEquipmentViews, attr='get_equipments', route_name='get_equipments')
        config.add_route('update_equipment', '/update_equipment')
        config.add_view(MedicalEquipmentViews, attr='update_equipment', route_name='update_equipment')
        config.add_route('delete_equipment', '/delete_equipment')
        config.add_view(MedicalEquipmentViews, attr='delete_equipment', route_name='delete_equipment')

        # 捕获异常
        config.scan()

# 运行应用
if __name__ == '__main__':
    main({})
