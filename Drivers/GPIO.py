import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BCM)

class GPIO_STRUCT:
    def __init__(self, pin_number, pin_state):
          self.pin_state = pin_state
          self.pin_number = pin_number
       
    #Getters
    def get_pin_number(self):
        return self.pin_number

    def get_pin_state(self):
        return self.pin_state
       
    #Setters
    def set_pin_state(self, state):
        if state != self.get_pin_state():
            if state:
                GPIO.output(self.get_pin_number(), GPIO.HIGH) #Turn gpio on
            else:
                GPIO.output(self.get_pin_number(), GPIO.LOW) #Turn gpio off
            self.pin_state = state

def setup_pin(gpio_pin):
    if gpio_pin.get_pin_state():
        GPIO.setup(gpio_pin.get_pin_number(), GPIO.OUT, initial = GPIO.HIGH)
    else:
        GPIO.setup(gpio_pin.get_pin_number(), GPIO.OUT, initial = GPIO.LOW)



