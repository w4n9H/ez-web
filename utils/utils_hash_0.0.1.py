# !/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib


def file_md5(filepath):
    mo = hashlib.md5()
    with open(filepath, 'rb') as fp:
        mo.update(fp.read())
    return mo.hexdigest()


def file_sha1(filepath):
    mo = hashlib.sha1()
    with open(filepath, 'rb') as fp:
        mo.update(fp.read())
    return mo.hexdigest()


def text_md5(text):
    return hashlib.md5(text).hexdigest()


def text_sha1(text):
    return hashlib.sha1(text).hexdigest()
