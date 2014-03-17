# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/16 12:25:47
FileName:   flow.py
'''

from wf.db.db import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Text

class Flow(Model) :
    __tablename__ = 'flow'
    id              =   Column(Integer, primary_key=True, autoincrement=True)
    f_type          =   Column(Integer, default='1')
    create_user_id  =   Column(Integer, default='0')
    create_user     =   Column(String(50), default='')
    department      =   Column(String(50), default='')
    phone           =   Column(String(20), default='')
    email           =   Column(String(50), default='')
    status          =   Column(Integer, default='0')
    detail          =   Column(Text())
    relation        =   Column(String(255), default='')
    end_time        =   Column(String(19), default='0000-00-00 00:00:00')
    subject         =   Column(String(255))
    des             =   Column(Text())
    create_time     =   Column(String(19))

    def __init__(self, f_type, create_user_id, create_user, department, phone, email, status, detail, relation, subject, des, end_time='0000-00-00 00:00:00') :
        self.f_type = f_type
        self.create_user_id = create_user_id
        self.create_user = create_user
        self.department = department
        self.phone = phone
        self.email = email
        self.status = status
        self.detail = detail
        self.relation = relation
        self.end_time = end_time
        self.subject = subject
        self.des = des

    def __repr__(self) :
        return '<Flow %r' % (unicode(self.f_type) + ":" + unicode(self.create_user_id) + ":" + unicode(self.create_user) + ":" + unicode(self.department) + ":" + unicode(self.phone) + ":" + unicode(self.email) + ":" + unicode(self.status) + ":" + unicode(self.detail) + ":" + unicode(self.relation) + ":" + unicode(self.end_time) + ":" + unicode(self.subject) + ":" + unicode(self.des) + ":" + unicode(self.create_time))
