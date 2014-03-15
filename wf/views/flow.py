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
from sqlalchemy import or_
import md5
import json
from flask.ext.sqlalchemy import Pagination
import math
from wf.util.libs import *
from datetime import date
from formValidate.testFlowForm import testFlowForm
import os
import time

mod = Blueprint('flow', __name__)

@mod.route('/flow/add', methods=['GET'])
def flow_add() :
    return render_template('wf/flow_add.html')

@mod.route('/flow/add/<id>', methods=['GET', 'POST'])
def flow_add_by_type(id) :
    form = testFlowForm()
    id = int(id)
    
    temp = get_type_temp(id)
    today = str(date.today())

    if request.method == "POST" :
        print session['pics']
        is_ajax = request.form['is_ajax']
        ret = {}
        if form.validate_on_submit() :
            session['pics'] = {}
            pass
            return "11111"
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
