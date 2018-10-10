from django.shortcuts import render
from django.http import *
import ui.models as models
import ui.monitor.api as api
import ui.monitor.models
import ui.monitor.session
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

        try:
            bms_can_profile = ui.monitor.models.CANProfile(request.POST['bms_can_model'], int(request.POST['bms_can_idx']),
                                                       int(request.POST['bms_can_channel']), request.POST['bms_can_bps'])
            modbus_can_profile = ui.monitor.models.CANProfile(request.POST['modbus_can_model'], int(request.POST['modbus_can_idx']),
                                                       int(request.POST['modbus_can_channel']), request.POST['modbus_can_bps'])

            bms_dev = None
            modbus_dev = models.ModbusDevice.objects.get(id=int(request.POST['modbus_dev_model']))
            session = ui.monitor.session.get_session_by_profiles(bms_dev, bms_can_profile, modbus_dev, modbus_can_profile)
        except Exception as e:
            print("打开通道失败!", e)
            return HttpResponseRedirect("/?e=%s" % str(e))

        return HttpResponseRedirect('/monitor/%d/' % session.get_id())

