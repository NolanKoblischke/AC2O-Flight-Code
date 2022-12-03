import time

#function to check temp
#Validate boundary
low_temp_threshold = 25
high_temp_threshold = 30

def on_off(temp, heater_pin):
    #if below turn on
    if(temp <= low_temp_threshold):
        #TURN HEATER ON
        heater_pin.set_pin_state(False)     #NOTE: THIS IS INVERTED BECAUSE IT'S A RELAY
        print("turning heater on")

    #if above turn on (slower/flicking it)
    elif(temp >= high_temp_threshold):
        heater_pin.set_pin_state(True)      #NOTE: THIS IS INVERTED BECAUSE IT'S A RELAY
        #TODO: Implement a flicking thing
        print("turning heater off")

