# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 13:20:54
FileName:   loginForm.py
'''

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length
from flask import session, flash
from wf import app

class loginForm(Form) :
    username = TextField(u'用户名', validators=[DataRequired('用户名必须填写')])
    password = PasswordField(u'密码', validators=[DataRequired('密码必须填写')])
    captcha = TextField(u'验证码', validators=[DataRequired('验证码必须填写'), Length(min=4, max=4)])

    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False
        
        SESSION_KEY_CAPTCHA = app.config['SESSION_KEY_CAPTCHA']

        if not session["'" + SESSION_KEY_CAPTCHA + "'"] : 
            flash(u'验证码session错误', 'error')
            return False

        tmpVerify = session["'" + SESSION_KEY_CAPTCHA + "'"]
        code = ""

        for _code in tmpVerify :
            code += _code

        code = code.lower()

        if not self.captcha.data.lower() == code :
            flash(u'验证码错误', 'error')
            return False

        return True

