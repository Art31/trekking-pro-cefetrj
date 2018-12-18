# --------------------------------------------------------------------------- #
# Title: Ultrasonic measure and interpretation script
# Author: Arthur Telles, Eduardo Brizida, Balthazar Paixao
# Date: 01/07/2018 (DD/MM/YYYY)
# Description: 
# --------------------------------------------------------------------------- #

import sys
import time
import signal
import RPi.GPIO as GPIO
from multiprocessing import Process
import numpy as np
from lib.MotorAtual import Motor as motor
#Usar apenas essa biblioteca para ultrassônicos

class Ultrassom():
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

        GPIO.setup(trigA,GPIO.OUT)
        GPIO.setup(echoA,GPIO.IN)

        GPIO.setup(trigB,GPIO.OUT)
        GPIO.setup(echoB,GPIO.IN)
        
        GPIO.setup(trigC,GPIO.OUT)
        GPIO.setup(echoC,GPIO.IN)
        
        GPIO.setup(trigD,GPIO.OUT)
        GPIO.setup(echoD,GPIO.IN)
        
        sampling_rate = 20.0
        speed_of_sound = 349.10
        max_distance = 4.0
        max_delta_t = max_distance / speed_of_sound

    def sigint_handler(signum, instant):
        clean()
        

        # Ativar a captura do sinal SIGINT (Ctrl-C)
    signal.signal(signal.SIGINT, sigint_handler)



