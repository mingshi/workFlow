# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/17 20:13:15
FileName:   approval.py
'''

from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional
from flask import session, flash
from wf import app

class Approval(Form) :
    flow_id         =   IntegerField(u'流程id', validators=[DataRequired('流程id是必须的')])
    opinion         =   TextAreaField(u'意见', validators=[Optional()])
    changeapp       =   IntegerField(u'是否转签或加签', validators=[Optional(), DataRequired('是否转签或加签必须选择或不选')])
    towho           =   TextField(u'交给谁', validators=[Optional()])
    approval_status =   IntegerField(u'审批状态')
    is_close        =   IntegerField(u'是否关闭', validators=[Optional()])
    
    start_time          = DateTimeField(u'开始时间', validators=[Optional(), DataRequired('开始时间格式不正确')])
    end_time            = DateTimeField(u'开始时间', validators=[Optional(), DataRequired('结束时间格式不正确')])
    custom_name         = TextField(u'客户名称', validators=[Optional()])
    pv                  = IntegerField(u'pv', validators=[Optional(), DataRequired('pv格式不正确')])
    income              = DecimalField(u'收入', validators=[Optional(), DataRequired('收入格式不正确')])
    cost                = DecimalField(u'成本', validators=[Optional(), DataRequired('成本格式不正确')])
    real_income         = DecimalField(u'利润', validators=[Optional(), DataRequired('利润格式不正确')])
    income_rate         = TextField(u'利润率', validators=[Optional()])
    back_info           = TextField(u'回款情况', validators=[Optional()])
    pay_des             = TextField(u'备注', validators=[Optional()])
    u_type              = TextField(u'审批人类型', validators=[Optional()])
    is_end_input        = IntegerField(u'是否结束输入', validators=[Optional()])

    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False
        
        if self.changeapp.data :
            if int(self.changeapp.data) == -1 and not self.approval_status.data:
                flash(u'审批状态必须选择', 'error')
                return False

            if int(self.changeapp.data) == 3 and not self.approval_status.data :
                flash(u'审批状态必须选择', 'error')
                return False

            if int(self.changeapp.data) == 3 and not self.towho.data:
                flash(u'交给谁必须填写', 'error')
                return False

            if int(self.changeapp.data) == 3 and not self.approval_status.data and not self.towho.data:
                flash(u'审批状态必须选择,交给谁必须填写', 'error')
                return False

            if int(self.changeapp.data) == 2 and not self.towho.data :
                flash(u'交给谁必须填写', 'error')
                return False

        return True
