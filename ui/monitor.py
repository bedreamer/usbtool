# -*- coding: UTF-8 -*-
__author__ = 'lijie'
from django.shortcuts import render
from django.http import *
import ui.models as models
import ui.api as api
import random
import json
import time
import math


def monitor_by_session_id(request, sid):
    context = dict()
    session = api.search_session_by_id(sid)
    if session is None:
        return HttpResponseRedirect('/')

    context['bms_model'] = 'BMS'
    context['dev_model'] = session.modbus_dev_model
    context['sid'] = sid
    return render(request, "监控/main.html", context=context)


def respons_json(respons, json_dict):
    respons = HttpResponse(json.dumps(json_dict))
    respons['Context-Type'] = 'application/json'
    return respons


def return_monitor_api_respons_without_error(request, json_dict, **kwargs):
    """
    返回无错误应答
    :param request:
    :param json_dict:
    :param args:
    :return:
    """
    api_respons = {
        'api': request.path,
        'status': 'ok',
        'tsp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'data': json_dict
    }
    for key, value in kwargs.items():
        api_respons[key] = value

    return respons_json(request, api_respons)


def return_monitor_api_respons_with_error(request, reason, json_dict, **kwargs):
    """
    返回有错误应答
    :param request:
    :param reason:
    :param json_dict:
    :param args:
    :return:
    """
    api_respons = {
        'api': request.path,
        'status': 'error',
        'reason': reason,
        'tsp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'data': json_dict
    }
    for key, value in kwargs.items():
        api_respons[key] = value

    return respons_json(request, api_respons)


def return_monitor_redir_to_page(request, reason, href, **kwargs):
    """
    通过API重定向
    :param request:
    :param reason:
    :param kwargs:
    :return:
    """
    return return_monitor_api_respons_with_error(request, reason, None, href=href)


def monitor_json_by_session_id(request, sid):
    session = api.search_session_by_id(sid)
    if session is None:
        reason = "因为使用了无效的会话ID（%d）导致重定向" % sid
        return return_monitor_redir_to_page(request, reason, href='/')

    j = {
        'p1': round(session.get_P1(1), 2),
        'p2': round(session.get_P2(1), 2),
        'f1': round(session.get_F1(1), 2),

        't1': round(session.get_T1(1) * 20, 2),
        't2': round(session.get_T2(1) * 20, 2),
        't3': round(session.get_T3(1) * 20, 2),

        'modbus_tx_count': session.modbus_tx_count,
        'modbus_rx_count': session.modbus_rx_count,

        'modbus_offline': False
    }

    return return_monitor_api_respons_without_error(request, j)
