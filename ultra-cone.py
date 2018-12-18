
from gpiozero import DistanceSensor
from lib.ServoAtual import Curvas
from time import sleep

servocurvas = Curvas(pino) #Indicar o pino

Ue = DistanceSensor(echo= , trigger= )
Uc = DistanceSensor(echo= , trigger= )
Ud = DistanceSensor(echo= , trigger= )
#Leitura dos pinos dos sensores (Ue, Uc, Ud)
leituras = [Ue.distance, Uc.distance, Ud.distance] # supondo leitura maxima de 5m

while (True):
    if min(leituras) <= 0.1:
        break  #Indicar que o cone foi encontrado

    elif leituras[1] == min(leituras): # mais proximo do centro
        print ("Frente")
        posicionar(0, 99)
            
        if leituras[1] < 5 and leituras[1] >= 3:
            #velocmotor(60)
        elif leituras[1] < 3 and leituras[1] >= 2:
            #velocmotor(50)
        elif leituras[1] < 2 and leituras[1] >= 1:
            #velocmotor(40)
        elif leituras[1] < 1 and leitura1[1] > 0.1:
            #velocmotor(30)
        else:
             # Definir algum movimento do robo que indique erro


    elif leituras[0] == min(leituras): # mais proximo da esquerda
        print ("Esquerda")  # 'forca' determina a velocidade de rotacao
        if leituras[0] < 5 and leituras[0] >= 3:
            forca = 40
            posicionar(-20,forca)
        elif leituras[0] < 3 and leituras[0] >= 2:
            forca = 60
            posicionar(-30,forca)
        elif leituras[0] < 2 and leituras[0] >= 1:
            forca = 80
            posicionar(-40,forca)
        elif leituras[0] < 1 and leituras[0] > 0.1:
            forca = 99
            posicionar(-45,forca)
        else:
            # Definir algum movimento do robo que indique erro

    elif leituras[2] == min(leituras): # mais proximo da direita
        print("Direita") # 'forca' determina a velocidade de rotacao
        if leituras[2] < 5 and leituras[2] >= 3:
            forca = 40
            posicionar(20,forca)
        elif leituras[2] < 3 and leituras[2] >= 2:
            forca = 60
            posicionar(30,forca)
        elif leituras[2] < 2 and leituras[2] >= 1:
            forca = 80
            posicionar(40,forca)
        elif leituras[2] < 1 and leituras[2] > 0.1:
            forca = 99
            posicionar(45,forca)
        else:
             # Definir algum movimento do robo que indique erro

    
    else:
        #O que fazer se não houver detecção

