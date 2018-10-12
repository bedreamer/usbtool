# -*- coding: utf8 -*-
import time
import importlib


_session_map = dict()
_session_id = 1


class BMSDriverWrapper:
    def __init__(self, bms_dev, bms_can_profile):
        self.bms_dev = bms_dev
        self.bms_can_profile = bms_can_profile
        self.bms_dev_driver = None

    def run_step_forward(self, request):
        data_pack = {}

        id, model, name = 0, '', ''
        starts_bar_json = {}
        json_body = {"status": starts_bar_json, "data": data_pack}
        return json_body, {}


class MonitorSession:
    def __init__(self, sid, bms_dev, bms_can_profile, modbus_dev, modbus_can_profile):
        self.sid = sid

        self.modbus_dev = modbus_dev
        self.modbus_can_profile = modbus_can_profile

        newline_device = importlib.import_module("ui.newline." + modbus_dev.model)
        self.modbus_dev_driver = newline_device.Driver(self, modbus_dev, modbus_can_profile)

        self.bms_dev = bms_dev
        self.bms_can_profile = bms_can_profile
        self.bms_dev_driver = BMSDriverWrapper(bms_dev, bms_can_profile)

        self.call_counter = 0
        self.birth = time.strftime("%Y-%m-%d %H:%M:%S")
        self.birth_tsp = time.time()

        self.mode = 'panel'

    def set_mode(self, mode):
        self.mode = mode

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

    def get_modbus_dev_driver(self):
        return self.modbus_dev_driver

    def get_bms_dev_driver(self):
        return self.bms_dev_driver.bms_dev_driver

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
