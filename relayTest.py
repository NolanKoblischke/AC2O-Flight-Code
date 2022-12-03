import Driver.BMP180 as BMP180
import Driver.BMP280 as BMP280
import Driver.camera as camera
import Driver.tempsensors as tempsensors
import time
import sys
import datetime
import Driver.GPIO as gpio
import RPi.GPIO as GPIO_PI
import keyboard
import Services.tempControl as tempControl
import numpy as np
import datetime
import Services.elink as elink
import os


#TODO: light
#TODO: barometer
#TODO: barometer validation
#TODO: Camera
#TODO: pump timing
#TODO: Local logging
#TODO: Messaging with timestamps, gpio states, local logic states of heaters/pumps

#****************************************************************************
#                                  Constants
#****************************************************************************
CAMERA_FRAMERATE = 3
PRESSURE_WARNING_THRESHOLD = 0.8 #TODO: change the values for something reasonable
PRESSURE_EMERGENCY_THRESHOLD = 0.5
PRESSURE_SLOPE_WARNING = 0.6
PRESSURE_SLOPE_EMERGENCY = 0.4
SECONDS_BETWEEN_PHOTOS = 3
SECONDS_BETWEEN_PUMPS = 60
LENGTH_OF_PUMPS_IN_SECONDS = 10
TIME_LIMIT_FOR_ELINK_DISCONNECTS = 20 #Seconds

#TODO: Check if these gpio pins match our actual hardware
HEATER_RELAY_GPIO = 21
PUMP_RELAY_GPIO = 16
LIGHT_RELAY_GPIO = 12

#****************************************************************************
#                                  GPIO SETUP
#****************************************************************************
gpio.init()

heater_relay_gpio = gpio.GPIO_STRUCT(HEATER_RELAY_GPIO, True)  #True means off. False means on. RELAY ONLY!!!

#TODO: implement a is_it_relay variable when creating a struct. So we deal with this inverted logic inside the GPIO.py to avoid confusion
gpio.setup_pin(heater_relay_gpio)
#TODO: Make a comment everytime you change the state of a relay, since they're confusing!

pump_relay_gpio = gpio.GPIO_STRUCT(PUMP_RELAY_GPIO, True)
gpio.setup_pin(pump_relay_gpio)

light_relay_gpio = gpio.GPIO_STRUCT(LIGHT_RELAY_GPIO, True) 
gpio.setup_pin(light_relay_gpio)

#****************************************************************************
#                                  Main Functions
#****************************************************************************

#****************************************************************************
#                                  OS Functions
#****************************************************************************

def graceful_shutdown():
    GPIO_PI.cleanup()

    sys.exit()


if __name__ == '__main__':
    # FOLLOWING CODE RUNS ONLY ONCE #***********************************************************************************************


    while True:
        
        pump_relay_gpio.set_pin_state(False)
        print("pump")
        time.sleep(2)
        pump_relay_gpio.set_pin_state(True)
        
        light_relay_gpio.set_pin_state(False)
        print("light")
        time.sleep(2)
        light_relay_gpio.set_pin_state(True)
        
        heater_relay_gpio.set_pin_state(False)
        print("heater")
        time.sleep(2)
        heater_relay_gpio.set_pin_state(True)
        
        