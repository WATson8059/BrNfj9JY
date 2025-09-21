# 代码生成时间: 2025-09-22 05:06:01
from pyramid.config import Configurator
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.scan()
    return config.make_wsgi_app()

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from pyramid.paster import bootstrap, setup_logging
from pyramid.scripts.common import parse_options
from pyramid.threadlocal import get_current_registry

# Database configuration
DATABASE_URL = 'postgresql://username:password@host:port/dbname'
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

# Scheduler configuration
scheduler = BackgroundScheduler(executors=[ThreadPoolExecutor(20)])

# Job store configuration
class JobStoreSession(Session):
    """ Custom session class for job store. """
    pass

# Register job store
scheduler.add_jobstore(JobStoreSession, alias='default')

# Define jobs
def job1():
    """ Execute job 1. """
    print("Executing job 1 at: ", datetime.now())
    Session.execute(text("INSERT INTO jobs (name) VALUES ('job1')"))
    Session.commit()

def job2():
    """ Execute job 2. "