# Variáveis para auxiliar no controle do loop principal
# sampling_rate: taxa de amostragem em Hz, isto é, em média,
#   quantas leituras do sonar serão feitas por segundo
# speed_of_sound: velocidade do som no ar a 30ºC em m/s
# max_distance: máxima distância permitida para medição
# max_delta_t: um valor máximo para a variável delta_t,
#   baseado na distância máxima max_distance


 
# Inicializa TRIG em nível lógico baixo
    GPIO.output(trigA,False)
    GPIO.output(trigB,False)
    GPIO.output(trigC,False)
    GPIO.output(trigD,False)

    def leitura(self):

        vA = []; vB = []; vC = []; vD = []
    
        for i in range(0,5):

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

            if end_tA - start_tA < max_delta_t:
                    delta_tA = end_tA - start_tA
                    distanceA = 100*(0.5 * delta_tA * speed_of_sound)
            else:
                    distanceA = -1


            if end_tB - start_tB < max_delta_t:
                    delta_tB = end_tB - start_tB
                    distanceB = 100*(0.5 * delta_tB * speed_of_sound)
            else:
                    distanceB = -1


            if end_tC - start_tC < max_delta_t:
                    delta_tC = end_tC - start_tC
                    distanceC = 100*(0.5 * delta_tC * speed_of_sound)
            else:
                    distanceC = -1


            if end_tD - start_tD < max_delta_t:
                    delta_tD = end_tD - start_tD
                    distanceD = 100*(0.5 * delta_tD * speed_of_sound)
            else:
                    distanceD = -1

            vA.append(distanceA)
            vB.append(distanceB)
            vC.append(distanceC)
            vD.append(distanceD)

        mA = np.median(vA)
        mB = np.median(vB)
        mC = np.median(vC)
        mD = np.median(vD)

        DiferentialBC = mB - mC


        #print(str(tpp - time()) + " seconds")

        #metricA e metricB tem que retornar valores muito grandes sempre,
        #quando eles retornarem algo menor que 300cm MAIS DE 3 VEZES,
        #isso e um obstaculo e precisamos escapar dele. Se
        #essa medida diminuir, estamos nos aproximando do obstaculo e precismos
        #desviar dele mais rapido ainda, usar a logica de blocos no
        #drive "logistica trekking". Quanto mais proximo mais rapido se desvia

        # trabalhar com casos de leitura confiavel em 2 ultras, e em 1 ultra
        #logicas diferentes pro da esquerda e direita e pros dois centrais
        
        # em 1 ultrassom, viramos mais rapido para que outro detecte, só podemos
        # nos alinhar direito quando 2 detectarem
		
        def navegacao(self):

            self.leituras()

            while (mA <= 180):
                # tem obstaculo na esquerda
                angulo1 = 15;angulo2 = 20;angulo3 = 25;angulo4 = 30;angulo5 = 35;angulo5 = 40
                self.controle.posicionar(angulo1,50)
                vel = motor.MudarVelocidade(40,80)

                if (mA <= 150):
                    self.controle.posicionar(angulo4,50)
                    vel = motor.MudarVelocidade(40,80)
                    #diminuir velocidade

                if (mB <= 180 and mC <= 180):
                    #objeto grande, desviar
                    #importar curvas no código e chamar nesse momento
                    self.controle.posicionar(angulo3,70) # confirmar angulo e forca
                    vel = motor.MudarVelocidade(40,80)
                    #diminuir velocidade

                if (mB <= 150 and mC <= 150):
                    self.controle.posicionar(angulo5,80)
                    vel = motor.MudarVelocidade(30,80)
                    #diminuir velocidade mais ainda

                elif (mB <= 180):
                    #objeto menor, virar mais lento
                    self.controle.posicionar(angulo2,60) # confirmar angulo e forca
                    vel = motor.MudarVelocidade(40,80)
                if (mB <= 150):
                    self.controle.posicionar(angulo3,50)
                    vel = motor.MudarVelocidade(30,80)
                    #diminuir velocidade

                if (mB > 180 and mC > 180):
                    #obstaculo nao e mais visto pela centro esquerda e centro direita
                    self.controle.posicionar(0,50)
                    vel = motor.MudarVelocidade(60, 80)

            while (mD <= 180):
                #repetir logica de rawA <= 180
                # tem obstaculo na direita
                angulo1 = -15;angulo2 = -20;angulo3 = -25;angulo4 = -30;angulo5 = -35
                self.controle.posicionar(angulo1,50)
                vel = motor.MudarVelocidade(40,80)
                if (mD <= 150):
                    self.controle.posicionar(angulo4,50)
                    vel = motor.MudarVelocidade(30,80)
                    #diminuir velocidade

                if (mB <= 180 and mC <= 180):
                    #objeto grande, desviar
                    #importar curvas no código e chamar nesse momento
                    self.controle.posicionar(angulo3,70) # confirmar angulo e forca
                    vel = motor.MudarVelocidade(40,80)
                    #diminuir velocidade

                if (mB <= 150 and mC <= 150):
                    self.controle.posicionar(angulo5,80)
                    vel = motor.MudarVelocidade(30,80)
                    #diminuir velocidade mais ainda

                elif (mB <= 180):
                #objeto menor, virar mais lento
                    self.controle.posicionar(angulo2,60) # confirmar angulo e forca
                    vel = motor.MudarVelocidade(40,80)

                if (mB <= 150):
                    self.controle.posicionar(angulo3,50)
                    vel = motor.MudarVelocidade(30,80)
                #diminuir velocidade

                if (mB > 180 and mC > 180):
                #obstaculo nao e mais visto pela centro esquerda e centro direita
                    self.controle.posicionar(0,50)
                    vel = motor.MudarVelocidade(60,80)

            return mA,mB,mC,mD

    #esse modo sera implementado na logica de controle, nao aqui
    def callback(self):
        print("Entramos em callback, regenerando navegacao")
        mA,mB,mC,mD = a.navegacao(5,0.1)
        time.sleep(1/20)
        return mA,mB,mC,mD

    def localizacao(self):
        self.leituras()    

            #Se chegamos nessa funcao, significa que imagens ja confirmou que e
            #um cone e estamos tao proximo que imagens deixa de ser confiavel.
            #Entao precisamos fazer ajustes finos aqui, chamando o motor e o servo.
            #Apos encostar nele, vamos ter que acionar a sirene e usar
            #a ponte H em marcha ré, mas precisamos definir como isso vai ser feito

            # trabalhar com casos de leitura confiavel em 2 ultras, e em 1 ultra
            #logicas diferentes pro da esquerda e direita e pros dois centrais

            # em 1 ultrassom, viramos mais rapido para que outro detecte, só podemos
            # nos alinhar direito quando 2 detectarem

            dist_min = min([mA,mB,mC,mD])

            while (dist_min > 5):
                minimo = min([mA, mB, mC, mD])
# -----------------------------
                # USAR Y = 0.434X - 3.478
                # posicao = minimo * 0.434 - 3.478
                # servo.posicionar(posicao,50) # arbitrar a forca
