# -*- coding: utf8 -*-
from ui.monitor import models
import random


class ModBus读供液温度(models.ModBus读供液温度):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读供液温度(models.ModBus读供液温度):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读回液温度(models.ModBus读回液温度):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读制冷输出状态(models.ModBus读制冷输出状态):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读加热输出状态(models.ModBus读加热输出状态):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读循环输出状态(models.ModBus读循环输出状态):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读供液口压力(models.ModBus读供液口压力):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读回液口压力(models.ModBus读回液口压力):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读供液口流量(models.ModBus读供液口流量):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读比例阀开度(models.ModBus读比例阀开度):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读实际设定温度值(models.ModBus读实际设定温度值):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读实际设定流量值(models.ModBus读实际设定流量值):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读取通讯状态(models.ModBus读取通讯状态):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读取状态位(models.ModBus读取状态位):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制设备启动(models.ModBus控制设备启动):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制设备关闭(models.ModBus控制设备关闭):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制排空加液开(models.ModBus控制排空加液开):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制排空加液关(models.ModBus控制排空加液关):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制内循环开(models.ModBus控制内循环开):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制内循环关(models.ModBus控制内循环关):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus设置温度(models.ModBus设置温度):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus设置流量(models.ModBus设置流量):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus设置运行程序号(models.ModBus设置运行程序号):
    def __init__(self):
        super(self.__class__, self).__init__()


class Driver:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.registers = {
            "供液温度": models.RRO(name='供液温度', address=1, resolution=100, signed=True, unit='℃'),
            "回液温度": models.RRO(name='回液温度', address=2, resolution=10, signed=True, unit='℃'),
            "制冷输出": models.RRO(name='制冷输出', address=3),
            "加热输出": models.RRO(name='加热输出', address=4),
            "循环输出": models.RRO(name='循环输出', address=5),
            "供液口压力": models.RRO(name='供液口压力', address=6, resolution=10, signed=True, unit='bar'),
            "比例阀开度": models.RRO(name='比例阀开度', address=7, resolution=10, unit='%'),
            "供液口流量": models.RRO(name='供液口流量', address=8, resolution=100, signed=True, unit='L/min'),
            "实际设定温度": models.RRO(name='实际设定温度', address=9, resolution=100, signed=True, unit='℃'),
            "实际设定流量": models.RRO(name='实际设定流量', address=10, resolution=100, signed=True, unit='L/min'),

            "运行": models.RWO(name='运行', address=11),
            "停止": models.RWO(name='停止', address=12),
            "排空加液开关": models.RWO(name='排空加液开关', address=13),
            "内循环控制": models.RWO(name='内循环控制', address=14),
            "设定温度": models.RWO(name='设定温度', address=15, resolution=100, signed=True, unit='℃'),
            "设定流量": models.RWO(name='设定流量', address=16, resolution=100, signed=True, unit='L/min'),
            "通讯信号判断": models.RWO(name='通讯信号判断', address=17),
        }

    def read_yaoxin(self):
        pass

    def read_yaoce(self):
        pass

    def write_yaokong(self):
        pass

    def write_yaotiao(self):
        pass

    def run_step_forward(self, request):
        return {
            'p1': random.randrange(0, 3),
            'p2': random.randrange(0, 3),
            'f1': random.randrange(0, 3),

            't1': random.randrange(0, 100),
            't2': random.randrange(0, 100),
            't3': random.randrange(0, 100),
        }

    def get_supported_registers_map(self):
        return self.registers

    def get_supported_registers_json(self, request):
        return list(self.registers.keys()), {}

    def read_register(self, request, reg):
        return 0, {}

    def write_register(self, request, reg, str_val):
        return 0, {}

