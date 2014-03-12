# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2013/11/26 14:31:12
FileName:   log.py
'''

from flask import Flask, request, redirect, send_from_directory, render_template, g, session
import os
import re
from wf import app
from datetime import date

def get_home_path() :
    pathArr = request.path.strip().split('/')
    homePath = "/" + pathArr[1]
    
    return homePath

def logRequest(s) :
    homePath = get_home_path()
    logPath = app.config['LOG_PATH']
    if not homePath in app.config['NO_NEED_LOG_PATH'] :
        today = date.today()
        logfile = logPath + "/" + str(today) + ".log"
        fObj = open(logfile, 'a')
        try :
            fObj.write(s + "\n")
        finally :
            fObj.close()
