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

app = Flask(__name__)

# load config according to enviroment
app.config.from_object("config")
if os.path.exists(app.config['ROOT_PATH'] + "/env.py"):
    app.config.from_object("env")
app.config.from_object("config.%sConfig" % (app.config['ENV']) )

configFile = os.path.join(app.root_path, 'BaseWFConfig.py')

app.config.from_pyfile(configFile)

'''
follow import views package
'''
from wf.views import login, captcha, index

app.register_blueprint(login.mod)
app.register_blueprint(captcha.mod)
app.register_blueprint(index.mod)

'''
views import finished
'''



@app.before_request
def before_request() :
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
