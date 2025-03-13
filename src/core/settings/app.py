from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request, jsonify

from core.db.db import setup_database_service, setup_database_service_sync
from core.settings import get_application_settings
import asyncio
settings = get_application_settings()

app=Flask(__name__)
POSTGRES={
    'user':'postgres',
    'pw':'EkQncsKEC27MQHVW',
    'db':'db_telehealth',
    'host':'localhost',
    'port':'5432'
}

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'%POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['REDIS_URL'] = settings.CELERY_BROKER_URL
db= SQLAlchemy(app)
migrate=Migrate(app,db)

app.config['SECRET_KEY'] = str(settings.SECRET_KEY)

setup_database_service_sync(settings)
asyncio.run(setup_database_service(settings))
