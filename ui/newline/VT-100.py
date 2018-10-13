# -*- coding: utf8 -*-
from ui.monitor import models
import random
import ui.newline.driver as driver
from ui.models import YaoceData
import json
import time
import datetime


__model__ = 'VT-100'
__sections_template_map__ = {
    'model_恒温恒流设备_状态表区': "监控/%s/model-状态表区.html" % __model__,
    'model_恒温恒流设备_温度计区': "监控/%s/model-温度计区.html" % __model__,
    'model_恒温恒流设备_仪表盘区': "监控/%s/model-仪表盘区.html" % __model__,
    'model_恒温恒流设备_控制区': "监控/%s/model-控制区.html" % __model__,
    'model_恒温恒流设备_故障显示区': "监控/%s/model-故障显示区.html" % __model__
}

class Driver(driver.ModbusDeviceDriver):
    def __init__(self, session, modbus_dev, modbus_can_profile):
        self.modbus_channel = models.ModbusCANChannel(modbus_can_profile)
        self.session = session
        self.dev = modbus_dev
        super(self.__class__, self).__init__("恒温恒流设备", __model__, self.modbus_channel, session, modbus_dev)

        word_bits_map = [
                    ("", ""),
                    ("", ""),
                    ("", ""),
                    ("", ""),
                    ("", ""),
                    ("", ""),
                    ("", ""),
                    ("", ""),
                    ("", "回液温度传感器或控温模块故障"),
                    ("", "供液温度传感器或控温模块故障"),
                    ("", "压缩机高温报警"),
                    ("", "压缩机低压报警"),
                    ("", "压缩机高压报警"),
                    ("", "低液位保护"),
                    ("", "供液压力超压报警"),
                    ("", ""),
        ]
        self.create_yaoxin_register(ui_name="errors", name='输出故障报警', address=0, bits_map=word_bits_map)

        self.create_yaoce_register(ui_name="t1", name='供液温度', address=1, resolution=100, unit='℃')
        self.create_yaoce_register(ui_name="t2", name='回液温度', address=2, resolution=10, unit='℃')

        self.create_yaoce_register(ui_name="s1", name='制冷输出', address=3)
        self.create_yaoce_register(ui_name="s2", name='加热输出', address=4)
        self.create_yaoce_register(ui_name="s3", name='循环输出', address=5)

        self.create_yaoce_register(ui_name="p1", name='供液口压力', address=6, resolution=100, unit='bar')
        self.create_yaoce_register(ui_name="p2", name='回液口压力', address=7, resolution=100, unit='bar')
        self.create_yaoce_register(ui_name="f1", name='供液口流量', address=8, resolution=10, unit='L/min')

        self.create_yaokong_register(ui_name="k1", name='运行', address=9)
        self.create_yaokong_register(ui_name="k2", name='停止', address=10)
        self.create_yaokong_register(ui_name="k3", name='排空加液开', address=11)
        self.create_yaokong_register(ui_name="k4", name='排空加液关', address=12)

        self.create_yaotiao_register(ui_name="set_t", name='设定温度', address=13, resolution=100, unit='℃')
        self.create_yaotiao_register(ui_name="set_l", name='设定流量', address=14, resolution=100, unit='L/min')
        self.create_yaotiao_register(ui_name="x1", name='控制运行程序号', address=15)
        self.create_yaokong_register(ui_name="x2", name='内循环控制', address=16)

    def run_step_forward(self, request):
        modbus_server_address = 1
        yaoxin = self.read_all_yaoxin(modbus_server_address)
        yaoce = self.read_all_yaoce(modbus_server_address)

        yaoce_json = json.dumps(yaoce)
        now = datetime.datetime.now()
        record = YaoceData(server_address=modbus_server_address, tsp=now, txt=yaoce_json)
        record.save()

        pack = {
            "data": dict(yaoce, **yaoxin),
            "status": self.modbus_channel.get_can_channel_status_bar_json(self.dev.id, self.dev.model, self.dev.name)
        }
        return pack, {}

    def get_template(self, section_name):
        return __sections_template_map__[section_name]

    def get_supported_registers_map(self):
        return self.registers

    def get_supported_registers_json(self, request):
        return list(self.registers.keys()), {}

    def read_register(self, request, reg):
        return 0, {}

    def write_register(self, request, reg, str_val):
        return 0, {}

