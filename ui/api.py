# -*- coding: UTF-8 -*-
__author__ = 'lijie'
import urllib
import json

"""
httpd.route("^/can/usbcan/supported/$", view.get_supported_usbcan_list)

httpd.route("^/can/usbcan/open/$", view.open_usbcan_device)
httpd.route("^/can/usbcan/close/$", view.close_usbcan_device)
httpd.route("^/can/usbcan/bps/$", view.get_supported_bps_list)

httpd.route("^/can/usbcan/channel/open/$", view.open_usbcan_channel)
httpd.route("^/can/usbcan/channel/close/$", view.close_usbcan_channel)

httpd.route("^/can/usbcan/modbus/x03/$", view.can_modbus_read)
httpd.route("^/can/usbcan/modbus/x06/$", view.can_modbus_write)
"""


def gateway_read(path):
    host = '192.168.2.103:8080'
    try:
        handle = urllib.request.urlopen('http://' + host + path)
        result = json.loads(handle.read())
        print("request on", host, path, "<<<", result)
    except Exception as e:
        print(e)
        result = None

    return result


def get_supported_can_device_list():
    result = gateway_read('/can/usbcan/supported/')
    if isinstance(result, dict) and 'status' in result and 'data' in result and result['status'] == 'ok':
        return result['data']
    return list()


def get_supported_idx_list(can_model):
    if can_model is None:
        return None
    return [0, 1, 2, 3]


def get_supported_channel_list(can_model):
    if can_model is None:
        return None
    return [0, 1]


def get_supported_bps_list(can_model):
    if can_model is None:
        return None
    result = gateway_read('/can/usbcan/bps/?model=%s' % can_model)
    if isinstance(result, dict) and 'status' in result and 'data' in result and result['status'] == 'ok':
        return result['data']
    return None


# 会话列表
_session_list = dict()
_session_id = 1


class ConversionSession:
    def __init__(self, sid, bms_can_model, bms_can_idx, bms_can_channel, bms_can_bps,
                        modbus_dev_model, modbus_can_model, modbus_can_idx, modbus_can_channel, modbus_can_bps):
        self.sid = sid

        self.modbus_dev_model = modbus_dev_model
        self.modbus_can_model = modbus_can_model
        self.modbus_can_idx = modbus_can_idx
        self.modbus_can_channel = modbus_can_channel
        self.modbus_can_bps = modbus_can_bps

        self.modbus_can_dev_handle = self.open_modbus_can_device(modbus_can_model, modbus_can_idx)
        self.modbus_channel_handle = self.open_modbus_can_channel(self.modbus_can_dev_handle, modbus_can_channel, modbus_can_bps)
        self.modbus_dev_offline = True

        if self.modbus_channel_handle is not None:
            self.modbus_dev_offline = False

    def open_modbus_can_device(self, modbus_can_model, modbus_can_idx):
        result = gateway_read('/can/usbcan/open/?model=%s&dev_idx=%d' % (modbus_can_model, modbus_can_idx))

        if isinstance(result, dict) and 'status' in result and 'data' in result and result['status'] == 'ok':
            return result['data']
        return None

    def open_modbus_can_channel(self, modbus_can_dev_handle, modbus_can_channel, modbus_can_bps):
        result = gateway_read('/can/usbcan/channel/open/?device_handle=%s&channel_number=%d&bps=%s' % (modbus_can_dev_handle, modbus_can_channel, modbus_can_bps))

        if isinstance(result, dict) and 'status' in result and 'data' in result and result['status'] == 'ok':
            return result['data']
        return None

    def modbus_x03_read(self, server_address, register_address):
        result = gateway_read('/can/usbcan/modbus/x03/?channel_handle=%s&server_address=%d&register_address=%d' % (self.modbus_channel_handle, server_address, register_address))

        if isinstance(result, dict) and 'status' in result and 'data' in result and result['status'] == 'ok':
            return result['data']
        return None

    def modbus_x06_write(self, server_address, register_address, value):
        return 0

    def get_T1(self, server_address):
        v = self.modbus_x03_read(server_address, 1)
        return v['value']/100.0 if v else 0

    def get_T2(self, server_address):
        v = self.modbus_x03_read(server_address, 2)
        return v['value']/100.0 if v else 0

    def get_T3(self, server_address):
        return 0

    def get_P1(self, server_address):
        v = self.modbus_x03_read(server_address, 6)
        return v['value']/100.0 if v else 0

    def get_P2(self, server_address):
        v = self.modbus_x03_read(server_address, 7)
        return v['value']/100.0 if v else 0

    def get_F1(self, server_address):
        v = self.modbus_x03_read(server_address, 8)
        return v['value']/100.0 if v else 0


def get_convert_session(bms_can_model, bms_can_idx, bms_can_channel, bms_can_bps,
                        modbus_dev_model, modbus_can_model, modbus_can_idx, modbus_can_channel, modbus_can_bps):
    global _session_list
    global _session_id

    for _, session in _session_list.items():
        if session.modbus_dev_model != modbus_dev_model:
            continue
        if session.modbus_can_model != modbus_can_model:
            continue
        if session.modbus_can_idx != modbus_can_idx:
            continue
        if session.modbus_can_channel != modbus_can_channel:
            continue

        # 当前设备的当前通道已经打开了
        return session.sid

    # 新建一个转换会话
    session = ConversionSession(_session_id, bms_can_model, bms_can_idx, bms_can_channel, bms_can_bps,
                        modbus_dev_model, modbus_can_model, modbus_can_idx, modbus_can_channel, modbus_can_bps)
    _session_id += 1

    _session_list[ str(session.sid) ] = session
    return session.sid


def search_session_by_id(sid):
    global _session_list

    if str(sid) in _session_list:
        return _session_list[str(sid)]

    return None
