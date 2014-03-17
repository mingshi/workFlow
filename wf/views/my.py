# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/17 14:42:01
FileName:   my.py
'''
from flask import Blueprint, render_template, request, url_for, redirect, session, g, jsonify
from wf import app
from wf.db.db import db_session
from wf.model import *
from wf.util.auth import *
from sqlalchemy import or_, desc
import md5
import json
from flask.ext.sqlalchemy import Pagination
import math
from wf.util.libs import *
from datetime import date
from formValidate.testFlowForm import testFlowForm
import os
import time
import datetime
from wf.engine.engine import Engine
from decimal import Decimal

mod = Blueprint('my', __name__)

@mod.route('/my/approval', methods=['GET'])
def my_approval() :
    uid = session["'" + app.config['SESSION_UID'] + "'"]

    steps = db_session.query(Step).filter_by(step_uid = uid, approval_status = app.config['APPROVAL_NEW']).order_by(Step.create_time.desc()).all()
    
    flowIds = []
    for step in steps :
        flowIds.append(int(step.flow_id))

    flows = db_session.query(Flow).filter(Flow.id.in_(flowIds)).order_by(Flow.create_time.desc()).all()

    return render_template('wf/my_approval.html', flows = flows)


