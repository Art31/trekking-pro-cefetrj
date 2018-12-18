from lib.motor import Motor
from lib.servomotor import Curves
from lib.simple_gps import gps
from lib.ultrasonic_hcsr04 import Ultrassom
from cone_detector.Object_detection_Picamera import object_detector
import time
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
gyroflex = False

def sirene():
    if gyroflex == False:
        GPIO.output(5,GPIO.HIGH)
        gyroflex == True
        time.sleep(2.5)
    if gyroflex == True:
        GPIO.output(5,GPIO.LOW)
        gyroflex == False

def pegar_coordenadas():
    da, dpc = ground.logica_localizacao()

    diff_ang.append(da)
    dist_prox_cone.append(dpc)

    return da,dpc
	
def pegar_coordenadas_com_delay():
    for i in range(0,5):
        da, dpc = ground.logica_localizacao()
        diff_ang.append(da)
        dist_prox_cone.append(dpc)
        time.sleep(0.01) # wait for the coordinates to update
    return da,dpc    

diff_ang = []; dist_prox_cone = []

ground = gps()
motor = Motor(23,24,18)
motor.move_forward()
servo = Curves(12)
servo.posicionar(0,100)
vel1 = motor.change_speed(15,80)
da,dpc = pegar_coordenadas_com_delay()

while (dpc[-1] > 3):
    vel1 = motor.change_speed(45,30)
    da,dpc = pegar_coordenadas()
    angulo = servo.posicionar(da[-1]*.25,50)
    #print("da = " + str(da))
    #if (da[-1] < -25):
    #    angulo1 = servo.posicionar(da[-1],50)
    #elif (((da[-1] > -40) & (da[-1] < -25))):
    #    angulo1 = servo.posicionar(da[-1],50)
    #    vel = motor.change_speed(35,80)
    #    time.sleep(0.05)
    #elif (da[-1] > -40):
    #    angulo1 = servo.posicionar(-35,50)
    #    vel = motor.change_speed(25,80)
    #    time.sleep(0.05) 
    #if (da[-1] < 25):
    #    angulo1 = servo.posicionar(da[-1],50)
    #elif (((da[-1] < 40) & (da[-1] > 25))):
    #    angulo1 = servo.posicionar(da[-1],50)
    #    vel = motor.change_speed(35,80)
    #    time.sleep(0.05)
    #elif (da[-1] > 40):
    #    angulo1 = servo.posicionar(35,50)
    #    vel = motor.change_speed(25,80)
    #    time.sleep(0.05)
    # 
while (dpc[-1] < 3):
    vel1 = motor.change_speed(25,30)
    da,dpc = pegar_coordenadas()
    angulo = servo.posicionar(da[-1]*.25,50)
    #if (da[-1] < -25):
    #    angulo1 = servo.posicionar(da[-1],50)
    #elif (((da[-1]) > -40) & (da[-1] < -25)):
    #    angulo1 = servo.posicionar(da[-1],50)
    #    vel = motor.change_speed(20,80)
    #    time.sleep(0.05)
    #elif (da[-1] > 40):
    #    angulo1 = servo.posicionar(-35,50)
    #    vel = motor.change_speed(20,80)
    #    time.sleep(0.05) 
    #if (da[-1] < 25):
    #    angulo1 = servo.posicionar(da[-1],50)
    #elif (((da[-1]) < 40) & (da[-1] > 25)):
    #    angulo1 = servo.posicionar(da[-1],50)
    #    vel = motor.change_speed(20,80)
    #    time.sleep(0.05)
    #elif (da[-1] > 40):
    #    angulo1 = servo.posicionar(35,50)
    #    vel = motor.change_speed(20,80)
    #    time.sleep(0.05)
    if (dpc[-1] < 0.5):
        vel = motor.change_speed(0,80)         
        motor.move_backward()
        time.sleep(0.002)
        sirene()


leituraA,leituraB,leituraC,leituraD = self.Ultrassom.leitura()
def coneum():
    if leituraA < 150 or leituraB < 150 or leituraC < 150 or leituraD < 150:
        if cone == True:
            self.Ultrassom.localizacao()
            cone_um = True
            cone_dois = False
            cone_tres = False
        
        elif cone == False:
            self.Ultrassom.navegacao()
    def conedois():
    if leituraA < 150 or leituraB < 150 or leituraC < 150 or leituraD < 150:
        if cone == True:
            self.Ultrassom.localizacao()
            cone_um = True
            cone_dois = False
            cone_tres = False

# MEXER COM O RETORNO DE ANGULO
#motor = Motor(23,24,18)
#motor.move_forward()
#servo = Curves(12)
#time.sleep(3)
#tempo = time.time()

#while ((time.time() - tempo) < 3):
#	vel1 = motor.change_speed(40,1)
#	angulo1 = servo.posicionar(15,10)
#vel2 = motor.change_speed(0,1)
#print(vel2)
#time.sleep(5)

#tempo = time.time()

#while ((time.time() - tempo) < 2):
#	vel1 = motor.change_speed(45,1)
#	angulo2 = servo.posicionar(5,100)
#vel2 = motor.change_speed(0,1)
#time.sleep(5)

#tempo = time.time()

#while ((time.time() - tempo) < 2):
#	vel1 = motor.change_speed(50,1)
#	angulo3 = servo.posicionar(0,100)
#vel2 = motor.change_speed(0,1)


angulo3 = servo.posicionar(0,100)
