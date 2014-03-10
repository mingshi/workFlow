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


