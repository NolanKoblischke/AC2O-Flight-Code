import os
import RPi.GPIO as GPIO
import glob
import time


# https://pimylifeup.com/raspberry-pi-temperature-sensor/
# Default port is 4


class newTempSensor:

    def __init__(self, sensorID=0):
        try:
            os.system('modprobe w1-gpio')  # Enabling 1-Wire connection to the GPIO pins
            os.system('modprobe w1-therm')  # Enabling 1-Wire connection to the Thermometer

            self.base_dir = '/sys/bus/w1/devices/'  # Changing directory
            self.device_folder = glob.glob(self.base_dir + '28*')[sensorID]  # Identifying Thermometer file
            self.device_file = self.device_folder + '/w1_slave'
        except IndexError:
            print("Initialization Error: Temp Sensor Missing")
        self.tempArray = []

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def getReading(self):
        """
        Returns a temperature in Celsius from Temp Sensor
        """
        lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')  # Finding the position of 't='
        if equals_pos != -1:  # If 't=' exists in lines then:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            self.tempArray.append(temp_c)
            return temp_c
