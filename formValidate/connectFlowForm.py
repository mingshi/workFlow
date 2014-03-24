# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/24 19:22:20
FileName:   connectFlowForm.py
'''

from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional
from flask import session, flash
from wf import app

class connectFlowForm(Form) :
    subject             = TextField(u'标题', validators=[DataRequired('标题必须填写')])
    media_type          = TextField(u'媒体类别', validators=[DataRequired('媒体类别必须填写')])
    ad_position         = TextField(u'广告位置', validators=[DataRequired('广告位置必须填写')])
    media_name          = TextField(u'投放媒体名称', validators=[DataRequired('投放媒体名称必须填写')])
    get_traffic         = TextField(u'采购流量', validators=[DataRequired('采购流量必须填写')])
    start_connect_time  = DateTimeField(u'正式接入时间', validators=[DataRequired('正式接入时间必须填写')])
    contract_pass       = SelectField(u'合同是否通过', choices=[('0', u'未通过'), ('1', u'通过')], validators=[Optional(), DataRequired('合同是否通过必须选择')])
    pay_type            = SelectField(u'付款方式', choices=[('1', u'免费'), ('2', u'后付'), ('3', u'预付')], validators=[DataRequired('付款方式必须选择')])
    slot_id             = IntegerField(u'广告位id', validators=[DataRequired('广告位ID必须填写')])
    contract_cost       = TextField(u'合同采购成本', validators=[DataRequired('合同采购成本必须填写')])
    cut_info            = TextField(u'扣量情况', validators=[DataRequired('扣量情况必须填写')])
    account_time        = SelectField(u'账期', choices=[('30', u'30天'), ('45', u'45天'), ('60', u'60天'), ('75', u'75天'), ('90', u'90天')], validators=[DataRequired('账期必须选择')])
    start_pay_time      = TextField(u'付款开始时间段', validators=[Optional(), DataRequired('付款开始时间段格式不正确')])
    end_pay_time        = TextField(u'付款结束时间段', validators=[Optional(), DataRequired('付款结束时间段格式不正确')])
    pay_company         = TextField(u'付款公司', validators=[Optional()])
    contract_num        = IntegerField(u'合同编号', validators=[Optional(), DataRequired('合同编号必须填写')])
    end_pay_time_dead   = DateTimeField(u'最晚付款时间', validators=[Optional(), DataRequired('最晚付款时间格式不正确')])
    pay_cost            = DecimalField(u'付款总额', validators=[Optional(), DataRequired('付款总额格式不正确')])
    media_account       = TextField(u'媒体账户名', validators=[Optional()])
    card_number         = IntegerField(u'银行卡号', validators=[Optional(), DataRequired('银行卡号格式不对')])
    media_bank          = TextField(u'开户行名称', validators=[Optional()])
    des                 = TextAreaField(u'其他说明', validators=[Optional()])
    relation_id         = TextField(u'关联流程id', validators=[Optional()])

    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False
        
        if self.contract_pass.data == app.config['IS_PASS'] :
            if not self.contract_num.data :
                return False

        if int(self.pay_type.data) == 3 :
            if not self.start_pay_time.data or not self.end_pay_time.data or not self.pay_company.data or not self.end_pay_time_dead.data or not self.pay_cost.data or not self.media_account.data or not self.card_number.data or not self.media_bank.data :
                return False

        return True
