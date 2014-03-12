# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2013/11/28 17:47:32
FileName:   upload.py
'''

from flask import Flask, session, redirect, request
from wf import app
import md5
import re
import pycurl
import StringIO
import urllib
import os
import Image
from wf.util.image_resize import *

def allowed_file(filename) :
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]


def generate_file_path_name(vid) :
    lastid = md5.new(vid).hexdigest()
    f = lastid[0:2]
    e = lastid[2:4]
    name = lastid[4:-1] + ".jpg"
    path = app.config["IMAGE_PATH"] + "/" + f + "/" + e + "/"

    res = {}
    res["path"] = path
    res["filename"] = name
    return res

def upload_file(file, path, filename) :
    msg = {}
    try :
        if not os.path.isdir(path) :
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        
        im = Image.open(path + filename)
        outfile = path + "s_" + filename

        if app.config['SITE_NUM'] == 0 :
            new_image = resize_and_crop(im, app.config['IMAGE_RESIZE_SIZE'][0], app.config['IMAGE_RESIZE_SIZE'][1])
            new_image.save(outfile, "JPEG", quality = 95)
        else :
            size = app.config['IMAGE_RESIZE_SIZE']
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "JPEG", quality = 95)
        
        msg["info"] = "文件上传成功"
        msg["type"] = "succ"
    except Exception, e :
        msg["info"] = "文件上传失败"
        msg["type"] = "error"

    if msg and "info" in msg :
        msg["info"] = msg["info"].decode('utf-8')
    return msg
