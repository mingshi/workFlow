# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/17 15:23:45
FileName:   approval.py
'''

from flask import Blueprint, render_template, request, url_for, redirect, session, g, jsonify
from wf import app
from wf.db.db import db_session
from wf.model import *
from wf.util.auth import *
from sqlalchemy import or_, and_, desc 
import md5
import json
from flask.ext.sqlalchemy import Pagination
import math
from wf.util.libs import *
from datetime import date
import os
import time
import datetime
from wf.engine.engine import Engine
from decimal import Decimal
from formValidate.approval import Approval
import time
from formValidate.testApproval import testApproval

mod = Blueprint('approval', __name__)

@mod.route('/approval/<f_type>/<id>', methods=['GET', 'POST'])
def approval_flow(f_type, id) :
    form = Approval()
    fType = int(f_type)
    fid = int(id)

    flow = db_session.query(Flow).filter_by(id = fid).first()
    
    if not flow :
        flash_error('没有该流程')
        return redirect('/flow/add')

    temp = get_approval_temp(f_type)

    flowDetail = json.loads(flow.detail)

    attachments = db_session.query(Attachment).filter_by(flow_id = fid).all()

    atts = []
    for attachment in attachments :
        atts.append(app.config['ATTACHEMENT_PATH'] + "/" + attachment.path)

    # 获取审批记录
    approval_logs = db_session.query(Step).filter(and_(Step.flow_id == fid, Step.approval_status != app.config['APPROVAL_NEW'])).order_by(Step.update_time.desc()).all()

    logsNum = len(approval_logs)
    
    nowApproval = db_session.query(Step).filter(Step.flow_id == fid).order_by(Step.update_time.desc()).first()

    if request.method == "POST" :
        is_ajax = request.form['is_ajax']
        if form.validate_on_submit() :
            thisStep = db_session.query(Step).filter(and_(Step.flow_id == fid, Step.step_uid == session["'" + app.config['SESSION_UID'] + "'"])).order_by(Step.update_time.desc()).first()

            if ((int(form.data['changeapp']) == -1 or int(form.data['changeapp']) == app.config['APPROVAL_ADD']) and int(form.data['approval_status']) == app.config['APPROVAL_REJECT']) :
                thisStep.approval_status = int(form.data['approval_status'])
                thisStep.approval_msg = form.data['opinion']
                thisStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                thisStep.step = thisStep.step + 1
                thisStep.user_step = thisStep.user_step + 1

                db_session.commit()

                thisFlow = db_session.query(Flow).filter_by(id = fid).first()
                thisFlow.status = app.config['FLOW_STATUS_REJECT']
                db_session.commit()
                
                if is_ajax :
                    return flash_form(form, True, 0, '/approval/log')
                else :
                    return flash_form(form, False, 0, '/approval/log')

            if int(form.data['changeapp']) == app.config['APPROVAL_ADD'] or int(form.data['changeapp']) == app.config['APPROVAL_TURN'] :
                if int(form.data['changeapp']) == app.config['APPROVAL_ADD'] :
                    thisStep.approval_status = int(form.data['approval_status'])
                else :
                    thisStep.approval_status = int(form.data['changeapp'])
                thisStep.approval_msg = form.data['opinion']
                thisStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                thisStep.step = thisStep.step + 1
                thisStep.user_step = thisStep.user_step + 1

                db_session.commit()
                
                step_uid = form.data['towho'].encode('utf-8').split(' ')[0]
                
                newStep = int(thisStep.step) + 1
                newUserStep = thisStep.user_step + 1
                newStepUser = form.data['towho'].encode('utf-8').split(' ')[1].decode('utf-8')
                newStep = Step(flow_id = fid, step = newStep, step_uid = step_uid, approval_status = app.config['APPROVAL_NEW'], approval_msg = '', user_from = 1, user_step = newUserStep, step_user = newStepUser, is_add_turn = app.config['IS_ADD_TURN'])
                db_session.add(newStep)
                db_session.commit()

                if is_ajax :
                    return flash_form(form, True, 0, '/approval/log')
                else :
                    return flash_form(form, False, 0, '/approval/log')
            else :
                thisStep.approval_msg = form.data['opinion']
                thisStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                thisStep.step = thisStep.step + 1
                thisStep.user_step = thisStep.user_step + 1
                thisStep.approval_status = int(form.data['approval_status'])

                db_session.commit()

                engine = Engine(1, session["'" + app.config['USER_INFO_HIGHER'] + "'"], thisStep.flow_id)
                engine.process()

                if is_ajax :
                    return flash_form(form, True, 0, '/approval/log')
                else :
                    return flash_form(form, False, 0, '/approval/log')


        else :
            if is_ajax :
                return flash_form(form, True, -1)
            else :
                return render_template('wf/' + temp, flow = flow, flowDetail = flowDetail, attachments = atts, logs = approval_logs, logsNum = logsNum, form = form, nowApproval = nowApproval)
    else :
        return render_template('wf/' + temp, flow = flow, flowDetail = flowDetail, attachments = atts, logs = approval_logs, logsNum = logsNum, form = form, nowApproval = nowApproval)


@mod.route('/approval/<f_type>/from_config/<fid>', methods=['POST'])
def approval_by_config(f_type, fid) :
    form = testApproval()

    if request.method == "POST" :
        is_ajax = request.form['is_ajax']
        if form.validate_on_submit() :
            if form.data['u_type'] == 'create' :
                start_date = str(form.data['start_date'])
                start_time = str(form.data['start_time'])
                end_date = str(form.data['end_date'])
                end_time = str(form.data['end_time'])

                flow = db_session.query(Flow).filter_by(id = fid).first()
                detail = flow.detail
                detail = json.loads(detail)
                detail['start_date'] = start_date
                detail['start_time'] = start_time
                detail['end_date'] = end_date
                detail['end_time'] = end_time
                
                detail = json.dumps(detail)

                flow.detail = detail

                db_session.commit()

            engine = Engine(1, session["'" + app.config['USER_INFO_HIGHER'] + "'"], fid)
            engine.process()
            
            if is_ajax :
                return flash_form(form, True, 0, '/approval/log')
            else :
                return flash_form(form, False, 0, '/approval/log')
        else :
            if is_ajax :
                return flash_form(form, True, -1)
            else :
                return redirect('/approval/' + f_type + '/from_config/' + fid)
