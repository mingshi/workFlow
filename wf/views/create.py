# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/17 11:34:37
FileName:   create.py
'''

from flask import Blueprint, render_template, request, url_for, redirect, session, g
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

mod = Blueprint("create", __name__)
@mod.route('/create/log', methods=['GET'])
def create_log() :
    uid = session["'" + app.config['SESSION_UID'] + "'"]
    myFlows = db_session.query(Flow).filter_by(create_user_id = uid).order_by(Flow.create_time.desc()).all()
    
    ids = []
    tmpFlow = {}
    for flow in myFlows :
        newStep = db_session.query(Step).filter_by(flow_id = flow.id).order_by(Step.create_time.desc()).first()
        if newStep :
            tmpFlow[int(flow.id)] = unicode(newStep.step_user)
    
    return render_template('wf/create_log.html', flows = myFlows, flowUser = tmpFlow)

