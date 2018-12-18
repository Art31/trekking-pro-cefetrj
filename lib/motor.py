# --------------------------------------------------------------------------- #
# Title: Motor control script
# Author: Arthur Telles
# Date: 01/07/2018 (DD/MM/YYYY)
# Description: This function was made upon the datasheet of the motor $%¨#$&%$&%$
# that contains 3 possible states: forward, backward and stop. The transition
# between duty cycles is made in a smooth manner with a loop. The change speed 
# function is able to do that for both raising and lowering the speed.
# --------------------------------------------------------------------------- #

import RPi.GPIO as GPIO
import time
import numpy as np


class Motor():
    
    def __init__(self,PinagemA,PinagemB,PinagemC):
        self.pinA = PinagemA #16
        self.pinB = PinagemB #20
        self.pinC = PinagemC #21

        GPIO.setmode(GPIO.BCM) # using raspberry pi 3 BCM setmode
        GPIO.setup(self.pinA,GPIO.OUT) #Setup to move forward (+)
        GPIO.setup(self.pinB,GPIO.OUT)  #Setup to move backward (-)
        # A (+) B (-) moves forward, A (-) B (+) moves backwards, A = B = 0 stops
        GPIO.setup(self.pinC,GPIO.OUT)  #PWM Setup
        
        GPIO.output(self.pinA,GPIO.LOW)
        GPIO.output(self.pinB,GPIO.LOW)
        self.Motor = GPIO.PWM(self.pinC, 1000) # 1kHz
        
        self.actual_dtc = 0
        
        self.Motor.start(self.actual_dtc)
        
    def StopMotor(self):
        # this puts the motor in high impedance mode
       # as the datasheet states, the motor taks 1.8ms to change states
        GPIO.output(self.pinA,GPIO.LOW)
        GPIO.output(self.pinB,GPIO.LOW)

    # moves forward
    def move_forward(self):
        # as the datasheet states, the motor taks 1.8ms to change states
        GPIO.output(self.pinA,GPIO.HIGH)
        GPIO.output(self.pinB,GPIO.LOW)
        
    
    def move_backward(self):
        # as the datasheet states, the motor taks 1.8ms to change states
        GPIO.output(self.pinA,GPIO.LOW)
        GPIO.output(self.pinB,GPIO.HIGH)
        
    # forca is a variable that determines how fast the duty cycle changes  
    def change_speed(self, desired_dtc, forca):
        
        self.desired_dtc = desired_dtc
        forca = int(forca)
        assert forca <= 100,"Cannot be bigger than 100"
        assert forca >= 1,"Cannot be smaller than 1"
            
        if (desired_dtc > self.actual_dtc):
        
            velocity_gain = desired_dtc - self.actual_dtc
            proportional_delay = velocity_gain/100
            nb_loops = len(np.arange(self.actual_dtc,desired_dtc,0.1))
            
            for dutycycle in np.arange(self.actual_dtc,desired_dtc,0.1):
                #tempo maximo de 
                self.Motor.ChangeDutyCycle(dutycycle)
                # forca max 100 - 7s * proportional_delay, forca min 1 - 40s * proportional_delay
                time.sleep(proportional_delay*((7/nb_loops) + ((100-forca)/3)/nb_loops))

            self.actual_dtc = desired_dtc
            print("Duty Cycle: " + str(self.actual_dtc))
        
        elif (desired_dtc < self.actual_dtc):
            
            velocity_loss = self.actual_dtc - desired_dtc
            proportional_delay = velocity_loss/100
            nb_loops = len(np.arange(desired_dtc,self.actual_dtc,0.1))
            
            for dutycycle in list(reversed(np.arange(desired_dtc,self.actual_dtc,0.1))):
                #tempo maximo de 
                self.Motor.ChangeDutyCycle(dutycycle)
                # forca max 100 = 7s * proportional_delay, forca min 1 = 40s * proportional_delay
                time.sleep(proportional_delay*((7/nb_loops) + ((100-forca)/3)/nb_loops))

            self.actual_dtc = desired_dtc
            print("Duty Cycle: " + str(self.actual_dtc))
        
        return self.actual_dtc
#tempo = time.time()    
### Exemplo de uso
#a = Motor(23,24,18)
#
#a.move_forward()
#while ((time.time() - tempo < 2)):
#    vel_atual = a.change_speed(40,1) # informar ultima velocidade a funcao superior

#a.StopMotor()
#time.sleep(10)
#a.move_backward()

#while ((time.time() - tempo < 15)):
#    vel_atual = a.change_speed(10,10)
#
#GPIO.cleanup() # lembrar de usar apos terminar codigo
###
