# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/25 12:54:07
FileName:   contractFlowForm.py
'''
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional
from flask import session, flash
from wf import app

class contractFlowForm(Form) :
    subject             = TextField(u'标题', validators=[DataRequired('标题必须填写')])
    media_type          = TextField(u'媒体类别', validators=[DataRequired('媒体类别必须填写')])
    ad_position         = TextField(u'广告位置', validators=[DataRequired('广告位置必须填写')])
    media_name          = TextField(u'投放媒体名称', validators=[DataRequired('投放媒体名称必须填写')])
    get_traffic         = TextField(u'采购流量', validators=[DataRequired('采购流量必须填写')])
    relation_id         = TextField(u'关联流程id', validators=[Optional()])
    slot_id             = IntegerField(u'广告位id', validators=[DataRequired('广告位ID必须填写')])
    start_connect_time  = DateTimeField(u'正式接入时间', validators=[DataRequired('正式接入时间必须填写')])
    contract_cost       = TextField(u'合同采购成本', validators=[DataRequired('合同采购成本必须填写')])
    contract_num        = IntegerField(u'合同编号', validators=[DataRequired('合同编号必须填写')])
    pay_type            = SelectField(u'付款方式', choices=[('1', u'免费'), ('2', u'后付'), ('3', u'预付')], validators=[DataRequired('付款方式必须选择')])
    contract_name       = TextField(u'合同对方名称', validators=[DataRequired('合同对方名称必须填写')])
    account_time        = SelectField(u'账期', choices=[('30', u'30天'), ('45', u'45天'), ('60', u'60天'), ('75', u'75天'), ('90', u'90天')], validators=[DataRequired('>账期必须选择')])
    cut_info            = TextField(u'扣量情况', validators=[DataRequired('扣量情况必须填写')])
    contract_main       = TextField(u'我方签约主体', validators=[DataRequired('我方签约主体必须填写')])
    des                 = TextAreaField(u'其他说明', validators=[Optional()])

    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False

        return True

