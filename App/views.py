from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from App.index import read_setting, read_com_setting, write_setting, write_com_setting
from App.RTUReaders.modbus_rtu import modbus_rtu
from MongoDB_Main import Document as Doc

import json
import App.globalsettings as appsetting

# Create your views here.
def index(request):
    return render(request, 'index.html')


def index_test(request, deviceid=None):
    return render(request, 'test.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def re(request):
    col="LiveData"
    doc = Doc().read_report(col)
    if len(doc)>0:
        context = {"data":doc}
    else:
        context={"data":"No data"}
    print("t", type(doc))
    return render(request, 'report.html', context)

class StartRtuService(APIView):
    @staticmethod
    def post(request):
        StartRtuService.start_rtu()
        return HttpResponse('success', "application/json")

    @staticmethod
    def start_rtu():
        appsetting.startRtuService = True
        modbus_rtu()

class ReadDeviceSettings(APIView):

    def get(self, request):
        raw_setting = read_setting()
        sensor_list = list(raw_setting["sensors"])
        dumped_setting = json.dumps(sensor_list, indent=4)
        return HttpResponse(dumped_setting, "application/json")

class UpdateDeviceSettings(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        request_data = json.loads(data)

        update_json = {
            "sensors": request_data
        }
        write_setting(update_json)

        
        return HttpResponse("Success", "application/json")

class ReadDeviceComSettings(APIView):

    def get(self, request):
        raw_setting = read_com_setting()
        dumped_setting = json.dumps(raw_setting, indent=4)
        return HttpResponse(dumped_setting, "application/json")

class UpdateDeviceComSettings(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        request_data = json.loads(data)
        print(request_data)
        write_com_setting(request_data)        
        return HttpResponse("Success", "application/json")