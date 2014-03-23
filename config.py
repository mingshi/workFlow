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
    ATTACHEMENT_PATH = "upload"
else :
    ENV = "Production"
    BASE_DOMAIN = ""
    UPLOAD_PATH = ""
    ATTACHEMENT_PATH = "upload"

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

MULTI_USER_INFO_URL = "http://member.adeaz.com/api/apimultiuserinfo"

SEARCH_USER_SIGN = "7f54de2f8ef0ae3c885431acf30f2839"
SEARCH_USER_KEY = "8cc59b4056aae8d50091ec8647127105"
SEARCH_USER_URL = "http://member.adeaz.com/api/apisearchuser"

SESSION_REAL_NAME = "adeazWF_realname"
SESSION_UID = "adeazWF_uid"

'''
下面定义流程的各种状态
'''
FLOW_STATUS_CREATE = 0
FLOW_STATUS_RUNNING = 0
FLOW_STATUS_REJECT = 2
FLOW_STATUS_FINISH = 10

FLOW_NAMING = {
    FLOW_STATUS_CREATE  :   u'正在进行', 
    FLOW_STATUS_RUNNING :   u'正在进行',
    FLOW_STATUS_REJECT  :   u'驳回',
    FLOW_STATUS_FINISH  :   u'已结束'
}


#下面是审批状态
APPROVAL_OK =   1
APPROVAL_TURN = 2
APPROVAL_ADD = 3
APPROVAL_REJECT = 4
APPROVAL_YET_OK = 5
APPROVAL_GOON_TEST = 6
APPROVAL_NEW = 0
APPROVAL_PAYED = 7
APPROVAL_CLOSE = 10

STEP_NAMING = {
    APPROVAL_OK :   u'同意',
    APPROVAL_TURN : u'转签',
    APPROVAL_ADD : u'加签',
    APPROVAL_REJECT : u'驳回',
    APPROVAL_YET_OK : u'不同意但继续',
    APPROVAL_GOON_TEST : u'建议继续测试',
    APPROVAL_NEW : u'新建',
    APPROVAL_PAYED : u'已付款',
    APPROVAL_CLOSE : u'关闭'
}

USER_FROM_DB = 1
USER_FROM_CONFIG = 2

MONEY_LINE = '3000'

IS_ADD_TURN = 1

'''
状态定义完毕
'''

PAY_TYPE = {
        "1" : u'免费',
        "2" : u'后付',
        "3" : u'预付'
        }



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
