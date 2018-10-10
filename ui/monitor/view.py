# -*- coding: utf8 -*-
from django.shortcuts import render
from django.http import *
from django.urls import path
import ui.models as models
from . import session
from . import api
import random
import json
import time
import math


def monitor_show_main_page(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    return render(request, "监控/main.html", context=context)


def monitor_stop_session(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    return render(request, "监控/main.html", context=context)


def monitor_fetch_session_info(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    return render(request, "监控/main.html", context=context)


def monitor_fetch_session_json_data(request, sid):
    s = session.get_session_by_id(sid)
    if s is None:
        reason = "因为使用了无效的会话ID（%d）导致重定向" % sid
        return api.json_redir_to_page(request, reason, href='/')

    j = s.run_step_forward()

    return api.json_without_error(request, j)



urlpatterns = [
    path("<int:sid>/", monitor_show_main_page),

    path("<int:sid>/json/", monitor_fetch_session_json_data),

    path("<int:sid>/stop/", monitor_stop_session),
    path("<int:sid>/info/", monitor_fetch_session_info),

    # 设备控制
    path("<int:sid>/control/start/", lambda request, sid: api.json_with_error(request, "Not Implemented", sid=sid)),
    path("<int:sid>/control/stop/", lambda request, sid: api.json_with_error(request, "Not Implemented")),
    path("<int:sid>/control/paikong/on/", lambda request, sid: api.json_with_error(request, "Not Implemented")),
    path("<int:sid>/control/paikong/off/", lambda request, sid: api.json_with_error(request, "Not Implemented")),
]
