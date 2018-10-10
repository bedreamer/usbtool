# -*- coding: utf8 -*-
from ui.models import *


class NewLineDevice(object):
    def __init__(self, id):
        self.model = ModbusDevice.objects.get(id=id)
        self.regs = ModbusRegister.objects.filter(device=id)

    def 运行(self):
        """
        启动
        :return:
        """
        pass

    def 停止(self):
        """
        停止
        :return:
        """
        pass

    def 排空加液开关(self):
        pass

    def 内循环控制(self):
        pass

    def 设定温度(self):
        pass

    def 设定流量(self):
        pass

