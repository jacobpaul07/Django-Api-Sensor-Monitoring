from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from MongoDB_Main import Document as Doc

import os, sys
import json


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

class ReadReport(APIView):

    def get(self,request):
        col="LiveData"
        doc = Doc().read_report(col)
        json_data = json.dumps(doc)
        return HttpResponse(json_data, "application/json")