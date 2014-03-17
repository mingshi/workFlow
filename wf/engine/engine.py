# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/16 18:15:11
FileName:   engine.py
'''

from flask import Blueprint, render_template, request, redirect, url_for, request, session, g, flash
from wf.db.db import db_session
import json
from wf.model import *
from wf import app
import time
from wf.util.auth import *
from pprint import pprint
from formValidate.loginForm import loginForm
from wf.util.libs import *
from sqlalchemy import or_, desc, func

class Engine :
    f_type = 1
    uid = 0
    fid = 0

    def __init__(self, f_type, uid, fid) :
        self.f_type = f_type
        self.uid = uid
        self.fid = fid

    def process(self) :
        # 先到step表查看是否存在
        activeStatus = [app.config['APPROVAL_OK'], app.config['APPROVAL_YET_OK']]
        if self.f_type == 1 :
            lastApproval = db_session.query(Step).filter(Step.approval_status.in_(activeStatus)).order_by(Step.create_time.desc()).first()
            if lastApproval :
                pass
            else :
                step_uid = session["'" + app.config['USER_INFO_HIGHER'] + "'"]
                step = 1
                approval_status = app.config['APPROVAL_NEW']
                approval_msg = ''
                user_from = 1
                user_step = 0
                
                step_user = get_multi_user_info_by_uid(step_uid)
                theUserInfo = json.loads(step_user)
                step_user = theUserInfo['info'][0]['realname']

                thisStep = Step(flow_id = self.fid, step = step, step_uid = step_uid, approval_status = approval_status, approval_msg = approval_msg, user_from = user_from, user_step = user_step, step_user = step_user)
                db_session.add(thisStep)
                db_session.commit()
                

