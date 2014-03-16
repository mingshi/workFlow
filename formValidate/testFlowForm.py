# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/14 14:21:20
FileName:   testFlowForm.py
'''

from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, DecimalField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional
from flask import session, flash
from wf import app

class testFlowForm(Form) :
    subject             = TextField(u'标题', validators=[DataRequired('标题必须填写')])
    media_type          = TextField(u'媒体类别', validators=[DataRequired('媒体类别必须填写')])
    ad_position         = TextField(u'广告位置', validators=[DataRequired('广告位置必须填写')])
    media_name          = TextField(u'投放媒体名称', validators=[DataRequired('投放媒体名称必须填写')])
    es_effect           = TextField(u'预估效果', validators=[DataRequired('预估效果必须填写')])
    test_consume        = TextField(u'测试时长', validators=[DataRequired('测试时长必须填写')])
    test_cost           = DecimalField(u'测试成本', validators=[DataRequired('测试成本必须为数字')])
    custom_type         = TextField(u'客户类型', validators=[DataRequired('客户类型必须填写')])
    disable_custom_type = TextField(u'禁投客户类型', validators=[DataRequired('禁投客户类型必须填写')])
    material_require    = TextField(u'素材要求', validators=[DataRequired('素材要求必须填写')])
    material_size       = TextField(u'素材尺寸', validators=[DataRequired('素材尺寸必须填写')])
    sensitive_area      = TextField(u'敏感地域', validators=[DataRequired('敏感地域必须填写')])
    media_admin         = TextField(u'媒体负责人', validators=[DataRequired('媒体负责人必须填写')])
    pay_type            = SelectField(u'付款方式', choices=[('1', u'免费'), ('2', u'后付'), ('3', u'预付')], validators=[DataRequired('付款方式必须选择')])
    pay_cost            = DecimalField(u'付款总额', validators=[Optional(), DataRequired('付款总额必须为数字')])
    des                 = TextAreaField(u'其他说明', validators=[Optional()])
    relation_id         = TextField(u'关联流程id', validators=[Optional()])
    es_cost             = DecimalField(u'预计采购成本', validators=[Optional(), DataRequired('预计采购成本必须为数字')])
    
    pay_company         = TextField(u'付款公司', validators=[Optional()])
    end_pay_time        = DateTimeField(u'最晚付款时间', validators=[Optional(), DataRequired('最晚付款时间格式不对')])
    media_account       = TextField(u'媒体账户名', validators=[Optional()])
    card_number         = IntegerField(u'银行卡号', validators=[Optional(), DataRequired('银行卡号格式不对')])
    media_bank          = TextField(u'开户行名称', validators=[Optional()])
    
    def __init__(self, *args, **kwargs) :
        Form.__init__(self, *args, **kwargs)

    def validate(self) :
        rv = Form.validate(self)
        if not rv :
            return False

        if int(self.pay_type.data) == 3 :
            if not self.pay_company.data or not self.end_pay_time.data or not self.media_account.data or not self.card_number.data or not self.media_bank.data :
                flash(u'付款选项填写不完整', 'error')
                return False

        return True
        
