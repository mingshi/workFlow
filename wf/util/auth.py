# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2013/11/18 16:37:01
FileName:   auth.py
'''

from flask import Flask, session, redirect, request
from wf import app
import md5
import re
import pycurl
import StringIO
import urllib

def create_login_sign() :
    params = []
    for key in request.form :
        params.append(key)
    params.append("key")
    params.sort()

    uri = ""
    for _key in params :
        if (_key == "sign") :
            continue
        if (_key == "key") :
            _value = app.config['LOGIN_KEY']
        else :
            _value = request.form[_key]

        uri += _key + "=" + _value + "&"
    uri = uri.strip('&')
    sign = md5.new(uri).hexdigest()

    return sign

def safe_password(str) :
    level = 0;
    if re.search('\d', str) :
        level += 1
    if re.search('[a-z]', str) :
        level += 1
    if re.search('[A-Z]', str) :
        level += 1
    if re.search('[^0-9a-zA-Z]', str) :
        level += 1

    if level < 3 :
        return None
    return 1

def password_hash(password) :
    signKey = app.config['SIG_KEY']
    tmpPass = md5.new(password).hexdigest()
    return md5.new(signKey + tmpPass).hexdigest()

def login_hash(username, password) :
    tmpPassword = password_hash(password)
    tmpUri = "key=" + app.config['LOGIN_KEY'] + "&password=" + tmpPassword + "&username=" + username

    return md5.new(tmpUri).hexdigest()

def do_login(username, password) :
    sign = login_hash(username, password)
    passwd = password_hash(password)

    post_data_dic = {"username" : username, "password" : passwd, "sign" : sign}

    try :
        ch = pycurl.Curl()
        ch.fp = StringIO.StringIO()
        ch.setopt(pycurl.URL, app.config['AUTH_URL'])
        ch.setopt(pycurl.AUTOREFERER, 1)
        ch.setopt(pycurl.FOLLOWLOCATION, 1)
        ch.setopt(pycurl.CONNECTTIMEOUT, 300)
        ch.setopt(pycurl.TIMEOUT, 500)
        ch.setopt(pycurl.POSTFIELDS, urllib.urlencode(post_data_dic))
        ch.setopt(pycurl.WRITEFUNCTION, ch.fp.write)
        ch.perform()

        res = ch.fp.getvalue()

    except :
        res = "error"
        return res
    else :
        return res


def get_user_info(username) :
    sign = create_user_info_sign(username)
    post_data_dic = {"username" : username, "key" : app.config['USER_INFO_KEY'], "sign" : sign}

    try :
        ch = pycurl.Curl()
        ch.fp = StringIO.StringIO()
        ch.setopt(pycurl.URL, app.config['USER_INFO_URL'])
        ch.setopt(pycurl.AUTOREFERER, 1)
        ch.setopt(pycurl.FOLLOWLOCATION, 1)
        ch.setopt(pycurl.CONNECTTIMEOUT, 300)
        ch.setopt(pycurl.TIMEOUT, 500)
        ch.setopt(pycurl.POSTFIELDS, urllib.urlencode(post_data_dic))
        ch.setopt(pycurl.WRITEFUNCTION, ch.fp.write)
        ch.perform()

        res = ch.fp.getvalue()

    except :
        res = "error"
        return res
    else :
        return res

def create_user_info_sign(username) :
    tmp = "key=" + app.config['USER_INFO_SIGN'] + "&username=" + username
    return md5.new(tmp).hexdigest()
