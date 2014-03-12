# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 14:53:06
FileName:   libs.py
'''

from flask import flash

def flash_form(form) :
    message = ""
    for field, errors in form.errors.items() :
        for error in errors :
            message += error + ","
    message = message.decode('utf-8')
    if message :
        flash(message, 'error')

def flash_error(error) :
    flash(error, 'error')
