import RPi.GPIO as GPIO
import time
import numpy as np
import sys
import time
import signal
import RPi.GPIO as GPIO
from multiprocessing import Process
import numpy as np
from lib.MotorAtual import Motor as motor
from lib.ServoAtual import Curvas
#Usar apenas essa biblioteca para ultrassônicos

class UltrassomEServo():
    def __init__(self):
		#esquerda
        self.trigA = 13 
        self.echoA = 27 
		#centro esquerda
        self.trigB = 19 
        self.echoB = 22 
		#centro direita
        self.trigC = 6 
        self.echoC = 17
		#direita
        self.trigD = 4 
        self.echoD = 20


        self.tempo = time.time()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigA,GPIO.OUT)
        GPIO.setup(self.echoA,GPIO.IN)

        GPIO.setup(self.trigB,GPIO.OUT)
        GPIO.setup(self.echoB,GPIO.IN)
        
        GPIO.setup(self.trigC,GPIO.OUT)
        GPIO.setup(self.echoC,GPIO.IN)
        
        GPIO.setup(self.trigD,GPIO.OUT)
        GPIO.setup(self.echoD,GPIO.IN)
        
        sampling_rate = 20.0
        self.speed_of_sound = 340.29
        max_distance = 4.0
        self.max_delta_t = 1.5 * (max_distance / self.speed_of_sound)

        self.servo = Curvas(12)

    def sigint_handler(signum, instant):
        clean()
        

        # Ativar a captura do sinal SIGINT (Ctrl-C)
        signal.signal(signal.SIGINT, sigint_handler)



# Variáveis para auxiliar no controle do loop principal
# sampling_rate: taxa de amostragem em Hz, isto é, em média,
#   quantas leituras do sonar serão feitas por segundo
# self.speed_of_sound: velocidade do som no ar a 30ºC em m/s
# max_distance: máxima distância permitida para medição
# max_delta_t: um valor máximo para a variável delta_t,
#   baseado na distância máxima max_distance


 
# Inicializa TRIG em nível lógico baixo
        GPIO.output(self.trigA,False)
        GPIO.output(self.trigB,False)
        GPIO.output(self.trigC,False)
        GPIO.output(self.trigD,False)

    def leitura(self):

        vA = []; vB = []; vC = []; vD = []
    
        for i in range(0,10):

            GPIO.output(self.trigA,True)
            time.sleep(0.00001)
            GPIO.output(self.trigA,False)
            while GPIO.input(self.echoA) == 0:
                start_tA = time.time()
            while (GPIO.input(self.echoA) == 1  and time.time() - start_tA < self.max_delta_t):
                end_tA = time.time()


            GPIO.output(self.trigB,True)
            time.sleep(0.00001)
            GPIO.output(self.trigB,False)
            while GPIO.input(self.echoB) == 0:
                start_tB = time.time()
            while (GPIO.input(self.echoB) == 1  and time.time() - start_tB < self.max_delta_t):
                end_tB = time.time()


            GPIO.output(self.trigC,True)
            time.sleep(0.00001)
            GPIO.output(self.trigC,False)
            while GPIO.input(self.echoC) == 0:
                start_tC = time.time()
            while (GPIO.input(self.echoC) == 1  and time.time() - start_tC < self.max_delta_t):
                end_tC = time.time()

            GPIO.output(self.trigD,True)
            time.sleep(0.00001)
            GPIO.output(self.trigD,False)
            while GPIO.input(self.echoD) == 0:
                start_tD = time.time()
            while (GPIO.input(self.echoD) == 1  and time.time() - start_tD < self.max_delta_t):
                end_tD = time.time()


            # Se a diferença entre end_t e start_t estiver dentro dos limites impostos,
            # atualizamos a variável delta_t e calculamos a distância até um obstáculo.
            # Caso o valor de delta_t não esteja nos limites determinados definimos a
            # distância como -1, sinalizando uma medida mal-sucedida.

            if end_tA - start_tA < self.max_delta_t:
                    delta_tA = end_tA - start_tA
                    distanceA = 100*(0.5 * delta_tA * self.speed_of_sound)
            else:
                    distanceA = -1


            if end_tB - start_tB < self.max_delta_t:
                    delta_tB = end_tB - start_tB
                    distanceB = 100*(0.5 * delta_tB * self.speed_of_sound)
            else:
                    distanceB = -1


            if end_tC - start_tC < self.max_delta_t:
                    delta_tC = end_tC - start_tC
                    distanceC = 100*(0.5 * delta_tC * self.speed_of_sound)
            else:
                    distanceC = -1


            if end_tD - start_tD < self.max_delta_t:
                    delta_tD = end_tD - start_tD
                    distanceD = 100*(0.5 * delta_tD * self.speed_of_sound)
            else:
                    distanceD = -1

            if distanceA != -1:
                vA.append(distanceA)
            if distanceB != -1:
                vB.append(distanceB)
            if distanceC != -1:
                vC.append(distanceC)
            if distanceD != -1:
                vD.append(distanceD)

        self.mA = np.median(vA)
        self.mB = np.median(vB)
        self.mC = np.median(vC)
        self.mD = np.median(vD)

        self.DiferentialBC = self.mB - self.mC

        
        print("mA" + str(self.mA) + str(vA))
        print('mB:' + str(self.mB) + str(vB))
        print('mC:' + str(self.mC) + str(vC))
        print('mD:' + str(self.mD) + str(vD))
        

    def localizacao(self): 
        self.leitura()

        # a angulacao precisa ser amarrada com esse maximo
        if (self.mA > 300):
            self.mA = 300
        elif (self.mB > 300):
            self.mB = 300
        elif (self.mC > 300):
            self.mC = 300
        elif (self.mD > 300):
            self.mD = 300

        dist_min = min([self.mA,self.mB,self.mC,self.mD])
        
        while (dist_min > 1):
            time.sleep(0.3)
            self.leitura()

            if (self.mA > 300):
                self.mA = 300
            elif (self.mB > 300):
                self.mB = 300
            elif (self.mC > 300):
                self.mC = 300
            elif (self.mD > 300):
                self.mD = 300
            
            dist_min = min([self.mA,self.mB,self.mC,self.mD])
