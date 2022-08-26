'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys, os              #import system package
from App.Utilities import write_gps_data


class GpsClass:

    def GPS_Info(self):
        try:
            # self.NMEA_buff
            # self.lat_in_degrees
            # self.long_in_degrees
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = self.NMEA_buff[0]                    #extract time from GPGGA string
            nmea_latitude = self.NMEA_buff[1]                #extract latitude from GPGGA string
            nmea_longitude = self.NMEA_buff[3]               #extract longitude from GPGGA string
            
            print("NMEA Time: ", nmea_time,'\n')
            # print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
            # print("lat-lon",nmea_latitude,nmea_longitude)
            if nmea_latitude==0 or nmea_longitude==0:
                print("No GPS DATA in NMEA")
                return None
            lat = float(nmea_latitude)                  #convert string into float for calculation
            longi = float(nmea_longitude)               #convertr string into float for calculation
            
            self.lat_in_degrees = self.convert_to_degrees(lat)    #get latitude in degree decimal format
            self.long_in_degrees = self.convert_to_degrees(longi) #get longitude in degree decimal format

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, f_name, exc_tb.tb_lineno)
            print("Error in GPS_INFO")
        
    #convert raw NMEA string into degree decimal format   
    def convert_to_degrees(self, raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position
        
    def gps_main(self):
        self.gpgga_info = "$GPGGA,"
        self.ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
        self.GPGGA_buffer = 0
        self.NMEA_buff = 0
        self.lat_in_degrees = 0
        self.long_in_degrees = 0
        
        while True:
            try:
                received_data = (str)(self.ser.readline())                   #read NMEA string received
                GPGGA_data_available = received_data.find(self.gpgga_info)   #check for NMEA GPGGA string               
                if (GPGGA_data_available>0):
                    self.GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                    self.NMEA_buff = (self.GPGGA_buffer.split(','))          #store comma separated data in buffer
                    self.GPS_Info()                                          #get time, latitude, longitude
                    if self.lat_in_degrees==0 or self.long_in_degrees==0:
                        print("No GPS DATA")
                        return None

                    print("lat in degrees:", self.lat_in_degrees," long in degree: ", self.long_in_degrees, '\n')
                    lat_str = str(self.lat_in_degrees)
                    long_str = str(self.long_in_degrees)
                    write_gps_data(latitude=lat_str, longitude=long_str)
                    # map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
                    # print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n",map_link)               #press ctrl+c to plot on map and exit 
                    print("------------------------------------------------------------\n")
                    sleep(10)
                                
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, f_name, exc_tb.tb_lineno)
                print("Error in GPS data")

        # except KeyboardInterrupt:
        #     webbrowser.open(map_link)        #open current position information in google map
        #     sys.exit(0)

