# 代码生成时间: 2025-10-01 02:24:34
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

# 数据库模型（假设使用SQLAlchemy）
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(DateTime)
    # 其他病人信息字段...

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    diagnosis = Column(String)
    prescription = Column(String)
    record_date = Column(DateTime)
    # 其他记录信息字段...

# 数据库配置
DATABASE_URL = 'sqlite:///:memory:'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Pyramid视图函数
@view_config(route_name='home', renderer='json')
def home_view(request):
    session = Session()
    try:
        patients = session.query(Patient).all()
        return {'patients': [patient.name for patient in patients]}
    except Exception as e:
        logging.error(f'Error fetching patients: {e}')
        return Response(json.dumps({'error': 'Internal server error'}), content_type='application/json', status=500)
    finally:
        session.close()

@view_config(route_name='patient', renderer='json')
def patient_view(request):
    session = Session()
    try:
        patient_id = request.matchdict['id']
        patient = session.query(Patient).filter(Patient.id == patient_id).one()
        records = session.query(Record).filter(Record.patient_id == patient_id).all()
        return {'patient': patient.name, 'records': [{'diagnosis': record.diagnosis, 'prescription': record.prescription} for record in records]}
    except Exception as e:
        logging.error(f'Error fetching patient {patient_id}: {e}')
        return Response(json.dumps({'error': 'Internal server error'}), content_type='application/json', status=500)
    finally:
        session.close()

@view_config(route_name='add_record', request_method='POST', renderer='json')
def add_record_view(request):
    session = Session()
    try:
        data = json.loads(request.body)
        patient_id = data['patient_id']
        diagnosis = data['diagnosis']
        prescription = data['prescription']
        record = Record(patient_id=patient_id, diagnosis=diagnosis, prescription=prescription, record_date=datetime.datetime.now())
        session.add(record)
        session.commit()
        return {'message': 'Record added successfully'}
    except Exception as e:
        logging.error(f'Error adding record: {e}')
        return Response(json.dumps({'error': 'Internal server error'}), content_type='application/json', status=500)
    finally:
        session.close()

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('patient', '/patient/{id}')
    config.add_route('add_record', '/add_record')
    config.scan()
    return config.make_wsgi_app()
