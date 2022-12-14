'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial  # import serial pacakge
from time import sleep
from datetime import datetime
import webbrowser  # import package for opening link in browser
from App.SMS.Serial_Input import SerialDevice
import sys
import os  # import system package
from App.Utilities import write_gps_data
from App.MQTT.mqtt_publisher import mqtt_gps_publish
from App.Utilities import read_result_file


class GpsClass:

    def GPS_Info(self):
        try:
            # self.NMEA_buff
            # self.lat_in_degrees
            # self.long_in_degrees
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = self.NMEA_buff[0]  # extract time from GPGGA string
            # extract latitude from GPGGA string
            nmea_latitude = self.NMEA_buff[1]
            # extract longitude from GPGGA string
            nmea_longitude = self.NMEA_buff[3]

            print("NMEA Time: ", nmea_time, '\n')
            # print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
            # print("lat-lon",nmea_latitude,nmea_longitude)
            if nmea_latitude == 0 or nmea_longitude == 0:
                print("No GPS DATA in NMEA")
                return None
            # convert string into float for calculation
            lat = float(nmea_latitude)
            # convertr string into float for calculation
            longi = float(nmea_longitude)

            self.lat_in_degrees = self.convert_to_degrees(
                lat)  # get latitude in degree decimal format
            self.long_in_degrees = self.convert_to_degrees(
                longi)  # get longitude in degree decimal format

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, f_name, exc_tb.tb_lineno)
            print("Error in GPS_INFO")

    # convert raw NMEA string into degree decimal format
    def convert_to_degrees(self, raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" % (position)
        return position

    def gps_main(self):
        self.gpgga_info = "$GPGGA,"
        self.ser = serial.Serial("/dev/ttyS0")  # Open port with baud rate
        self.GPGGA_buffer = 0
        self.NMEA_buff = 0
        self.lat_in_degrees = 0
        self.long_in_degrees = 0

        while True:
            try:
                # read NMEA string received
                received_data = (str)(self.ser.readline())
                GPGGA_data_available = received_data.find(
                    self.gpgga_info)  # check for NMEA GPGGA string
                if (GPGGA_data_available > 0):
                    # store data coming after "$GPGGA," string
                    self.GPGGA_buffer = received_data.split("$GPGGA,", 1)[1]
                    # store comma separated data in buffer
                    self.NMEA_buff = (self.GPGGA_buffer.split(','))
                    self.GPS_Info()  # get time, latitude, longitude
                    if self.lat_in_degrees == 0 or self.long_in_degrees == 0:
                        print("No GPS DATA")
                        return None

                    print("lat in degrees:", self.lat_in_degrees,
                          " long in degree: ", self.long_in_degrees, '\n')
                    lat_str = str(self.lat_in_degrees)
                    long_str = str(self.long_in_degrees)
                    gps_data = {
                        "latitude": lat_str,
                        "longitude": long_str
                    }
                    
                    mqtt_gps_publish(message=gps_data)
                    result_file = read_result_file()
                    now = datetime.now()
                    latitude = result_file['gps_data']['latitude']
                    longitude = result_file['gps_data']['longitude']
                    gps_alert_time = result_file['gps_data']['gps_alert_time']
                    write_gps_data(latitude=lat_str, longitude=long_str, time=gps_alert_time)

                    # Alert GPS Location Data
                    if os.environ["MODE"] != "WAREHOUSE":

                        if gps_alert_time != "":
                            # previous_alert_time_pds = pandas.to_datetime(previous_alert_time)
                            gps_alert_time_pds = datetime.strptime(gps_alert_time, '%Y-%m-%d %H:%M:%S.%f')
                            gps_alert_time_difference = now - gps_alert_time_pds
                            gps_difference_seconds = gps_alert_time_difference.seconds

                        else:
                            gps_difference_seconds = 0
                        
                        if gps_difference_seconds >= 600 or gps_difference_seconds==0:
                            if str(latitude) == str(lat_str) and str(longitude) == str(long_str):
                                tag_name="GPS -"
                                alert_msg = "Device is in the same location"
                                SerialDevice().serial_write(tag_name=tag_name, alert=alert_msg)
                                result_file['gps_data']['gps_alert_time']=str(now)
                    
                    else:
                        if gps_alert_time != "":
                            # previous_alert_time_pds = pandas.to_datetime(previous_alert_time)
                            gps_alert_time_pds = datetime.strptime(gps_alert_time, '%Y-%m-%d %H:%M:%S.%f')
                            gps_alert_time_difference = now - gps_alert_time_pds
                            gps_difference_seconds = gps_alert_time_difference.seconds

                        else:
                            gps_difference_seconds = 0
                        
                        if gps_difference_seconds >= 600 or gps_difference_seconds==0:
                            if str(latitude) != str(lat_str) and str(longitude) != str(long_str):
                                tag_name="GPS -"
                                alert_msg = "Device is in the same location"
                                SerialDevice().serial_write(tag_name=tag_name, alert=alert_msg)
                                result_file['gps_data']['gps_alert_time']=str(now)

                    write_gps_data(latitude=lat_str, longitude=long_str, time=str(now))
                    # map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
                    # print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n",map_link)               #press ctrl+c to plot on map and exit
                    print(
                        "------------------------------------------------------------\n")
                    sleep(10)

            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, f_name, exc_tb.tb_lineno)
                print("Error in GPS data")

        # except KeyboardInterrupt:
        #     webbrowser.open(map_link)        #open current position information in google map
        #     sys.exit(0)
