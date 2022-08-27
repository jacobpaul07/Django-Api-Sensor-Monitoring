"""
sih_python_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import App.views as views
from App import history_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/readsettings', views.ReadDeviceSettings().as_view()),
    path('api/updatesettings', views.UpdateDeviceSettings().as_view()),
    path('api/readcomsettings', views.ReadDeviceComSettings().as_view()),
    path('api/updatecomsettings', views.UpdateDeviceComSettings().as_view()),

    # Database URLs
    path('api/readspecifictimedata', history_views.ReadHistoryData().as_view()),
    path('api/report', history_views.ReadReport().as_view()),

    path('', views.dashboard, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('device/<str:deviceid>', views.index_test, name='index'),
    path('device', views.index_test, name='index'),
]
