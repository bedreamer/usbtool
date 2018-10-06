# -*- coding: UTF-8 -*-
__author__ = 'lijie'


def get_supported_can_device_list():
    return ['CANUSB-2E-U', 'CANUSB-4E-U']


def get_supported_idx_list(can_model):
    if can_model is None:
        return None
    return [0, 1, 2, 3]


def get_supported_channel_list(can_model):
    if can_model is None:
        return None
    return [0, 1]


def get_supported_bps_list(can_model):
    if can_model is None:
        return None
    return ["100Kbps", "50Kbps"]
