# -*- coding = utf-8 -*-
# @Time : 2023-07-22 16:04
# @Author : mfk
# @File : encrypt.py
# @Software : PyCharm
import hashlib

def encrypt(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()