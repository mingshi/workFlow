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
import datetime
from wf.engine.engine import Engine
from decimal import Decimal

mod = Blueprint('approval', __name__)

@mod.route('/approval/<f_type>/<id>', methods=['GET'])
def approval_flow(f_type, id) :
    fType = int(f_type)
    id = int(id)
    
    flow = db_session.query(Flow).filter_by(id = id).first()

    temp = get_approval_temp(f_type)
    
    flowDetail = json.loads(flow.detail)
    
    attachments = db_session.query(Attachment).filter_by(flow_id = id).all()
    
    atts = []
    for attachment in attachments :
        atts.append(app.config['ATTACHEMENT_PATH'] + "/" + attachment.path)

    return render_template('wf/' + temp, flow = flow, flowDetail = flowDetail, attachments = atts)