# -----------------------------
                angulo1 = 5;angulo2 = 10;angulo3 = 15;angulo4 = 20;angulo5 = 30
                if minimo < 100:
                    vel = motor.MudarVelocidade(30,80)
                    #diminuir velocidade 20%

                    if minimo == mA:
                        while ((minimo != mB) or (minimo != mC)):
                            #Cone mais próximo da esquerda
                            servo.posicionar(angulo4, 50)
                            vel = motor.MudarVelocidade(15,80)

                            #motor a 15%
                            #if minimo == mD:
                                #break
                        minimo = min([mA,mB,mC,mD])
                    #elif minimo == mB:
                        
                        #Cone mais  próximo do centro esquerda
                     #   servo.posicionar(angulo2, 50)
                        #motor a 20%
                    elif minimo == mC or minimo == mB:
                        ServoAng = 0.22 * DiferentialBC
                        if (ServoAng >= 45):
                            ServoAng = 45
                        if (ServoAng <= -45):
                            ServoAng = -45
                        #Cone mais proximo do centro direita
                        #angulo1 = -15;angulo2 = -20;angulo3 = -25;angulo4 = -30;angulo5 = -35
                        servo.posicionar(ServoAng, 50)
                        vel = motor.MudarVelocidade(20,80)

                        #motor a 20%
                        #if minimo == mA:
                         #       break
                        minimo = min([mA,mB,mC,mD])
                elif minimo < 50:
                    #diminuir mais velocidade 10%
                    #repete a logica acima virando mais com a mesma velocidade de motor
                    if minimo == rawA:
                        #Cone mais próximo da esquerda
                        self.posicionar(angulo3, 50)
                        vel = motor.MudarVelocidade(20,80)
                        #motor a 5%

                    elif minimo == rawB:
                        #Cone mais  próximo do centro esquerda
                        self.posicionar(angulo1, 50)
                        vel = motor.MudarVelocidade(20,80)
                        #motor a 10%
                    
                    elif minimo == rawC:
                        #Cone mais proximo do centro direita
                        self.posicionar(angulo1, 50)
                        vel = motor.MudarVelocidade(20,80)
                        #motor a 10%
                    
                    elif minimo == rawD:
                        #Cone mais propximo da direita
                        self.posicionar(angulo3, 50)
                        vel = motor.MudarVelocidade(15,80)

                        #motor a 5%
                                            
                elif minimo < 20:
                    motor.StopMotor()
                    sirene()

                    #diminuir mais velocidade 5%
                    #repete a logica acima virando mais, porem em uma velocidade de motor mais lenta
                   # if minimo == rawA:
                        #Cone mais próximo da esquerda
                    #    self.posicionar(angulo1, 30)
                        #motor a 10%
                   # elif minimo == rawB:
                        #Cone mais  próximo do centro esquerda
                    #    self.posicionar(3, 20)
                        #motor a 15%
                    #elif minimo == rawC:
                        #Cone mais proximo do centro direita
                        #angulo1 = -15;angulo2 = -20;angulo3 = -25;angulo4 = -30;angulo5 = -35
                     #   self.posicionar(3, 20)
                        #motor a 15%
                   # elif minimo == rawD:
                        #Cone mais propximo da direita
                        #angulo1 = -15;angulo2 = -20;angulo3 = -25;angulo4 = -30;angulo5 = -35
                    #    self.posicionar(angulo1, 30)
                        #motor a 10%
                #elif minimo <= 8:
                    #sirene
                    #motor da ré e direcionar o servo para o proximo cone
                dist_min = min([mA,mB,mC,mD])

            while (dist_min < 40):
                print("Entramos no modo de saida do cone")
                
                if cone_um == True:
                    while ((time.time() - tempo) < 3):                        
                        self.posicionar(-angulo5,70)
                        motor.MarchaRe()
                        motor.MudarVelocidade(40, 50)

                    motor.StopMotor()

                    ###Voltar com imagens

                   # while ((time.time() - tempo) < 3):
                    #    self.posicionar(angulo5,70)
                     #   motor.VelocidadePositiva()
                      #  motor.MudarVelocidade(30, 80)
                    #while ((time.time() - tempo) < 2):
                     #   self.posicionar(0,20)
                    
                
                elif cone_dois == True:
                    while ((time.time() - tempo) < 5):
                        self.posicionar(0,70)
                        motor.MarchaRe()
                        motor.MudarVelocidade(40, 90)

                        motor.StopMotor()

                    while ((time.time() - tempo) < 2):

                        self.posicionar(angulo5,70)
                        motor.VelocidadePositiva()
                        motor.MudarVelocidade(60, 80)
                        self.posicionar()

                        ##Voltar com imagens
                elif cone_tres == True:
                    #Somente checar com imagens

                    
                #dar marcha ré a 15% e pegar angulo de saida do proximo cone
                
##        except:
##            a.callback() #deu xabu, chamando novamente navegacao
##            dist_min = min([metricB,metricC])
                            
        return mA,mB,mC,mD

### Exemplo de uso
#a = Ultrassom(19,22,13,27)
#
#metricA,metricB = a.navegacao(1,0.005)
#
###a

##ultraA_read()
##def UltraDiferencial():
##    while (True):
##        
##        Diferencial = Ue - Ud
##
##        print(Diferencial)    
##readings = []
##readings.append(Process(target=ultraA_read))
##for reading in readings:
##    reading.start()
##    print(reading)

