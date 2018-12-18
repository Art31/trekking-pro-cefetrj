from lib.MotorAtual import Motor
from lib.ServoAtual import Curvas
from lib.GpsAtual import gps
import time
import numpy as np

# MEXER COM O RETORNO DE ANGULO
a = gps()
motor = Motor(23,24,18)
motor.VelocidadePositiva()
servo = Curvas(12)
time.sleep(3)
tempo = time.time()

while ((time.time() - tempo) < 40):
        a.logica_localizacao()
        vel1 = motor.MudarVelocidade(60,50)
        angulo1 = servo.posicionar(-10,10)
vel2 = motor.MudarVelocidade(0,1)
print(vel2)
time.sleep(5)

tempo = time.time()

#while ((time.time() - tempo) < 2):
#	vel1 = motor.MudarVelocidade(45,1)
#	angulo2 = servo.posicionar(5,100)
#vel2 = motor.MudarVelocidade(0,1)
#time.sleep(5)

#tempo = time.time()

#while ((time.time() - tempo) < 2):
#	vel1 = motor.MudarVelocidade(50,1)
#	angulo3 = servo.posicionar(0,100)
#vel2 = motor.MudarVelocidade(0,1)

motor.MarchaRe()
#time.sleep(5)

tempo = time.time()
while ((time.time() - tempo) < 2):
	vel1 = motor.MudarVelocidade(30,1)
	angulo3 = servo.posicionar(-15,100)
vel2 = motor.MudarVelocidade(0,1)
time.sleep(5)
angulo4 = servo.posicionar(0,1)

