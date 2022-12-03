import BMP180
import time
import datetime
while True:
    print(datetime.datetime.now())
    temp, pressure, altitude = BMP180.readBmp180()
    print("Temperature is ",temp)  # degC
    print("Pressure is    ",pressure) # Pressure in Pa
    #print("Altitude is ",altitude) # Altitude in meters

    print("\n")
    time.sleep(0.001)
