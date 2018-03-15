# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse

from utils.utils_common import dumps_result, json_loads, cross_domain

# Create your views here.


def login(request):
    result = dict()
    rev_json_body = json_loads(request.body)
    username = rev_json_body.get('username', None)
    password = rev_json_body.get('password', None)
    if not username or not password:
        result["status"], result["data"] = 1, "failed"

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        if user.is_superuser:
            authority = "superuser"
        else:
            authority = "normaluser"
        result["status"], result["data"] = 0, {"username": request.user.username,
                                               "session_id": request.session.session_key,
                                               "authority": authority}
    else:
        result["status"], result["data"] = 1001, "failed"

    response = HttpResponse(dumps_result(result))
    return cross_domain(response)


def logout(request):
    result = dict()

    try:
        auth.logout(request)
        result["status"], result["data"] = 0, "success"
    except Exception as error:
        result["status"], result["data"] = 1001, "{}".format(error)
    finally:
        response = HttpResponse(dumps_result(result))
        return cross_domain(response)

