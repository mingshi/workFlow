# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/10 10:12:27
FileName:   config.py
'''

import os
def hostname() :
    sys = os.name
    if sys == 'nt':
            hostname = os.getenv('computername')
            return hostname
    elif sys == 'posix':
            host = os.popen('echo $HOSTNAME')
            try:
                    hostname = host.read()
                    return hostname
            finally:
                    host.close()
    else:
            return 'Unkwon hostname'

DEV_HOST = ['mingshi-hacking.local']

if hostname().strip('\n') in DEV_HOST :
    ENV = "Development"
    BASE_DOMAIN = "http://127.0.0.1:3999"
    UPLOAD_PATH = "/tmp/upload"
else :
    ENV = "Production"
    BASE_DOMAIN = ""
    UPLOAD_PATH = ""

NO_NEED_LOGIN = ["login", "static", "captcha", "favicon", "sign"]
NO_NEED_LOG_PATH = ["/static"]

LOG_PATH = "logs"

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

'''
config some Key
'''
SESSION_KEY_CAPTCHA = 'captcha_WF'
SECRET_KEY = "WF*U(*#@====++ASD_o213&^5%"

LOGIN_SESSION_NAME = "!adeazWFLoginKey%!"
LOGIN_KEY = "7d26eda13b33c1257999de31bcd8ebfc"
SIG_KEY = "adeazMemberSigKey@#$%^&"
AUTH_URL = "http://member.adeaz.com/api/login"

USER_INFO_KEY = "3ec8e544422a626075d904d0a9be0dcb"
USER_INFO_SIGN = "!adeazMemberUiFO7&^%"
USER_INFO_MOBILE = "adEazWorkFlowUserMobile"
USER_INFO_EMAIL = "adEazWorkFlowUserEmail"
USER_INFO_DEPARTMENT = "adEazWorkFlowUserDepartment"
USER_INFO_HIGHER = "adEazWorkFlowUserHigher"
USER_INFO_URL = "http://member.adeaz.com/api/userinfo_by_username"

SESSION_REAL_NAME = "adeazWF_realname"
SESSION_UID = "adeazWF_uid"

class Config(object):
    HOST='0.0.0.0'
    PORT=8818
    DB_CONNECT_OPTIONS = {}

class ProductionConfig(Config):
    DEBUG=True
    DB_URI="mysql+oursql://root:thisisme!@localhost/wf?unix_socket=/tmp/mysql.sock&charset=utf8"

class DevelopmentConfig(Config):
    HOST='0.0.0.0'
    PORT=3999
    DEBUG=True
    DB_URI="mysql+oursql://root:@127.0.0.1/wf?charset=utf8"
