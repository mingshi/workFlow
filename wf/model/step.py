# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/17 10:04:18
FileName:   step.py
'''

from wf.db.db import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Text

class Step(Model) :
    __tablename__ = 'step'
    id              =   Column(Integer, primary_key=True, autoincrement=True)
    flow_id         =   Column(Integer, default='0')
    step            =   Column(Integer, default='1')
    step_uid        =   Column(Integer, default='0')
    approval_status =   Column(Integer, default='1')
    approval_msg    =   Column(Text())
    user_from       =   Column(Integer, default='1')
    user_step       =   Column(Integer, default='0')
    create_time     =   Column(String(19))
    step_user       =   Column(String(255))
    update_time     =   Column(String(19))

    def __init__(self, flow_id, step, step_uid, approval_status, approval_msg, user_from, user_step, step_user) :
        self.flow_id            =   flow_id
        self.step               =   step
        self.step_uid           =   step_uid
        self.approval_status    =   approval_status
        self.approval_msg       =   approval_msg
        self.user_from          =   user_from
        self.user_step          =   user_step
        self.step_user          =   step_user

    def __repr__(self) :
        return '<Step %r' % (unicode(self.flow_id) + ":" + unicode(self.step) + ":" + unicode(self.step_uid) + ":" + unicode(self.approval_status) + ":" + unicode(self.approval_msg) + ":" + unicode(self.user_from) + ":" + unicode(self.user_step) + ":" + unicode(self.step_user) + ":" + unicode(self.update_time))

