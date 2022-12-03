import RPi.GPIO as GPIO_PI
import Driver.GPIO as gpio
import sys

#****************************************************************************
#                                  Constants
#****************************************************************************
HEATER_RELAY_GPIO = 21
PUMP_RELAY_GPIO = 16
LIGHT_RELAY_GPIO = 12

#****************************************************************************
#                                  GPIO SETUP
#****************************************************************************

GPIO_PI.setmode(GPIO_PI.BCM)
GPIO_PI.setwarnings(False)

heater_relay_gpio = gpio.GPIO_STRUCT(HEATER_RELAY_GPIO, True)  #True means off. False means on. RELAY ONLY!!!
gpio.setup_pin(heater_relay_gpio)
pump_relay_gpio = gpio.GPIO_STRUCT(PUMP_RELAY_GPIO, True)
gpio.setup_pin(pump_relay_gpio)
light_relay_gpio = gpio.GPIO_STRUCT(LIGHT_RELAY_GPIO, True) 
gpio.setup_pin(light_relay_gpio)

#Start graceful shutdown
GPIO_PI.cleanup()
sys.exit()