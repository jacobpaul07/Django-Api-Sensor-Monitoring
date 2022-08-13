import os
import threading
from django.apps import AppConfig
from App.MQTT.mqtt_subscribe import mqtt_subscribe
from App.views import StartRtuService


class MyAppConfig(AppConfig):
    name = "sih_python_django"
    started = False

    def ready(self):
        if not self.started:
            self.started = True
            print("Agent Started at Origin")
            if os.environ['APPLICATION_MODE'] == "web":
                thread = threading.Thread(target=mqtt_subscribe, args=())
                thread.start()
                # thread = threading.Thread(target=socket_listener, args=())
                # thread.start()
            else:
                StartRtuService.start_rtu()
