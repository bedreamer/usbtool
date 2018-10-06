from django.shortcuts import render
from django.http import *
import ui.models as models
import ui.api as api
# Create your views here.


def startup(request):
    if request.method == 'GET':
        context = dict()

        # --------------------------BMS
        try:
            bms_model = request.GET['bms_model']
        except KeyError:
            bms_model = None
        context['bms_model'] = bms_model
        context['bms_supported_model_list'] = []
        if bms_model is None and isinstance(context['bms_supported_model_list'], list) and len(context['bms_supported_model_list']) > 0:
            context['bms_model'] = context['bms_supported_model_list'][0]

        try:
            bms_can_model = request.GET['bms_can_model']
        except KeyError:
            bms_can_model = None
        context['bms_can_model'] = bms_can_model
        context['bms_supported_can_model_list'] = api.get_supported_can_device_list()

        if bms_can_model is None and isinstance(context['bms_supported_can_model_list'], list) and len(context['bms_supported_can_model_list']) > 0:
            bms_can_model = context['bms_supported_can_model_list'][0]

        try:
            bms_can_idx = int(request.GET['bms_can_idx'])
        except KeyError:
            bms_can_idx = None
        context['bms_can_idx'] = bms_can_idx
        context['bms_can_supported_idx_list'] = api.get_supported_idx_list(bms_can_model)

        try:
            bms_can_channel = int(request.GET['bms_can_channel'])
        except KeyError:
            bms_can_channel = None
        context['bms_can_channel'] = bms_can_channel
        context['bms_can_supported_channel_list'] = api.get_supported_channel_list(bms_can_model)

        try:
            bms_can_bps = request.GET['bms_can_bps']
        except KeyError:
            bms_can_bps = None
        context['bms_can_bps'] = bms_can_bps
        context['bms_supported_bps_list'] = api.get_supported_bps_list(bms_can_model)

        # --------------------------modbus device
        try:
            modbus_dev_model = int(request.GET['modbus_dev_model'])
        except KeyError:
            modbus_dev_model = None
        context['modbus_dev_model'] = modbus_dev_model
        context['modbus_supported_dev_model_list'] = list(models.ModbusDevice.objects.all())
        if modbus_dev_model is None and isinstance(context['modbus_supported_dev_model_list'], list) and len(context['modbus_supported_dev_model_list']) > 0:
            context['modbus_dev_model'] = context['modbus_supported_dev_model_list'][0].id

        try:
            modbus_can_model = request.GET['modbus_can_model']
        except KeyError:
            modbus_can_model = None
        context['modbus_can_model'] = modbus_can_model
        context['modbus_supported_can_model_list'] = api.get_supported_can_device_list()

        if modbus_can_model is None and isinstance(context['modbus_supported_can_model_list'], list) and len(context['modbus_supported_can_model_list']) > 0:
            modbus_can_model = context['modbus_supported_can_model_list'][0]

        try:
            modbus_can_idx = int(request.GET['modbus_can_idx'])
        except KeyError:
            modbus_can_idx = None
        context['modbus_can_idx'] = modbus_can_idx
        context['modbus_can_supported_idx_list'] = api.get_supported_idx_list(modbus_can_model)

        try:
            modbus_can_channel = int(request.GET['modbus_can_channel'])
        except KeyError:
            modbus_can_channel = None
        context['modbus_can_channel'] = modbus_can_channel
        context['modbus_can_supported_channel_list'] = api.get_supported_channel_list(modbus_can_model)

        try:
            modbus_can_bps = request.GET['modbus_can_bps']
        except KeyError:
            modbus_can_bps = None
        context['modbus_can_bps'] = modbus_can_bps
        context['modbus_supported_bps_list'] = api.get_supported_bps_list(modbus_can_model)

        return render(request, "启动页/main.html", context=context)
    else:
        for key, value in request.POST.items():
            print(key, '---', value)

        return HttpResponseRedirect('/monitor/1/')


def show_all_modbusdevice(request):
    dev_list = models.ModbusDevice.objects.all()

    context = dict()
    context['dev_list'] = dev_list
    return render(request, "设备/all.html", context=context)


def new_modbusdevice(request):
    if request.method == 'GET':
        return render(request, "设备/new.html")
    else:
        name = request.POST['name']
        model = request.POST['model']
        if 0 in (len(name), len(model)):
            return render(request, "设备/new.html")

        dev = models.ModbusDevice(name=name, model=model)
        dev.save()

    return HttpResponseRedirect('/modbusdevice/')


def show_modbusdevice_info(request, devid):
    context = dict()
    return render(request, "设备/all.html", context=context)


def edit_modbusdevice_info(request, devid):
    if request.method == 'GET':
        context = dict()
        context['device'] = models.ModbusDevice.objects.get(id=devid)
        context['reg_list'] = models.ModbusRegister.objects.filter(device=devid)
        if len(context['reg_list']) == 0:
            context['reg_list'] = [models.ModbusRegister()]
        return render(request, "设备/edit.html", context=context)
    else:
        return HttpResponseRedirect(request.path)


def delete_modbusdevice_info(request, devid):
    return HttpResponseRedirect('/modbusdevice/')

