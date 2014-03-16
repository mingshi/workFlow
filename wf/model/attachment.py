# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/16 17:38:32
FileName:   attachment.py
'''

from wf.db.db import Model
from sqlalchemy import Column, Integer, String, ForeignKey

class Attachment(Model) :
    __tablename__ = 'attachment'
    id      =   Column(Integer, primary_key=True, autoincrement=True)
    flow_id =   Column(Integer, default='0')
    path    =   Column(String(255), default='')
    create_user_id  =   Column(Integer, default='0')

    def __init__(self, flow_id, path, create_user_id) :
        self.flow_id    =   flow_id
        self.path       =   path
        self.create_user_id =   create_user_id

    def __repr__(self) :
        return '<Attachment %r' % (str(self.flow_id) + ":" + str(self.path) + ":" + str(self.create_user_id))

