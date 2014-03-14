# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 16:13:39
FileName:   flow.py
'''

from flask import Blueprint, render_template, request, url_for, redirect, session, g
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
        is_ajax = request.form['is_ajax']
        ret = {}
        if form.validate_on_submit() :
            pass
            return "11111"
        else :
            if is_ajax :
                return flash_form(form, True, -1)
            else :
                return render_template('wf/' + temp, today = today, form = form)
    else :
        return render_template('wf/' + temp, today = today, form = form)

