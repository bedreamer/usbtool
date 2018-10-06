from django.contrib import admin
import ui.models as models


class ModbusRegisterAdmin(admin.TabularInline):
    model = models.ModbusRegister
    extra = 1


# Register your models here.
@admin.register(models.ModbusDevice)
class ModbusDeviceAdmin(admin.ModelAdmin):
    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('id', 'name', 'model')

    list_per_page = 50  # 控制每页显示的对象数量，默认是100
    inlines = [ModbusRegisterAdmin]
