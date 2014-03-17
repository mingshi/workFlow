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
    changeapp       =   IntegerField(u'是否转签或加签', validators=[DataRequired('是否转签或加签必须选择或不选')])
    towho           =   TextField(u'交给谁', validators=[Optional()])
    approval_status =   IntegerField(u'审批状态')

    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False

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
