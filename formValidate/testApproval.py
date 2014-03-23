# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/22 21:14:25
FileName:   testApproval.py
'''

from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask import session, flash
from wf import app

class testApproval(Form) :
    u_type              =   TextField(u'配置文件用户类型', validators=[DataRequired('配置文件用户类型是必须的')])
    start_date          =   DateField(u'测试开始日期', validators=[Optional(), DataRequired('测试开始日期格式不对')])
    start_time          =   TextField(u'测试开始时间段', validators=[Optional(), DataRequired('测试开始时间段是必须的')])  
    end_date            =   DateField(u'测试结束日期', validators=[Optional(), DataRequired('测试结束日期格式不对')])
    end_time            =   TextField(u'测试结束时间段', validators=[Optional(), DataRequired('测试结束时间段是必须的')])
    approval_status     =   SelectField(u'是否已付款', choices=[('0', u'请选择'), ('7', '已付款')], validators=[Optional(), DataRequired('是否付款必须选择')])
    whoPay              =   TextField(u'指派谁去付款', validators=[Optional(), DataRequired('指派谁去付款必须填写')])
    whoTest             =   TextField(u'指派谁去测试', validators=[Optional(), DataRequired('指派谁去测试必须填写')])
    cate                =   IntegerField(u'相同类别的分类', validators=[NumberRange(min=0, max=1)])
    test_date           =   DateField(u'测试日期', validators=[Optional(), DataRequired('测试日期格式不对')])
    test_start_time     =   TextField(u'测试开始时间段', validators=[Optional(), DataRequired('测试开始时间段格式不对')])
    test_end_time       =   TextField(u'测试结束时间段', validators=[Optional(), DataRequired('测试结束时间段格式不对')])
    test_custom_name    =   TextField(u'投放客户名称', validators=[Optional(), DataRequired('投放客户名称是必须的')])
    test_cost_ecpm      =   TextField(u'成本ecpm', validators=[Optional(), DataRequired('成本ecpm是必须的')])
    test_income_ecpm    =   TextField(u'收入ecpm', validators=[Optional(), DataRequired('收入ecpm是必须的')])
    test_income_rate    =   TextField(u'利润率', validators=[Optional(), DataRequired('利润率是必须的')])
    is_end_test         =   IntegerField(u'是否结束测试', validators=[Optional(), NumberRange(min=0, max=1)])
    opinion             =   TextAreaField(u'意见', validators=[Optional()])
    ceo_approval_status =   IntegerField(u'审批状态', validators=[Optional(), DataRequired('审批状态必须选择')])
    #ceo_approval_status =   SelectField(u'审批状态', choices=[('1', u'同意'), ('6', u'建议继续测试'), ('4', u'驳回')], validators=[Optional(), DataRequired('审批状态必须选择')])
    is_close            =   IntegerField(u'是否关闭', validators=[Optional()])

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
        if self.u_type.data == 'finance' and self.cate.data == 0 :
            if not self.whoPay.data :
                return False

        if self.u_type.data == 'finance' and self.cate.data == 1 :
            if self.approval_status.data == '0' :
                return False

        if self.u_type.data == 'testadmin' and self.cate.data == 0 :
            if not self.whoTest.data :
                return False
       
        if self.u_type.data == 'testadmin' and self.cate.data == 1 :
            if not self.is_end_test.data :
                if not self.test_date.data or not self.test_start_time.data or not self.test_end_time.data or not self.test_custom_name.data or not self.test_cost_ecpm.data or not self.test_income_ecpm.data or not self.test_income_rate.data :
                    return False

        if self.u_type.data == 'ceo' :
            if not self.ceo_approval_status.data :
                return False

        return True


