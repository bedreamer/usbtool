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

    context['sid'] = sid
    context['modbus_dev'] = s.get_modbus_dev()
    context['bms_dev'] = s.get_bms_dev()

    return render(request, "监控/pane1l.html", context=context)


def monitor_stop_session(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    return render(request, "监控/panel.html", context=context)


def monitor_fetch_session_info(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    return render(request, "监控/panel.html", context=context)


def monitor_list_all_in_table(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    return render(request, "监控/list.html", context=context)


def monitor_fetch_session_json_data(request, sid):
    s = session.get_session_by_id(sid)
    if s is None:
        reason = "因为使用了无效的会话ID（%d）导致重定向" % sid
        return api.json_redir_to_page(request, reason, href='/')

    body, ext = s.run_step_forward(request)

    return api.json_without_error(request, body, **ext)


def monitor_fetch_session_supported_registers_json_data(request, sid):
    s = session.get_session_by_id(sid)
    if s is None:
        reason = "因为使用了无效的会话ID（%d）导致重定向" % sid
        return api.json_redir_to_page(request, reason, href='/')

    body, ext = s.get_supported_registers_json(request)

    return api.json_without_error(request, body, **ext)


def monitor_session_read_register(request, sid, reg):
    s = session.get_session_by_id(sid)
    if s is None:
        reason = "因为使用了无效的会话ID（%d）导致重定向" % sid
        return api.json_redir_to_page(request, reason, href='/')

    body, ext = s.read_register(request, reg)

    return api.json_without_error(request, body, **ext)


def monitor_session_write_register(request, sid, reg, str_val):
    s = session.get_session_by_id(sid)
    if s is None:
        reason = "因为使用了无效的会话ID（%d）导致重定向" % sid
        return api.json_redir_to_page(request, reason, href='/')

    body, ext = s.write_register(request, reg, str_val)

    return api.json_without_error(request, body, **ext)


def monitor_session_modbus_read(request, sid, server_address, reg):
    """
    通过回话读取指定设备的寄存器
    :param request:
    :param sid:
    :param server_address:
    :param reg:
    :return:
    """
    return api.json_without_error(request, {})


def monitor_session_modbus_write(request, sid, server_address, reg, val):
    return api.json_without_error(request, {})


urlpatterns = [
    path("<int:sid>/", monitor_show_main_page),

    path("<int:sid>/json/", monitor_fetch_session_json_data),

    path("<int:sid>/stop/", monitor_stop_session),
    path("<int:sid>/list/", monitor_list_all_in_table),
    path("<int:sid>/info/", monitor_fetch_session_info),

    path("<int:sid>/registers/", monitor_fetch_session_supported_registers_json_data),
    path("<int:sid>/read/<str:reg>/", monitor_session_read_register),
    path("<int:sid>/write/<str:reg>/<str:str_val>/", monitor_session_write_register),

    path("<int:sid>/modbus/server/<int:server_address>/x03/register/<int:reg>/", monitor_session_modbus_read),
    path("<int:sid>/modbus/server/<int:server_address>/x06/register/<int:reg>/value/<str:val>/", monitor_session_modbus_write),

    # 设备控制
    path("<int:sid>/control/start/", lambda request, sid: api.json_with_error(request, "Not Implemented", sid=sid)),
    path("<int:sid>/control/stop/", lambda request, sid: api.json_with_error(request, "Not Implemented")),
    path("<int:sid>/control/paikong/on/", lambda request, sid: api.json_with_error(request, "Not Implemented")),
    path("<int:sid>/control/paikong/off/", lambda request, sid: api.json_with_error(request, "Not Implemented")),
]
