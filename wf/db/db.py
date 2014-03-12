# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 10:25:25
FileName:   db.py
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from wf import app

engine = create_engine(app.config['DB_URI'], encoding='utf8', pool_size=10, pool_recycle=5, echo_pool=True, convert_unicode=True,
        **app.config['DB_CONNECT_OPTIONS'])

db_session = scoped_session(sessionmaker(autoflush=False, autocommit=False, bind=engine))

Model = declarative_base(name="Model")

def init_db():
    Model.metadata.create_all(bind=engine)

