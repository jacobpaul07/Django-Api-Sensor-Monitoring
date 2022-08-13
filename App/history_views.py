from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.views import APIView
from App.index import read_setting, read_com_setting, write_setting
from App.RTUReaders.modbus_rtu import modbus_rtu
from MongoDB_Main import Document as Doc

import os, sys
import json
import App.globalsettings as appsetting

class ReadHistoryData(APIView):

    def get(self, request):
        try:
            date_time = request.GET.get("date")
            db_log = Doc().SpecificDate_Document(
                Timestamp=date_time, 
                filterField="last_updated_timestamp",
                col="LiveData"
                ) 
            if db_log:
                return HttpResponse(json.dumps(db_log, indent=4, default=str), "application/json")
            else:
                bad_response = "No Data Available"
                print(bad_response)
                return HttpResponseBadRequest(bad_response)      
        except Exception as ex:
            print("Exception occured in Read_History_Data:", ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, f_name, exc_tb.tb_lineno)
    