# -----------------------------
            # USAR Y = 0.434X - 3.478
            # posicao = dist_min * 0.434 - 3.478
            # #servo.posicionar(posicao,50) # arbitrar a self.Power
# -----------------------------
            angulo1 = 5;angulo2 = 10;angulo3 = 15;angulo4 = 20;angulo5 = 30

            if dist_min == self.mA:
                print("to no MA")
                self.Angulacao = ((35/285)*(self.mC - self.mA)) # valor max 285 min ~0 - ang max 35
##                self.Power = ((-1.5*self.Angulacao) + 100)
                self.estado_servo = self.servo.posicionar(self.Angulacao,50)

                
            elif dist_min == self.mC or dist_min == self.mB:
                diff = self.mC - self.mB
                if diff > 50:
                    diff = 50
                elif diff < -50:
                    diff = -50
                print("to no MB,MC")
                self.Angulacao = ((35/50)*(diff)) # valor max 50 min -50 - ang max 35
##                self.Power = ((-1.5*self.Angulacao)+100)
                self.estado_servo = self.servo.posicionar(self.Angulacao,50)

                
            if dist_min == self.mD:
                print("TO NO MD")
                self.Angulacao = (-(35/285)*(self.mB - self.mD)) # valor max 285 min ~0 - ang max 35
##                self.Power = ((-1.5*self.Angulacao)+100)
                self.estado_servo = self.servo.posicionar(self.Angulacao,50)

            dist_min = min([self.mA,self.mB,self.mC,self.mD])

            print('Angulo:' + str(self.Angulacao))
##            print("Power:" +  str(self.Power))      

        
            
a = UltrassomEServo()






