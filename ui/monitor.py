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
    session = api.search_session_by_id(sid)
    if session is None:
        print("因为使用了无效的会话ID（%d）导致重定向" % sid)
        return HttpResponseRedirect('/')

    j = {
        'p1': session.get_P1(1),
        'p2': session.get_P2(1),
        'f1': session.get_F1(1),
    }

    r = HttpResponse(json.dumps(j))
    r['Context-Type'] = 'application/json'
    return r