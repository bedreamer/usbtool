# -*- coding: UTF-8 -*-
__author__ = 'lijie'
import urllib
import json
import ui.usbcan.gateway.can.api as gateway
import ui.usbcan.gateway.modbus.api as modbus


get_supported_can_device_list = gateway.get_supported_model_list
get_supported_bps_list = gateway.get_device_bps_by_model


def get_supported_idx_list(can_model):
    if can_model is None:
        return None
    return [0, 1, 2, 3]


def get_supported_channel_list(can_model):
    if can_model is None:
        return None
    return [0, 1]


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
        self.modbus_can_dev_handle = None
        self.modbus_channel_handle = None

        self.modbus_tx_count = 0
        self.modbus_rx_count = 0

        self.offline = True

    def get_sid(self):
        return self.sid

    def open(self):
        dev_handle = gateway.open_device_by_model(self.modbus_can_model, self.modbus_can_idx)
        if dev_handle in {-1, 0, None}:
            raise ValueError('打开设备失败')

        channel_handle = gateway.open_channel(dev_handle, self.modbus_can_channel, self.modbus_can_bps)
        if channel_handle in {-1, 0, None}:
            raise ValueError('打开通道失败')

        self.modbus_can_dev_handle = dev_handle
        self.modbus_channel_handle = channel_handle

        return self

    def modbus_x03_read(self, server_address, register_address):
        self.modbus_tx_count += 1
        result = modbus.read_register(self.modbus_channel_handle, server_address, register_address)
        self.modbus_rx_count += 1
        return result

    def modbus_x06_write(self, server_address, register_address, value):
        return 0

    def get_T1(self, server_address):
        v = self.modbus_x03_read(server_address, 1)
        return v/100.0 if v else 0

    def get_T2(self, server_address):
        v = self.modbus_x03_read(server_address, 2)
        return v/100.0 if v else 0

    def get_T3(self, server_address):
        return 0

    def get_P1(self, server_address):
        v = self.modbus_x03_read(server_address, 6)
        return v/100.0 if v else 0

    def get_P2(self, server_address):
        v = self.modbus_x03_read(server_address, 7)
        return v/100.0 if v else 0

    def get_F1(self, server_address):
        v = self.modbus_x03_read(server_address, 8)
        return v/100.0 if v else 0


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
        return session

    # 新建一个转换会话
    session = ConversionSession(_session_id, bms_can_model, bms_can_idx, bms_can_channel, bms_can_bps,
                        modbus_dev_model, modbus_can_model, modbus_can_idx, modbus_can_channel, modbus_can_bps)

    # 打开失败会抛出异常，在上层处理。
    session.open()
    _session_id += 1

    _session_list[ str(session.sid) ] = session
    return session


def search_session_by_id(sid):
    global _session_list

    if str(sid) in _session_list:
        return _session_list[str(sid)]

    return None
