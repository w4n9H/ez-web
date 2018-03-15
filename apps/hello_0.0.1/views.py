# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from utils.utils_common import dumps_result

# Create your views here.


def ping(request):
    result = dict()
    try:
        result["status"], result["data"] = 0, {"message": "Welcome to MTA for SX project!!!"}
    except Exception as error:
        result["status"], result["data"] = 1, error
    finally:
        return HttpResponse(dumps_result(result))