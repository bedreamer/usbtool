# -*- coding: utf8 -*-


class ModbusFunctionBasic(object):
    def __init__(self):
        self.function_name = self.__class__.__name__.strip('ModBus')


class ModBus读供液温度(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读回液温度(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读制冷输出状态(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读加热输出状态(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读循环输出状态(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读供液口压力(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读回液口压力(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读供液口流量(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读比例阀开度(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读实际设定温度值(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读实际设定流量值(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读取通讯状态(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus读取状态位(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制设备启动(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制设备关闭(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制排空加液开(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制排空加液关(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制内循环开(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus控制内循环关(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus设置温度(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus设置流量(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class ModBus设置运行程序号(ModbusFunctionBasic):
    def __init__(self):
        super(self.__class__, self).__init__()


class CANProfile:
    """
    CAN通道配置数据
    """
    def __init__(self, can_model, can_idx, can_channel_idx, bps):
        self.can_model = can_model
        self.can_idx = can_idx
        self.can_channel_idx = can_channel_idx
        self.bps = bps

    def __str__(self):
        return "<%s:%s_%d.ch_%d@%s>" % \
               (self.__class__.__name__, self.can_model, self.can_idx, self.can_channel_idx, self.bps)

    def __eq__(self, other):
        if self.can_model != other.can_model:
            return False
        if self.can_idx != other.can_idx:
            return False
        if self.can_channel_idx != other.can_channel_idx:
            return False

        return True


class CANChannel:
    """
    CAN通信通道
    """
    def __init__(self):
        pass


class ModbusChannel:
    def __init__(self):
        pass
