"""usbtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import ui.views as view
import ui.monitor as m

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", view.startup),

    path("modbusdevice/", view.show_all_modbusdevice),
    path("modbusdevice/new/", view.new_modbusdevice),
    path("modbusdevice/<int:devid>/", view.show_modbusdevice_info),
    path("modbusdevice/<int:devid>/edit/", view.edit_modbusdevice_info),
    path("modbusdevice/<int:devid>/delete/", view.delete_modbusdevice_info),

    path("monitor/<int:sid>/", m.monitor_by_session_id),
    path("json/monitor/<int:sid>/", m.monitor_json_by_session_id),
]
