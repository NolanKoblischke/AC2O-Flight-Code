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

def main_init():
    camera0 = None
    tempSensor0 = None
    try:
        camera0 = camera.newCamera()
    except Exception as e:
        print("Camera failed to initialize")
        print(e)
    try:
        tempSensor0 = tempsensors.newTempSensor(sensorID=0)
    except Exception as e:
        print("Temp Sensor failed to initialize")
        print(e)
        tempSensor0 = None
    return camera0, tempSensor0
  
    

def graceful_shutdown():
    GPIO_PI.cleanup()

    sys.exit()


if __name__ == '__main__':
    # FOLLOWING CODE RUNS ONLY ONCE #***********************************************************************************************
    camera0, tempSensor0 = main_init()
    in_sleep_state = False
    # in_emergency_state = False
    time_of_last_photo = time.time()
    time_of_last_pump = time.time()
    time_of_last_proper_elink_connection = time.time()
    timestamp_for_csv_file = time.strftime('%b-%d-%Y_%H_%M', time.localtime())
    #Create dataframe to store sensor data
    currentDatetime = datetime.datetime.now()
    temp_tower, pressure_tower, temp_plate, temp_dome, pressure_dome = None, None, None, None, None
    array = ["currentDatetime", "temp_tower", "pressure_tower", "temp_plate", "temp_dome", "pressure_dome"]
    #******************************************************************************************************************************
    light_relay_gpio.set_pin_state(False) #Turn off heater


    while True:
        print(datetime.datetime.now())
        
        try:
            time.sleep(0.25)
            #Test if elink is connected
            if elink.elinkStatus():
                time_of_last_proper_elink_connection = time.time()
            else:
                if (time.time() - time_of_last_proper_elink_connection) > TIME_LIMIT_FOR_ELINK_DISCONNECTS:
                    heater_relay_gpio.set_pin_state(True) #Turn off heater
                    os.system('sudo reboot')
            try:
                temp_tower, pressure_tower = BMP280.readBmp280()
                pressure_tower = pressure_tower*100
            except Exception as exc:
                print("_____________ BMP280 (Tower) faulty _______________")
                print("Message: ", exc)
                print("/_________________________________________________/")
                
            #TODO: Pressure check
            try:
                temp_dome, pressure_dome = BMP180.readBmp180()
            except Exception as exc:
                print("_____________ BMP180 (Dome) faulty _______________")
                print("Message: ", exc)
                print("/_________________________________________________/")
                
            try:
                temp_plate = tempSensor0.getReading()
            except Exception as exc:
                print("_____________ Temp Plate Sensor faulty _____________________")
                print("Message: ", exc)
                print("/_________________________________________________/")
                
            tempControl.on_off(temp_tower, heater_relay_gpio)
            # if temp_tower is not None:
                # print("Temp Tower: {:.2f}".format(float(temp_tower)))
            try:
                print("SENSOR STATUS ----------------------------------")
                print("Temp Tower:    {:.2f}".format(float(temp_tower)))
                print("Temp Dome:     {:.2f}".format(float(temp_dome)))
                print("Temp Plate:    {:.2f}".format(float(temp_plate)))
                print("Pressure Dome: {:.2f}".format(pressure_dome))
                print("Pressure Tower:{:.2f}".format(pressure_tower))
                
                print("\nGPIO STATUS ----------------------------------")
                print("Light Relay GPIO:   ", light_relay_gpio.get_pin_state())
                print("Pump Relay GPIO:    ", pump_relay_gpio.get_pin_state())
                print("Heater Relay GPIO:  ", heater_relay_gpio.get_pin_state())
                
                

            except Exception as exc:
                print(exc)
            
            try:
                array2 = [datetime.datetime.now(), temp_tower, pressure_tower, temp_plate, temp_dome, pressure_dome]
                array = np.vstack((array, array2))
                #save to csv
                np.savetxt("FlightLogs/results{}.csv".format(timestamp_for_csv_file), array, delimiter=",", fmt='%s')
            except Exception as exc:
                print("Failed to save data to csv.")
                print(exc)
                array2 = [datetime.datetime.now(),-1, -1, -1, -1, -1]
                array = np.vstack((array, array2))
                #save to csv
                np.savetxt("FlightLogs/results{}.csv".format(timestamp_for_csv_file), array, delimiter=",", fmt='%s')
                
            if (time.time() - time_of_last_photo) > SECONDS_BETWEEN_PHOTOS/2:
                try:
                    camera0.take_photo()
                    print("Photo taken")
                    time_of_last_photo = time.time()
                except Exception as exc:
                    print("_____________ Camera failed to take photo _______________")
                    print("Message: ", exc)
                    print("/_________________________________________________/")
                
            if (time.time() - time_of_last_pump) > SECONDS_BETWEEN_PUMPS:
                if (time.time() - time_of_last_pump) > SECONDS_BETWEEN_PUMPS + LENGTH_OF_PUMPS_IN_SECONDS:
                    # Turn off pump after LENGTH_OF_PUMPS_IN_SECONDS
                    pump_relay_gpio.set_pin_state(True)
                    time_of_last_pump = time.time()
                    print("Pump Off")
                else:
                    # Turn on pump
                    pump_relay_gpio.set_pin_state(False)
                    print("Pump On")
                    

                

        except KeyboardInterrupt:
            user_input = raw_input("Interupt Menu: ")
            print('Interrupted with user response', user_input)
            #TODO: manually control GPIOs
            #TODO: Change picture rate (?)
            
            if user_input == "SHUTDOWN":
                print("shutdown confirmed")
                graceful_shutdown()
            else:
                continue