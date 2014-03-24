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
from sqlalchemy import or_, desc, func, and_

class Engine :
    f_type = 1
    uid = 0
    fid = 0

    def __init__(self, f_type, uid, fid) :
        self.f_type = f_type
        self.uid = uid
        self.fid = fid
        self.flag = False

    def process(self) :
        # 先到step表查看是否存在
        activeStatus = [app.config['APPROVAL_OK'], app.config['APPROVAL_YET_OK'], app.config['APPROVAL_TURN']]
        lastApproval = db_session.query(Step).filter(and_(Step.approval_status.in_(activeStatus), Step.flow_id == self.fid, Step.is_add_turn != app.config['IS_ADD_TURN'])).order_by(Step.create_time.desc()).first()
        if lastApproval :
            #检查是否已经在config文件读取
            tmpApproval = db_session.query(Step).filter(Step.flow_id == self.fid).order_by(Step.create_time.desc()).first()
            
            if tmpApproval.user_from == app.config['USER_FROM_CONFIG'] :
                nextKey = tmpApproval.user_step + 1
                step = tmpApproval.step + 1
                step_uid = app.config['WORK_FLOW'][self.f_type]['uid'][nextKey]
                approval_msg = ''
                if not app.config['WORK_FLOW'][self.f_type]['can'][nextKey] == 'ceo' :
                    approval_status = app.config['APPROVAL_NEW']
                    approval_msg = ''
                else :
                    #回头改
                    approval_status = app.config['APPROVAL_NEW']
               
                if 'approval_status' in request.form :
                    tmpApproval.approval_status = request.form['approval_status']
                else :
                    tmpApproval.approval_status = app.config['APPROVAL_OK']
                tmpApproval.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                db_session.commit()
                
                user_from = app.config['USER_FROM_CONFIG']
                user_step = nextKey
                stepUser = get_multi_user_info_by_uid(step_uid)
                tmpInfo = json.loads(stepUser)
                step_user = tmpInfo['info'][0]['realname']

                thisStep = Step(flow_id = self.fid, step = step, step_uid = step_uid, approval_status = approval_status, approval_msg = approval_msg, user_from = user_from, user_step = user_step, step_user = step_user)
                db_session.add(thisStep)
                db_session.commit()

            else :
                lastUid = lastApproval.step_uid
                
                # 检查上一个是不是加签或者转签
                step = lastApproval.step + 1
                approval_status = app.config['APPROVAL_NEW']
                user_from = app.config['USER_FROM_DB']
                user_step = lastApproval.user_step + 1
                
                flow = db_session.query(Flow).filter_by(id = self.fid).first()
                flow_detail = json.loads(flow.detail)
                pay_cost = flow_detail['pay_cost']

                res = get_multi_user_info_by_uid(lastUid)
                res_info = json.loads(res)
                step_uid = 0
                approval_msg = ''
                step_user = ''
                if res_info['msg'] == "success" and res_info['status'] == 'ok' and not res_info['info'][0]['higher'] == 0 :
                    step_uid = res_info['info'][0]['higher']
                    newRes = get_multi_user_info_by_uid(step_uid)
                    newResInfo = json.loads(newRes)
                    if newResInfo['msg'] == 'success' and newResInfo['status'] == 'ok' :
                        step_user = newResInfo['info'][0]['realname']
               
                if pay_cost >= app.config['MONEY_LINE'] and self.f_type == 1 :
                    if res_info['info'][0]['higher'] == 0 :
                        self.flag = True
                else :
                    if res_info['info'][0]['higher'] == 0 :
                        self.flag = True                      
                
                if self.flag :
                    # 要到配置文件去读取流程配置了
                    flowConfig = app.config['WORK_FLOW'][self.f_type]
                    step_uid = flowConfig['uid'][0]
                    if step_uid == 'flow_uid' :
                        step_uid = flow.create_user_id
                        step_user = flow.create_user
                    else : 
                        step_user = get_multi_user_info_by_uid(step_uid)
                        step_user = json.loads(step_user)
                        step_user = step_user['info'][0]['realname']

                    approval_status = app.config['APPROVAL_NEW']
                    approval_msg = ''
                    user_from = app.config['USER_FROM_CONFIG']
                    user_step = 0
                    thisStep = Step(flow_id = self.fid, step = step, step_uid = step_uid, approval_status = approval_status, approval_msg = approval_msg, user_from = user_from, user_step = user_step, step_user = step_user)
                    db_session.add(thisStep)
                    db_session.commit()

                else :
                    thisStep = Step(flow_id = self.fid, step = step, step_uid = step_uid, approval_status = approval_status, approval_msg = approval_msg, user_from = user_from, user_step = user_step, step_user = step_user)
                    db_session.add(thisStep)
                    db_session.commit()

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
