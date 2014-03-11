#!/usr/bin/env python
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/10 10:25:55
FileName:   run.py
'''
# -*- coding: utf-8 -*-

from wf import app

if __name__ == "__main__" :
    if app.config['DEBUG'] :
        print app.config
    app.run(host=app.config['HOST'], port=app.config['PORT'])


