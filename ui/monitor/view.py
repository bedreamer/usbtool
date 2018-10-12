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
    context['session'] = s
    s.set_mode('panel')

    modbus_dev_driver = s.get_modbus_dev_driver()
    bms_dev_driver = s.get_bms_dev_driver()

    # 根据型号不同加载不同的UI模板
    modbus_dev_sections_name_list = [
        'model_恒温恒流设备_状态表区',
        'model_恒温恒流设备_温度计区',
        'model_恒温恒流设备_仪表盘区',
        'model_恒温恒流设备_控制区',
        'model_恒温恒流设备_故障显示区'
    ]
    for section_name in modbus_dev_sections_name_list:
        context[section_name] = modbus_dev_driver.get_template(section_name)

    bms_dev_sections_name_list = ['model_BMS设备_状态表区', 'model_BMS设备_仪表盘区']
    #for section_name in bms_dev_sections_name_list:
    context['model_BMS设备_状态表区'] = "监控/model-BMS设备状态表.html"
    context['model_BMS设备_仪表盘区'] = "监控/model-BMS设备仪表盘区.html"

    return render(request, "监控/base-会话显示面板.html", context=context)


def monitor_list_all_in_table(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    context['session'] = s
    s.set_mode('list')

    return render(request, "监控/list.html", context=context)


def monitor_session_in_grid(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    context['session'] = s
    s.set_mode('grid')

    return render(request, "监控/base-曲线视图模板.html", context=context)


def monitor_show_session_configure_page(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['sid'] = sid
    context['modbus_dev'] = s.get_modbus_dev()
    context['bms_dev'] = s.get_bms_dev()
    context['session'] = s
    s.set_mode('options')

    return render(request, "监控/base-会话配置面板.html", context=context)


def monitor_stop_session(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    context['session'] = s

    return render(request, "监控/panel.html", context=context)


def monitor_fetch_session_info(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    context['session'] = s

    return render(request, "监控/panel.html", context=context)


def monitor_session_in_list(request, sid):
    context = dict()
    s = session.get_session_by_id(sid)
    if s is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = s.modbus_dev
    context['sid'] = sid
    context['session'] = s

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
    path("<int:sid>/", lambda request, sid: HttpResponseRedirect(request.path + 'panel/')),

    path("<int:sid>/json/", monitor_fetch_session_json_data),

    path("<int:sid>/panel/", monitor_show_main_page),
    path("<int:sid>/grid/", monitor_session_in_grid),
    path("<int:sid>/list/", monitor_session_in_list),

    path("<int:sid>/options/", monitor_show_session_configure_page),

    path("<int:sid>/stop/", monitor_stop_session),

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
