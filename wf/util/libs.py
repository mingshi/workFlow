# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 14:53:06
FileName:   libs.py
'''

from flask import flash
import json

def flash_form(form, flag = False, code = 0) :
    message = ""
    for field, errors in form.errors.items() :
        for error in errors :
            message += error + ","
    message = message.strip(',').decode('utf-8')
    
    if not message and code == 0 and flag == True:
        message = u'保存成功'

    if message :
        if flag == True :
            ret = {}
            ret['code'] = code
            ret['msg'] = message
            return json.dumps(ret)
            
        flash(message, 'error')

def flash_error(error) :
    flash(error, 'error')

def get_type_temp(id) :
    temp = ""
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
    return temp
