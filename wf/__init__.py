# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/10 10:27:58
FileName:   __init__.py
'''
from flask import Flask, request, redirect, send_from_directory, render_template, g, session, make_response
import os
import re
import md5
import time
from datetime import datetime
'''
上面是load一些基础包
'''
app = Flask(__name__)

# load config according to enviroment
app.config.from_object("config")
if os.path.exists(app.config['ROOT_PATH'] + "/env.py"):
    app.config.from_object("env")
app.config.from_object("config.%sConfig" % (app.config['ENV']) )

configFile = os.path.join(app.root_path, 'BaseWFConfig.py')

app.config.from_pyfile(configFile)

'''
下面load一些用户包
'''
from wf.util.log import *
from wf.db.db import db_session

'''
follow import views package
'''
from wf.views import login, captcha, index, flow

app.register_blueprint(login.mod)
app.register_blueprint(captcha.mod)
app.register_blueprint(index.mod)
app.register_blueprint(flow.mod)

'''
views import finished
'''

@app.before_request
def before_request() :
    g.start = time.time() * 1000
    path = request.path
    key = app.config['LOGIN_SESSION_NAME']
    if not ("'" + key + "'" in session) :
        rycle = 0
        for tmpPath in app.config['NO_NEED_LOGIN'] :
            if not tmpPath in path :
                continue
            else :
                rycle += 1
                break
        if rycle == 0 :
            return redirect('login')
    else :
        rycle = 0
        for tmpPath in app.config['NO_NEED_LOGIN'] :
            if not tmpPath in path :
                continue
            else :
                rycle += 1

        if rycle == 0 :
            pathArr = path.strip().split('/')
            g.homePath = pathArr[1]


@app.route('/app-path')
def app_path():
    return app.root_path

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html')

@app.errorhandler(405)
def page_not_found(error):
    return render_template('error/405.html')

@app.route("/version")
def hello():
    return "0.1"

@app.route("/403")
def forbbiden():
    return render_template('error/403.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static' ), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.teardown_request
def close_session(exception):
    db_session.remove()

@app.after_request
def after_request(response) :
    s = str(datetime.now()) + " " + str(request.url) + " " + str(response.status_code) + " "
    etime = time.time() * 1000 - g.start
    s += str(etime) + " "

    s += str(request.remote_addr) + " "

    key = app.config['LOGIN_SESSION_NAME']
    if not ("'" + key + "'" in session) :
        s += " "
    else :
        s += session["'" + key + "'"] + " "

    logRequest(s)
    return response


