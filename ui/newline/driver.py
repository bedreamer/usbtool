# -*- coding: utf8 -*-
import random
import struct


class YaoceRegister:
    def __init__(self, ui_name, name, address, resolution, unit):
        self.ui_name, self.name, self.address, self.resolution, self.unit = ui_name, name, address, resolution, unit

    def complie_modbus_value(self, display_value):
        pass

    def complie_display_value(self, modbus_value):
        if modbus_value & 0x8000 == 0x8000:
            x = struct.pack(">h", modbus_value)
            modbus_value = struct.unpack(">h", x)[0]

        if self.resolution == 10:
            return round(modbus_value/10.0, 1)
        elif self.resolution == 100:
            return round(modbus_value/100.0, 2)
        else:
            return modbus_value


class YaoxinRegister:
    def __init__(self, ui_name, name, address, bits_map):
        self.ui_name, self.name, self.address, self.bits_map = ui_name, name, address, bits_map

    def complie_display_value(self, modbus_value):
        yaoxin = list()
        x = bin(modbus_value)[2:]
        padding = '0' * (16 - len(x))
        str_bg = ''.join([padding, x])
        str_zero_order = str_bg[::-1]

        yaoxin.append(str_zero_order)

        for idx, ch in enumerate(str_zero_order):
            negtive, positive = self.bits_map[idx]
            if ch == '0' and negtive not in {'', None}:
                yaoxin.append(negtive)
            elif ch == '1' and positive not in {'', None}:
                yaoxin.append(positive)
            else:
                pass

        return yaoxin


class ModbusDeviceDriver(object):
    def __init__(self, name, model, modbuscan_channel, session, device):
        self.name = name
        self.model = model
        self.modbuscan_channel = modbuscan_channel
        self.session = session
        self.device = device

        self.yaoce_register_list = list()
        self.yaoxin_register_list = list()

    def bind(self, page, sector, template):
        pass

    def create_yaoce_register(self, ui_name, name, address, resolution=None, unit=None):
        """
        创建遥测值寄存器
        :param name:
        :param address:
        :param resolution:
        :param unit:
        :return:
        """
        reg = YaoceRegister(ui_name, name, address, resolution if resolution is not None else 1, unit if unit is not None else '')
        self.yaoce_register_list.append(reg)

    def create_yaokong_register(self, ui_name, name, address):
        """
        创建遥控值寄存器
        :param name:
        :param address:
        :return:
        """
        pass

    def create_yaotiao_register(self, ui_name, name, address, resolution=None, unit=None):
        """
        创建遥调值寄存器
        :param name:
        :param address:
        :param resolution:
        :param unit:
        :return:
        """
        pass

    def create_yaoxin_register(self, ui_name, name, address, bits_map):
        """
        创建遥信值寄存器
        :param name:
        :param address:
        :param bits_map:
        :return:
        """
        reg = YaoxinRegister(ui_name, name, address, bits_map)
        self.yaoxin_register_list.append(reg)

    def read_yaoxin(self, modbus_server_address):
        body = dict()
        for reg in self.yaoxin_register_list:
            modbus_value = self.modbuscan_channel.read_register(modbus_server_address, reg.address)
            body[reg.ui_name] = reg.complie_display_value(modbus_value)
        return body

    def read_yaoce(self, modbus_server_address):
        body = dict()
        for reg in self.yaoce_register_list:
            modbus_value = self.modbuscan_channel.read_register(modbus_server_address, reg.address)
            body[reg.ui_name] = reg.complie_display_value(modbus_value)
        return body
