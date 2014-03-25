# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/25 14:14:12
FileName:   payFlowForm.py
'''
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional
from flask import session, flash
from wf import app

class payFlowForm(Form) :
    subject             = TextField(u'标题', validators=[DataRequired('标题必须填写')])
    media_type          = TextField(u'媒体类别', validators=[DataRequired('媒体类别必须填写')])
    ad_position         = TextField(u'广告位置', validators=[DataRequired('广告位置必须填写')])
    end_pay_time_dead   = DateTimeField(u'最晚付款时间', validators=[DataRequired('最晚付款时间格式不正确')])
    start_pay_time      = TextField(u'付款开始时间段', validators=[DataRequired('付款开始时间段格式不正确')])
    end_pay_time        = TextField(u'付款结束时间段', validators=[DataRequired('付款结束时间段格式不正确')])
    contract_pass       = SelectField(u'合同是否通过', choices=[('0', u'未通过'), ('1', u'通过')], validators=[DataRequired('合同是否通过必须选择')])
    request             = IntegerField(u'总请求量', validators=[DataRequired('总请求量必须为数字')])
    click               = IntegerField(u'总点击量', validators=[DataRequired('总点击量必须为数字')])
    show_lose_rate      = TextField(u'展现损耗率', validators=[DataRequired('展现损耗率必须填写')])
    cut_info            = TextField(u'扣量情况', validators=[DataRequired('扣量情况必须填写')])
    price               = DecimalField(u'单价', validators=[DataRequired('单价格式不正确')])
    contract_num        = IntegerField(u'合同编号', validators=[DataRequired('合同编号必须填写')])
    pay_company         = TextField(u'付款公司', validators=[DataRequired('付款公司必须填写')])
    media_account       = TextField(u'媒体账户名', validators=[DataRequired('媒体账户名必须填写')])
    card_number         = IntegerField(u'银行卡号', validators=[DataRequired('银行卡号格式不对')])
    media_bank          = TextField(u'开户行名称', validators=[DataRequired('开户行名称必须填写')])
    media_name          = TextField(u'投放媒体名称', validators=[DataRequired('投放媒体名称必须填写')])
    relation_id         = TextField(u'关联流程id', validators=[Optional()])
    slot_id             = IntegerField(u'广告位id', validators=[DataRequired('广告位ID必须填写')])
    schedule            = TextField(u'合同规定排期', validators=[DataRequired('合同规定排期必须填写')])
    show                = IntegerField(u'总展现量', validators=[DataRequired('总展现量必须填写')])
    ctr                 = TextField(u'ctr', validators=[DataRequired('ctr必须填写')])
    data_gap            = TextField(u'真实数据与排期差', validators=[DataRequired('真是数据与排期差必须填写')])
    clear_data          = TextField(u'结算数据', validators=[DataRequired('结算数据必须填写')])
    clear_amount        = DecimalField(u'结算金额', validators=[DataRequired('结算金额格式不对')])
    pay_cost            = DecimalField(u'付款总额', validators=[DataRequired('付款总额格式不正确')])
    des                 = TextAreaField(u'其他说明', validators=[Optional()])
    
    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False
    
        return True
