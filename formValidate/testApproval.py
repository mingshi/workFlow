# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/22 21:14:25
FileName:   testApproval.py
'''

from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Optional
from flask import session, flash
from wf import app

class testApproval(Form) :
    u_type          =   TextField(u'配置文件用户类型', validators=[DataRequired('配置文件用户类型是必须的')])
    start_date      =   DateField(u'测试开始日期', validators=[Optional(), DataRequired('测试开始日期格式不对')])
    start_time      =   TextField(u'测试开始时间段', validators=[Optional(), DataRequired('测试开始时间段是必须的')])  
    end_date        =   DateField(u'测试结束日期', validators=[Optional(), DataRequired('测试结束日期格式不对')])
    end_time        =   TextField(u'测试结束时间段', validators=[Optional(), DataRequired('测试结束时间段是必须的')])
    approval_status =   SelectField(u'是否已付款', choices=[('0', u'请选择'), ('7', '已付款')], validators=[Optional(), DataRequired('是否付款必须选择')])
    
    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False

        if self.u_type.data == 'create' :
            if not self.start_date.data or not self.start_time.data or not self.end_date.data or not self.end_time.data :
                #flash(u'开始日期,结束日期,开始时间段以及结束时间段必须填写', 'error')
                return False
        if self.u_type.data == 'finance' :
            if self.approval_status.data == '0' :
                return False
        
        return True


