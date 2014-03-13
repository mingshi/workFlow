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

mod = Blueprint('flow', __name__)

@mod.route('/flow/add', methods=['GET'])
def flow_add() :
    return render_template('wf/flow_add.html')

@mod.route('/flow/add/<id>', methods=['GET'])
def flow_add_by_type(id) :
    id = int(id)

    if id == 1 :
        temp = "test.html"
    elif id == 2 :
        temp = "connect.html"
    elif id == 3 :
        temp = "pay.html"
    elif id == 4 :
        temp = "contract.html"
    else :
        temp = "test.html"
    
    today = str(date.today())
    return render_template('wf/' + temp, today = today)

