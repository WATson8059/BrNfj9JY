# 代码生成时间: 2025-09-05 10:18:27
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.request import Request
from pyramid.response import Response
from pyramid.security import Authenticated
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
import os

# Database configuration
DATABASE_URL = 'sqlite:///inventory.db'

# Create engine and bind it to a database
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Inventory Item model
class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

# Create all tables in the database
Base.metadata.create_all(engine)

# Session factory
Session = scoped_session(sessionmaker(bind=engine))

# Pyramid route setup
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('add_item', '/add')
    config.add_route('update_item', '/update/{id}')
    config.add_route('delete_item', '/delete/{id}')
    config.add_route('view_item', '/view/{id}')
    config.add_route('list_items', '/')
    config.scan()
    return config.make_wsgi_app()

# Views
@view_config(route_name='list_items', renderer='templates/list_items.pt')
def list_items(request: Request) -> dict:
    "