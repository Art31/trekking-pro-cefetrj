# --------------------------------------------------------------------------- #
# Title: Servo control script
# Author: Arthur Telles
# Date: 01/07/2018 (DD/MM/YYYY)
# Description: This function was made upon the datasheet of the servo 
# JX PDI-6221MG, its a precision servo, and can be modified for any other one. 
# It uses 330 as the PWM frequency and considers half the amplitude as the 0 
# degree starting position, that is 32.5 degrees. So it may move between 17.5 
# and 50 in duty cycle, that interval represents a move from -45 to 45 degrees.
# --------------------------------------------------------------------------- #

import RPi.GPIO as GPIO
import time
import numpy as np

class Curves():
    def __init__(self, pin):
        self.pino = pin
        self.initial_angle = 32.5
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pino,GPIO.OUT)
        self.p = GPIO.PWM(self.pino, 330) # 330Hz
        self.p.start(32.5) # 32.5 = 0
        self.current_angle = 0
        self.current_dtc = 32.5
##        self.speed = time.sleep(-0.000175*self.Force+0.0205)
##        self.Force =int(input(x))

    # forca is a variable that determines how fast the duty cycle changes  
    def posicionar(self, desired_angle, forca):
        
        forca = int(forca)
        
        assert forca <= 100,"Cannot be bigger than 100"
        assert forca >= 1,"Cannot be smaller than 1"
        
        desired_dtc = (17.5/45) * desired_angle + 32.5 # desired_angle de -45() a 45

        if (self.current_dtc < desired_dtc):
            for dutycycle in np.arange(self.current_dtc,desired_dtc,0.01):
                #frange(self.current_angle,desired_angle,0.01):
                self.p.ChangeDutyCycle(dutycycle)
                # aumentei para 2/375 pq tava rapido demais
                time.sleep((1/375)/forca) # forca max 100 min 1
        elif (self.current_dtc > desired_dtc):
            for dutycycle in list(reversed(np.arange(desired_dtc,self.current_dtc,0.01))):
                #frange(self.current_angle,desired_angle,0.01):
                self.p.ChangeDutyCycle(dutycycle)
                # aumentei para 2/375 pq tava rapido demais
                time.sleep((1/375)/forca) # forca max 100 min 1
                
        self.current_angle = desired_angle
        self.current_dtc = desired_dtc

        #print("Angulo " + str(desired_angle))
        #print("Duty " + str(desired_dtc))
        return self.current_angle
	
### Exemplo de uso
#a = Curves(12)
#
#time.sleep(3)
#current_angle = a.posicionar(-45,50) # informar ultimo angulo a funcao superior

#time.sleep(3)

#a.posicionar(45,50)
#
#GPIO.cleanup() # lembrar de usar apos terminar codigo
###






##	for dutyc in range (45, -45,0.1):
##		pwm.ChangeDutyCycle(dutyc)
##		time.sleep(self.speed)



