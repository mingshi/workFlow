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
    
    temp = get_approval_temp(fType)
    
    flowDetail = json.loads(flow.detail)
    
    testNum = 0
    if 'testDetail' in flowDetail :
        testNum = len(flowDetail['testdetail'])

    attachments = db_session.query(Attachment).filter_by(flow_id = fid).all()

    atts = []
    for attachment in attachments :
        atts.append(app.config['ATTACHEMENT_PATH'] + "/" + attachment.path)

    # 获取审批记录
    approval_logs = db_session.query(Step).filter(and_(Step.flow_id == fid, Step.approval_status != app.config['APPROVAL_NEW'])).order_by(Step.update_time.desc()).all()

    logsNum = len(approval_logs)
    
    nowApproval = db_session.query(Step).filter(Step.flow_id == fid).order_by(Step.create_time.desc()).first()
    
    if not nowApproval.step_uid == session["'" + app.config['SESSION_UID'] + "'"] :
        return redirect('/403')

    if request.method == "POST" :
        is_ajax = request.form['is_ajax']
        if form.validate_on_submit() :
            thisStep = db_session.query(Step).filter(and_(Step.flow_id == fid, Step.step_uid == session["'" + app.config['SESSION_UID'] + "'"])).order_by(Step.create_time.desc()).first()
            
            if form.data['changeapp'] :
                if ((int(form.data['changeapp']) == -1 or int(form.data['changeapp']) == app.config['APPROVAL_ADD']) and int(form.data['approval_status']) == app.config['APPROVAL_REJECT']) :
                    thisStep.approval_status = int(form.data['approval_status'])
                    thisStep.approval_msg = form.data['opinion']
                    thisStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

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

                    db_session.commit()
                    
                    step_uid = form.data['towho'].encode('utf-8').split(' ')[0]
                    
                    newStep = int(thisStep.step) + 1
                    if thisStep.user_from == app.config['USER_FROM_CONFIG'] :
                        newUserStep = thisStep.user_step
                    else :
                        newUserStep = thisStep.user_step + 1
                    newStepUser = form.data['towho'].encode('utf-8').split(' ')[1].decode('utf-8')
                    newStep = Step(flow_id = fid, step = newStep, step_uid = step_uid, approval_status = app.config['APPROVAL_NEW'], approval_msg = '', user_from = thisStep.user_from, user_step = newUserStep, step_user = newStepUser, is_add_turn = app.config['IS_ADD_TURN'])
                    db_session.add(newStep)
                    db_session.commit()

                    if is_ajax :
                        return flash_form(form, True, 0, '/approval/log')
                    else :
                        return flash_form(form, False, 0, '/approval/log')
                else :
                    thisStep.approval_msg = form.data['opinion']
                    thisStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    if form.data['approval_status'] :
                        thisStep.approval_status = int(form.data['approval_status'])
                    elif form.data['is_close'] :
                        thisStep.approval_status = int(app.config['APPROVAL_CLOSE'])

                    db_session.commit()
                    
                    if not form.data['is_close'] :
                        engine = Engine(f_type, session["'" + app.config['USER_INFO_HIGHER'] + "'"], thisStep.flow_id)
                        engine.process()
                    else :
                        if form.data['is_close'] == app.config['APPROVAL_CLOSE'] :
                            flow.status = app.config['FLOW_STATUS_FINISH']
                            db_session.commit()

                    if is_ajax :
                        return flash_form(form, True, 0, '/approval/log')
                    else :
                        return flash_form(form, False, 0, '/approval/log')
            else :
                thisStep.approval_msg = form.data['opinion']
                thisStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                if form.data['approval_status'] :
                    thisStep.approval_status = int(form.data['approval_status'])
                elif form.data['is_close'] :
                    thisStep.approval_status = int(app.config['APPROVAL_CLOSE'])

                db_session.commit()
                
                if not 'is_close' in form.data :
                    engine = Engine(f_type, session["'" + app.config['USER_INFO_HIGHER'] + "'"], thisStep.flow_id)
                    engine.process()
                else :
                    if form.data['is_close'] == app.config['APPROVAL_CLOSE'] :
                        flow.status = app.config['FLOW_STATUS_FINISH']
                        db_session.commit()

                if is_ajax :
                    return flash_form(form, True, 0, '/approval/log')
                else :
                    return flash_form(form, False, 0, '/approval/log')


        else :
            if is_ajax :
                return flash_form(form, True, -1)
            else :
                return render_template('wf/' + temp, flow = flow, testNum = testNum, flowDetail = flowDetail, attachments = atts, logs = approval_logs, logsNum = logsNum, form = form, nowApproval = nowApproval)
    else :
        return render_template('wf/' + temp, flow = flow, flowDetail = flowDetail, testNum = testNum, attachments = atts, logs = approval_logs, logsNum = logsNum, form = form, nowApproval = nowApproval)


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
                
                engine = Engine(f_type, session["'" + app.config['USER_INFO_HIGHER'] + "'"], fid)
                engine.process()

            if form.data['u_type'] == 'finance' and form.data['cate'] == 0 :
                nowStep = db_session.query(Step).filter_by(flow_id = fid).order_by(Step.create_time.desc()).first()
                
                nowStep.approval_status = app.config['APPROVAL_OK']
                nowStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                db_session.commit() 
                
                step_uid = form.data['whoPay'].split(' ')[0]
                step_user = form.data['whoPay'].split(' ')[1]
                step = nowStep.step + 1
                approval_status = app.config['APPROVAL_NEW']
                approval_msg = ''
                user_from = app.config['USER_FROM_CONFIG']
                user_step = nowStep.user_step
                is_add_turn = app.config['IS_ADD_TURN']

                thisStep = Step(flow_id = fid, step = step, step_uid = step_uid, approval_status = approval_status, approval_msg = approval_msg, user_from = user_from, user_step = user_step, step_user = step_user, is_add_turn = is_add_turn)
                db_session.add(thisStep)
                db_session.commit()
            
            if form.data['u_type'] == 'finance' and form.data['cate'] == 1 :
                nowStep = db_session.query(Step).filter_by(flow_id = fid).order_by(Step.create_time.desc()).first()
                nowStep.approval_status = form.data['finance_approval_status']
                nowStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                db_session.commit()

                engine = Engine(f_type, session["'" + app.config['USER_INFO_HIGHER'] + "'"], fid)
                engine.process()

            if form.data['u_type'] == 'testadmin' and form.data['cate'] == 0 :
                nowStep = db_session.query(Step).filter_by(flow_id = fid).order_by(Step.create_time.desc()).first()
                nowStep.approval_status = app.config['APPROVAL_OK']
                nowStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                db_session.commit()

                step_uid = form.data['whoTest'].split(' ')[0]
                step_user = form.data['whoTest'].split(' ')[1]
                step = nowStep.step + 1
                approval_status = app.config['APPROVAL_NEW']
                approval_msg = ''
                user_from = app.config['USER_FROM_CONFIG']
                user_step = nowStep.user_step
                is_add_turn = app.config['IS_ADD_TURN']

                thisStep = Step(flow_id = fid, step = step, step_uid = step_uid, approval_status = approval_status, approval_msg = approval_msg, user_from = user_from, user_step = user_step, step_user = step_user, is_add_turn = is_add_turn)
                db_session.add(thisStep)
                db_session.commit()
            
            if form.data['u_type'] == 'testadmin' and form.data['cate'] == 1 :
                flow = db_session.query(Flow).filter_by(id = fid).first()
                if form.data['is_end_test'] == 1 :
                    engine = Engine(f_type, session["'" + app.config['USER_INFO_HIGHER'] + "'"], fid)
                    engine.process()
                
                detail = json.loads(flow.detail)
                if not 'testdetail' in detail :
                    detail['testdetail'] = []

                tmpTest = {}
                tmpTest['test_date'] = str(form.data['test_date']).strip()
                tmpTest['test_start_time'] = str(form.data['test_start_time']).strip()
                tmpTest['test_end_time'] = str(form.data['test_end_time']).strip()
                tmpTest['test_custom_name'] = str(form.data['test_custom_name']).strip()
                tmpTest['test_cost_ecpm'] = str(form.data['test_cost_ecpm']).strip()
                tmpTest['test_income_ecpm'] = str(form.data['test_income_ecpm']).strip()
                tmpTest['test_income_rate'] = str(form.data['test_income_rate']).strip()
                
                if tmpTest['test_date'] and tmpTest['test_start_time'] and tmpTest['test_end_time'] and tmpTest['test_custom_name'] and tmpTest['test_cost_ecpm'] and tmpTest['test_income_ecpm'] and tmpTest['test_income_rate'] :
                    detail['testdetail'].append(tmpTest)
                    detail = json.dumps(detail)
                    flow.detail = detail
                    db_session.commit()

            if form.data['u_type'] == 'ceo' :
                if form.data['ceo_approval_status'] == app.config['APPROVAL_OK'] :
                    engine = Engine(f_type, session["'" + app.config['USER_INFO_HIGHER'] + "'"], fid)
                    engine.process()
                elif form.data['ceo_approval_status'] == app.config['APPROVAL_GOON_TEST'] :
                    akey = app.config['WORK_FLOW']['1']['can'].index('testadmin')
                    nowStep = db_session.query(Step).filter_by(flow_id = fid).order_by(Step.create_time.desc()).first()
                    nowStep.approval_status = form.data['ceo_approval_status']
                    nowStep.approval_msg = form.data['opinion']
                    nowStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

                    db_session.commit()

                    step_uid = app.config['WORK_FLOW']['1']['uid'][akey]
                    stepUser = get_multi_user_info_by_uid(step_uid)
                    tmpInfo = json.loads(stepUser)
                    step_user = tmpInfo['info'][0]['realname']
                    user_from = app.config['USER_FROM_CONFIG']
                    user_step = akey
                    approval_status = app.config['APPROVAL_NEW']
                    approval_msg = ''
                    is_add_turn = app.config['IS_ADD_TURN']
                    step = nowStep.step + 1

                    thisStep = Step(flow_id = fid, step = step, step_uid = step_uid, approval_status = approval_status, approval_msg = approval_msg, user_from = user_from, user_step = user_step, step_user = step_user, is_add_turn = is_add_turn)
                    db_session.add(thisStep)
                    db_session.commit()
                elif form.data['ceo_approval_status'] == app.config['APPROVAL_REJECT'] :
                    nowStep = db_session.query(Step).filter_by(flow_id = fid).order_by(Step.create_time.desc()).first()
                    nowStep.approval_status = form.data['ceo_approval_status']
                    nowStep.approval_msg = form.data['opinion']
                    nowStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

                    db_session.commit()
                    
                    flow =  db_session.query(Flow).filter_by(id = fid).first()
                    flow.status = app.config['FLOW_STATUS_REJECT']
                    db_session.commit()

            if form.data['u_type'] == 'closer' :
                nowStep = db_session.query(Step).filter_by(flow_id = fid).order_by(Step.create_time.desc()).first()
                nowStep.approval_status = form.data['is_close']
                nowStep.update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

                db_session.commit()
                
                if form.data['is_close'] == app.config['FLOW_STATUS_FINISH'] :
                    flow =  db_session.query(Flow).filter_by(id = fid).first()
                    flow.status = form.data['is_close']
                    db_session.commit()

            if is_ajax :
                return flash_form(form, True, 0, '/approval/log')
            else :
                return flash_form(form, False, 0, '/approval/log')
        else :
            if is_ajax :
                return flash_form(form, True, -1)
            else :
                return redirect('/approval/' + f_type + '/from_config/' + fid)


@mod.route('/approval/log', methods=['GET'])
def approval_log() :
    uid = session["'" + app.config['SESSION_UID'] + "'"]
    approvals = db_session.query(Step).filter_by(step_uid = uid).order_by(Step.update_time.desc()).all()

    result = []
    for step in approvals :
        tmp = {}
        tmpFlow = db_session.query(Flow).filter_by(id = step.flow_id).first()
        tmp['fid'] = tmpFlow.id
        tmp['subject'] = tmpFlow.subject
        tmp['create_time'] = tmpFlow.create_time
        tmp['create_user'] = tmpFlow.create_user
        tmp['step_status'] = app.config['STEP_NAMING'][step.approval_status]
        tmp['step_time'] = step.update_time
        tmp['f_type'] = tmpFlow.f_type
        result.append(tmp)

    return render_template('wf/approval_log.html', results = result)
