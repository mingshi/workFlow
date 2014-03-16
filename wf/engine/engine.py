# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/16 18:15:11
FileName:   engine.py
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

def get_next_uid(f_type, uid) :
    f_type = int(f_type)
    if f_type == 1 :
        

