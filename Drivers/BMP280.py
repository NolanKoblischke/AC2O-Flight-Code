# sudo apt-get install python-smbus
import smbus
import time
from bmp280 import BMP280
 
#DEVICE = 0x76 # Default device I2C address
 
bus = smbus.SMBus(1) # Rev 2 Pi uses 1 
bmp280 = BMP280(i2c_dev=bus)

def readBmp280():
    return (bmp280.get_temperature(), bmp280.get_pressure())


