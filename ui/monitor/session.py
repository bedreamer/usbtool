# -*- coding: utf8 -*-
import time
import importlib
import ui.usbcan.gateway.can.api as gateway
import ui.usbcan.gateway.modbus.api as modbus


_session_map = dict()
_session_id = 1


class CANChannel(object):
    def __init__(self, can_profile):
        self.can_profile = can_profile
        can_model, can_idx = self.can_profile.can_model, self.can_profile.can_idx
        dev_handle = gateway.open_device_by_model(can_model, can_idx)
        if dev_handle in {-1, 0, None}:
            raise ValueError('打开设备失败')

        can_channel, can_bps = self.can_profile.can_channel_idx, self.can_profile.bps
        channel_handle = gateway.open_channel(dev_handle, can_channel, can_bps)
        if channel_handle in {-1, 0, None}:
            raise ValueError('打开通道失败')

        self.can_dev_handle = dev_handle
        self.can_channel_handle = channel_handle

        self.can_frame_tx = 0
        self.can_frame_rx = 0
        self.offline = True

    def get_can_channel_status_bar_json(self, dev_id, dev_model, dev_name):
        return {
            'can_model': self.can_profile.can_model,
            'can_idx': self.can_profile.can_channel_idx,
            'can_ch_idx': self.can_profile.can_channel_idx,
            'can_bps': self.can_profile.bps,
            'can_dev_handle': self.can_dev_handle,
            'can_ch_handle': self.can_channel_handle,
            'offline': self.offline,
            'tx_count': self.can_frame_tx,
            'rx_count': self.can_frame_rx,
            'dev_model': dev_model,
            'dev_id': dev_id,
            'dev_name': dev_name
        }


class ModbusDevDriverWrapper(CANChannel):
    def __init__(self, modbus_dev, modbus_can_profile):
        super(self.__class__, self).__init__(modbus_can_profile)
        self.modbus_dev = modbus_dev
        self.modbus_can_profile = modbus_can_profile
        model = importlib.import_module("ui.newline." + modbus_dev.model)
        self.modbus_dev_driver = model.Driver(self)

        self.offline = False

    def run_step_forward(self, request):
        data_pack = self.modbus_dev_driver.run_step_forward(request)
        id, model, name = self.modbus_dev.id, self.modbus_dev.model, self.modbus_dev.name
        starts_bar_json = self.get_can_channel_status_bar_json(id, model, name)
        json_body = {"status": starts_bar_json, "data": data_pack}
        return json_body, {}

    def get_supported_registers_map(self):
        return self.modbus_dev_driver.get_supported_registers_map()

    def get_supported_registers_json(self, request):
        return self.modbus_dev_driver.get_supported_registers_json(request)

    def read_register(self, request, reg):
        return self.modbus_dev_driver.read_register(request, reg)

    def write_register(self, request, reg, str_val):
        return self.modbus_dev_driver.write_register(request, reg, str_val)


class BMSDriverWrapper(CANChannel):
    def __init__(self, bms_dev, bms_can_profile):
        super(self.__class__, self).__init__(bms_can_profile)
        self.bms_dev = bms_dev
        self.bms_can_profile = bms_can_profile

    def run_step_forward(self, request):
        data_pack = {}

        id, model, name = 0, '', ''
        starts_bar_json = self.get_can_channel_status_bar_json(id, model, name)
        json_body = {"status": starts_bar_json, "data": data_pack}
        return json_body, {}


class MonitorSession:
    def __init__(self, sid, bms_dev, bms_can_profile, modbus_dev, modbus_can_profile):
        self.sid = sid

        self.modbus_dev = modbus_dev
        self.modbus_can_profile = modbus_can_profile

        self.modbus_dev_driver = ModbusDevDriverWrapper(modbus_dev, modbus_can_profile)

        self.bms_dev = bms_dev
        self.bms_can_profile = bms_can_profile
        self.bms_dev_driver = BMSDriverWrapper(bms_dev, bms_can_profile)

        self.call_counter = 0
        self.birth = time.strftime("%Y-%m-%d %H:%M:%S")
        self.birth_tsp = time.time()

    def run_step_forward(self, request):
        self.call_counter += 1

        session_json_ext = {
            "counter": self.call_counter,
            "born": self.birth,
            "live": round(time.time() - self.birth_tsp, 3),
            "sid": self.get_id()
        }

        bms_body, bms_ext = self.bms_dev_driver.run_step_forward(request)
        dev_body, dev_ext = self.modbus_dev_driver.run_step_forward(request)
        session_json_body = {
            "bms": bms_body,
            "dev": dev_body
        }

        merge_ext = dict(bms_ext, **dev_ext)
        return session_json_body, dict(session_json_ext, **merge_ext)

    def get_id(self):
        return self.sid

    def start(self):
        pass

    def stop(self):
        pass

    def get_supported_registers_map(self):
        return self.modbus_dev_driver.get_supported_registers_map()

    def get_supported_registers_json(self, request):
        return self.modbus_dev_driver.get_supported_registers_json(request)

    def read_register(self, request, reg):
        return self.modbus_dev_driver.read_register(request, reg)

    def write_register(self, request, reg, str_val):
        return self.modbus_dev_driver.write_register(request, reg, str_val)

    def get_modbus_dev(self):
        return self.modbus_dev

    def get_bms_dev(self):
        return self.bms_dev


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

    # 如果打开失败的话会跳出这个函数调用
    session = MonitorSession(_session_id, bms_dev, bms_can_profile, modbus_dev, modbus_can_profile)

    _session_map[ str(_session_id) ] = session
    _session_id += 1

    return session


def get_session_by_id(id):
    global _session_map
    try:
        return _session_map[str(id)]
    except:
        return None
