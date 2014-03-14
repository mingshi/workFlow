# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/12 10:20:25
FileName:   login.py
'''
from flask import Blueprint, render_template, request, redirect, url_for, request, session, g, flash
from wf.db.db import db_session
import json
from wf.model import *
from wf import app
import time
from wf.util.auth import *
from pprint import pprint
from formValidate.loginForm import loginForm
from wf.util.libs import *

mod = Blueprint("login", __name__)

@mod.route('/login', methods=["GET", "POST"])
def login() :
    form = loginForm()
    if request.method == "POST" :
        if form.validate_on_submit() :
            loginInfo = do_login(form.data['username'], form.data['password'])
            if loginInfo == "error" :
                flash_error(u'系统错误')
                return render_template('wf/login.html', form=form)
            else :
                user = db_session.query(User).filter_by(username = form.data['username']).first()
                resource = json.loads(loginInfo)
                if resource['code'] == 0 :
                    login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    login_ip = request.remote_addr
                    if not user :
                        thisUser = User(uid = resource['info']['id'], username = form.data['username'], realname = resource['info']['realname'], login_time = login_time, login_ip = login_ip)
                        db_session.add(thisUser)
                        db_session.commit()
                    else :
                        user.login_time = login_time
                        user.login_ip = login_ip
                        db_session.commit()

                    # 获取用户的基本信息 由于多了一个http请求,需要优化
                    userInfo = get_user_info(form.data['username'])
                    userRealInfo = json.loads(userInfo)

                    if userRealInfo['msg'] == 'success' and userRealInfo['status'] == 'ok' :
                        session["'" + app.config['USER_INFO_MOBILE'] + "'"] = userRealInfo['info'][0]['mobile']
                        session["'" + app.config['USER_INFO_EMAIL'] + "'"] = userRealInfo['info'][0]['email']
                        session["'" + app.config['USER_INFO_DEPARTMENT'] + "'"] = userRealInfo['info'][0]['department']
                        session["'" + app.config['USER_INFO_HIGHER'] + "'"] = userRealInfo['info'][0]['higher']
                    key = app.config['LOGIN_SESSION_NAME']
                    session["'" + key + "'"] = form.data['username']
                    keyRealName = app.config['SESSION_REAL_NAME']
                    session["'" + keyRealName + "'"] = resource['info']['realname']
                    keyUid = app.config['SESSION_UID']
                    session["'" + keyUid + "'"] = resource['info']['id']
                    
                    return redirect('/index')
                else :
                    message = resource['msg']
                    flash_error(message)
                
                    return render_template('wf/login.html', form=form)
        else :
            flash_form(form)
            return render_template('wf/login.html', form=form)
    else :
        key = app.config['LOGIN_SESSION_NAME']
        if "'" + key + "'" in session :
            pass
        else :
            return render_template('wf/login.html', form=form)


@mod.route('/logout')
def logout() :
    key = app.config['LOGIN_SESSION_NAME']
    session.pop("'" + key + "'", None)
    session.pop("'" + app.config['SESSION_REAL_NAME'] + "'", None)
    session.pop("'" + app.config['SESSION_UID'] + "'", None)
    session.pop("'" + app.config['USER_INFO_MOBILE'] + "'", None)
    session.pop("'" + app.config['USER_INFO_EMAIL'] + "'", None)
    session.pop("'" + app.config['USER_INFO_DEPARTMENT'] + "'", None)

    return redirect('/')
