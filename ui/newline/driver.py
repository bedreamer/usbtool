# -*- coding: utf8 -*-
import random


class YaoceRegister:
    def __init__(self, ui_name, name, address, resolution, unit):
        self.ui_name, self.name, self.address, self.resolution, self.unit = ui_name, name, address, resolution, unit


class YaoxinRegister:
    def __init__(self, ui_name, name, address, bits_map):
        self.ui_name, self.name, self.address, self.bits_map = ui_name, name, address, bits_map


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
            body[reg.ui_name] = modbus_value
        return body

    def read_yaoce(self, modbus_server_address):
        body = dict()
        for reg in self.yaoce_register_list:
            modbus_value = self.modbuscan_channel.read_register(modbus_server_address, reg.address)
            body[reg.ui_name] = modbus_value
        return body
