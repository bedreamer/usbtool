# -*- coding: utf8 -*-
import ui.usbcan.gateway.can.api as gateway
import ui.usbcan.gateway.modbus.api as modbus


_session_map = dict()
_session_id = 1


class MonitorSession:
    def __init__(self, sid, bms_dev, bms_can_profile, modbus_dev, modbus_can_profile):
        self.sid = sid

        self.modbus_dev = modbus_dev
        self.modbus_can_profile = modbus_can_profile

        self.bms_dev = bms_dev
        self.bms_can_profile = bms_can_profile

    def open(self):
        can_model, can_idx = self.modbus_can_profile.can_model, self.modbus_can_profile.can_idx
        dev_handle = gateway.open_device_by_model(can_model, can_idx)
        if dev_handle in {-1, 0, None}:
            raise ValueError('打开设备失败')

        can_channel, can_bps = self.modbus_can_profile.can_channel_idx, self.modbus_can_profile.bps
        channel_handle = gateway.open_channel(dev_handle, can_channel, can_bps)
        if channel_handle in {-1, 0, None}:
            raise ValueError('打开通道失败')

        self.modbus_can_dev_handle = dev_handle
        self.modbus_channel_handle = channel_handle

        return self

    def run_step_forward(self):
        j = {
            'p1': 0,
            'p2': 0,
            'f1': 0,

            't1': 0,
            't2': 0,
            't3': 0,

            'modbus_tx_count': 0,
            'modbus_rx_count': 0,

            'modbus_offline': False
        }
        return j

    def get_id(self):
        return self.sid

    def start(self):
        pass

    def stop(self):
        pass


def get_session_by_profiles(bms_dev, bms_can_profile, modbus_dev, modbus_can_profile):
    global _session_map, _session_id

    for _, session in _session_map.items():
        if session.modbus_can_profile == modbus_can_profile:
            if session.bms_can_profile == bms_can_profile:
                return session
            else:
                raise ValueError("BMS-can 通道已经被打开了!")
        elif session.bms_can_profile == bms_can_profile:
            if session.modbus_can_profile == modbus_can_profile:
                return session
            else:
                raise ValueError("MODBUS-can 通道已经被打开了!")
        else:
            continue

    if bms_can_profile == modbus_can_profile:
        raise ValueError("BMS-can 和 MODBUS-can 不能公用同一个通道!")

    session = MonitorSession(_session_id, bms_dev, bms_can_profile, modbus_dev, modbus_can_profile)
    # 如果打开失败的话会跳出这个函数调用
    session.open()

    _session_map[ str(_session_id) ] = session
    _session_id += 1

    return session


def get_session_by_id(id):
    global _session_map
    try:
        return _session_map[str(id)]
    except:
        return None
