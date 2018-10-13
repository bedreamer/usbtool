# -*- coding: utf8 -*-
import ui.usbcan.gateway.can.api as gateway
import ui.usbcan.gateway.modbus.api as modbus


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


class ModbusCANChannel(object):
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

    def read_register(self, server_address, register_address):
        self.can_frame_tx += 1
        result = modbus.read_register(self.can_channel_handle, server_address, register_address)
        self.can_frame_rx += 1
        return result

    def write_register(self, server_address, register_address, short_value):
        self.can_frame_tx += 1
        result = modbus.write_register(self.can_channel_handle, server_address, register_address, short_value)
        self.can_frame_rx += 1
        return result


class ModbusDriver:
    def __init__(self):
        pass

    def read_register(self, modbus_server_address, register_address):
        """
        读寄存器
        :param modbus_server_address:
        :param register_address:
        :return: short value
        """
        pass

    def write_register(self, modbus_server_address, register_address, short_value):
        """
        写寄存器
        :param modbus_server_address:
        :param register_address:
        :param short_value:
        :return: short value
        """
        pass
