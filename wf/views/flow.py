# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 16:13:39
FileName:   flow.py
'''

from flask import Blueprint, render_template, request, url_for, redirect, session, g, jsonify
from wf import app
from wf.db.db import db_session
from wf.model import *
from wf.util.auth import *
from sqlalchemy import or_, and_
import md5
import json
from flask.ext.sqlalchemy import Pagination
import math
from wf.util.libs import *
from datetime import date
from formValidate.testFlowForm import testFlowForm
from formValidate.connectFlowForm import connectFlowForm
from formValidate.contractFlowForm import contractFlowForm
import os
import time
import datetime
from wf.engine.engine import Engine
from decimal import Decimal

mod = Blueprint('flow', __name__)

@mod.route('/flow/add', methods=['GET'])
def flow_add() :
    return render_template('wf/flow_add.html')

@mod.route('/flow/add/<id>', methods=['GET', 'POST'])
def flow_add_by_type(id) :
    id = int(id)
    if id == 1 :
        form = testFlowForm()
    elif id == 2 :
        form = connectFlowForm()
    elif id == 3 :
        pass
    elif id == 4 :
        form = contractFlowForm()
    temp = get_type_temp(id)
    today = str(date.today())

    if request.method == "POST" :
        is_ajax = request.form['is_ajax']
        if form.validate_on_submit() :
            f_type = id
            create_user_id = session["'" + app.config['SESSION_UID'] + "'"]
            create_user = session["'" + app.config['SESSION_REAL_NAME'] + "'"]
            department = session["'" + app.config['USER_INFO_DEPARTMENT']  + "'"]
            phone = session["'" + app.config['USER_INFO_MOBILE']  + "'"]
            email = session["'" + app.config['USER_INFO_EMAIL']  + "'"]
            status = app.config['FLOW_STATUS_CREATE']
            relation = form.data['relation_id']
            subject = form.data['subject']
            des = form.data['des']

            tmp = {}
            for item in form.data :
                tmp[item] = unicode(form.data[item])
            
            detail = json.dumps(tmp)

            thisFlow = Flow(f_type = f_type, create_user_id = create_user_id, create_user = create_user, department = department, phone = phone, email = email, status = status, detail = detail, relation = relation, subject = subject, des = des)
            db_session.add(thisFlow)
            db_session.commit()

            if 'pics' in session :
                for item in session['pics'] :
                    thisAttachement = Attachment(flow_id = thisFlow.id, path = str(item), create_user_id = session["'" + app.config['SESSION_UID'] + "'"])
                    db_session.add(thisAttachement)
                    db_session.commit()

                del session['pics']

            engine = Engine(id, session["'" + app.config['USER_INFO_HIGHER'] + "'"], thisFlow.id)
            engine.process()

            if is_ajax :
                return flash_form(form, True, 0, '/create/log')
            else :
                return render_template('wf/' + temp, today = today, form = form)
        else :
            if is_ajax :
                return flash_form(form, True, -1)
            else :
                return render_template('wf/' + temp, today = today, form = form)
    else :
        return render_template('wf/' + temp, today = today, form = form)

@mod.route('/flow/uploadFile', methods=['POST'])
def uploadFile() :
    if request.method == 'POST' :
        data_file = request.files.get('files[]')
        file_name = str(int(time.time())) + "_" + data_file.filename
        
        if not os.path.exists(app.config['UPLOAD_PATH']) :
            os.makedirs(app.config['UPLOAD_PATH'])

        save_path = app.config['UPLOAD_PATH'] + '/' + file_name
        data_file.save(save_path)
       
        if not 'pics' in session :
            session['pics'] = {}

        session['pics'][file_name] = file_name

        file_url = url_for('static', filename = 'upload/' + file_name)
        
        file_size = os.path.getsize(app.config['ROOT_PATH'] + '/wf' + file_url)

        one = {}

        one['name'] = file_name
        one['size'] = file_size
        one['url'] = file_url
        one['thumbnailUrl'] = file_url
        one['deleteUrl'] = "/flow/deleteUpload/?" + "file=" + file_name + "&_method=DELETE"
        one['deleteType'] = "POST"

        result = {}
        result['files'] = []

        result['files'].append(one)

        return json.dumps(result)

@mod.route('/flow/deleteUpload/', methods=['POST'])
def deleteUpload() :
    file_name = request.args.get('file')
    file_url = url_for('static', filename = 'upload/' + file_name)
    absolute_url = app.config['ROOT_PATH'] + '/wf' + file_url 
    
    if os.path.isfile(absolute_url) :
        os.remove(absolute_url)
    if file_name in session['pics'] :
        del session['pics'][file_name]
    result = {}
    result[file_name] = True
    return json.dumps(result)

@mod.route('/flow/detail/<f_type>/<fid>', methods=['GET', 'POST'])
def flow_detail(f_type, fid) :
    if int(f_type) == 1 :
        form = testFlowForm()
    elif int(f_type) == 2 :
        form = connectFlowForm()
    elif int(f_type) == 4 :
        form = contractFlowForm()
    temp = get_detail_temp(int(f_type))
    fid = int(fid)
    flow = db_session.query(Flow).filter_by(id = fid).first()

    if not flow :
        flash_error('没有该流程')
        return redirect('/flow/add')

    flowDetail = json.loads(flow.detail)
    testNum = 0
    if 'testdetail' in flowDetail :
        testNum = len(flowDetail['testdetail'])

    attachments = db_session.query(Attachment).filter_by(flow_id = fid).all()
    atts = []

    for attachment in attachments :
        tmp = {}
        tmp['att'] = app.config['ATTACHEMENT_PATH'] + "/" + attachment.path
        tmp['id'] = attachment.id
        atts.append(tmp)

    approval_logs = db_session.query(Step).filter(and_(Step.flow_id == fid, Step.approval_status != app.config['APPROVAL_NEW'])).order_by(Step.update_time.desc()).all()

    logsNum = len(approval_logs)
    
    if request.method == 'POST' :
        is_ajax = request.form['is_ajax']
        if form.validate_on_submit() : 
            flow.status = app.config['FLOW_STATUS_RUNNING']
            tmp = {}
            for item in form.data :
                tmp[item] = unicode(form.data[item])

            flow.detail = json.dumps(tmp)
            
            flow.subject = form.data['subject']
            flow.des = form.data['des']
            flow.relation = form.data['relation_id']
            
            db_session.commit()

            if 'pics' in session :
                for item in session['pics'] :
                    thisAttachement = Attachment(flow_id = flow.id, path = str(item), create_user_id = session["'" + app.config['SESSION_UID'] + "'"])
                    db_session.add(thisAttachement)
                    db_session.commit()

                del session['pics']

            engine = Engine(f_type, session["'" + app.config['USER_INFO_HIGHER'] + "'"], flow.id)
            engine.process()

            if is_ajax :
                return flash_form(form, True, 0, '/create/log')
            else :
                return render_template('wf/' + temp, today = today, form = form)

        else :
            if is_ajax :
                return flash_form(form, True, -1)
            else :
                return render_template('wf/' + temp, today = today, form = form)
    else :
        return render_template('wf/' + temp, flow = flow, flowDetail = flowDetail, testNum = testNum, attachments = atts, logs = approval_logs, logsNum = logsNum, form = form)

@mod.route('/flow/del/attachment/<fid>/<aid>', methods=['GET'])
def del_attachment(fid, aid) :
    attachment = db_session.query(Attachment).filter(and_(Attachment.id == aid, Attachment.flow_id == fid)).first()
    flow = db_session.query(Flow).filter_by(id = fid).first()
    if not session["'" + app.config['SESSION_UID'] + "'"] == flow.create_user_id :
        return redirect('/403')
    
    if not flow :
        flash_error('没有该流程')
        return redirect('/flow/add')
    if not attachment :
        flash_error('没有该附件')

    filePath = os.path.abspath(os.path.dirname(__file__)) + "/../static/" + app.config['ATTACHEMENT_PATH'] + "/" + attachment.path
    os.remove(filePath) 
    db_session.delete(attachment)
    db_session.commit()
    
    flash(u'删除成功', 'succ')
    return redirect('/flow/detail/'+ str(flow.f_type) + '/' + str(fid)) 
