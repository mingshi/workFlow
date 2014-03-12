# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 10:27:01
FileName:   user.py
'''

from wf.db.db import Model
from sqlalchemy import Column, Integer, String, ForeignKey

class User(Model) :
    __tablename__ = 'user'
    id          =   Column(Integer, primary_key=True, autoincrement=True)
    uid         =   Column(Integer, unique=True)
    username    =   Column(String(50), unique=True)
    realname    =   Column(String(50))
    login_time  =   Column(String(19))
    login_ip    =   Column(String(15))
    role        =   Column(String(50), default='0')

    def __init__(self, uid, username, realname, login_time, login_ip) :
        self.uid        =   uid
        self.username   =   username
        self.realname   =   realname
        self.login_time =   login_time
        self.login_ip   =   login_ip

    def __repr__(self) :
        return '<User %r' % (self.username + ":" + self.realname + ":" + str(self.id) + ":" + str(self.uid) + ":" + self.role)


