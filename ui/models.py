# -*- coding: utf8 -*-
from django.db import models


# Create your models here.
class BMSDevice(models.Model):
    name = models.CharField(default='', max_length=30, help_text="设备名称")
    model = models.CharField(default='', max_length=30, help_text="设备型号")

    def __str__(self):
        return "BMS设备"


# Create your models here.
class ModbusDevice(models.Model):
    name = models.CharField(default='', max_length=30, help_text="设备名称")
    model = models.CharField(default='', max_length=30, help_text="设备型号")

    def __str__(self):
        return "Modbus设备"


class ModbusRegister(models.Model):
    device = models.ForeignKey(ModbusDevice, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, help_text="寄存器名称")

    supported_x03 = models.BooleanField(default=True, help_text="是否支持0x03功能码")
    supported_x06 = models.BooleanField(default=False, help_text="是否支持0x06功能码")

    address = models.IntegerField(default=0, help_text="地址")
    unit = models.CharField(max_length=10, blank=True, default='', help_text="单位")

    resolution = models.IntegerField(default=1, help_text="精度, x1, x10, x100")
    signed = models.BooleanField(default=False, help_text="是否有符号")

    def __str__(self):
        return "Modbus寄存器"


class Profiles(models.Model):
    name = models.CharField(max_length=100, help_text="配置名称")

    bms_model = models.CharField(max_length=100, blank=True, help_text="BMS设备型号")
    bms_can_model = models.CharField(max_length=100, blank=True, help_text="BMS-CAN设备型号")
    bms_can_idx = models.IntegerField(default=0, help_text="BMS-CAN设备索引号")
    bms_can_channel = models.IntegerField(default=0, help_text="BMS-CAN设备通道")
    bms_can_bps = models.CharField(max_length=30, help_text="BMS-CAN设备波特率")

    modbus_model = models.CharField(max_length=100, blank=True, help_text="MODBUS设备型号")
    modbus_can_model = models.CharField(max_length=100, blank=True, help_text="MODBUS-CAN设备型号")
    modbus_can_idx = models.IntegerField(default=0, help_text="MODBUS-CAN设备索引号")
    modbus_can_channel = models.IntegerField(default=0, help_text="MODBUS-CAN设备通道")
    modbus_can_bps = models.CharField(max_length=30, help_text="MODBUS-CAN设备波特率")


# Create your models here.
class YaoceData(models.Model):
    server_address = models.IntegerField(help_text="modbus 服务器地址")
    tsp = models.DateTimeField(default="2018-01-01 00:00:00", help_text="记录时戳")

    txt = models.TextField(help_text="json数据")
