# -*- coding: UTF-8 -*-
__author__ = 'lijie'
from django.shortcuts import render
from django.http import *
import ui.models as models
import ui.api as api
import random
import json


def monitor_by_session_id(request, sid):
    context = dict()
    return render(request, "监控/main.html", context=context)


def monitor_json_by_session_id(request, sid):
    j = {
        'p1': random.randrange(0, 100),
        'p2': random.randrange(0, 100),
        'f1': random.randrange(0, 100),
    }
    r = HttpResponse(json.dumps(j))
    r['Context-Type'] = 'application/json'
    return r