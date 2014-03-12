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

mod = Blueprint('flow', __name__)

@mod.route('/flow/add', methods=['GET'])
def flow_add() :
    return render_template('wf/flow_add.html')

