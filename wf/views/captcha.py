# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 10:53:56
FileName:   captcha.py
'''

from flask import Blueprint, Response, session
from wf.util.captcha import *
import StringIO
from wf import app

mod = Blueprint("captcha", __name__)

@mod.route('/captcha')
def captcha() :
    app.secret_key = app.config['SECRET_KEY']
    res = create()
    image = res['image']
    SESSION_KEY_CAPTCHA = app.config['SESSION_KEY_CAPTCHA']
    session["'" + SESSION_KEY_CAPTCHA + "'"] = res['chars']
    buf = StringIO.StringIO()
    image.save(buf,'png',quality=90)
    return Response(buf.getvalue(), mimetype='image/png')

