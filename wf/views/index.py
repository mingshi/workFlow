# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 15:38:28
FileName:   index.py
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

mod = Blueprint("index", __name__)
@mod.route('/', methods=['GET'])
@mod.route('/index', methods=['GET'])
def index() :
    return redirect('/flow/add')
    return render_template('wf/index.html')

@mod.route('/getJsonUser', methods=['POST', 'GET'])
def do_search_user() :
    kwd = request.args.get('term').strip()
    users = search_user(kwd)
    
    realUsers = json.loads(users)

    return json.dumps(realUsers['info'])
