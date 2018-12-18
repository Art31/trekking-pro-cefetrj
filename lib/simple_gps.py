# --------------------------------------------------------------------------- #
# Title: GPS measure and control script
# Author: Arthur Telles
# Date: 01/07/2018 (DD/MM/YYYY)
# Description: 
# --------------------------------------------------------------------------- #

import gpsd
import time
import numpy as np

# eixo x e positivo para a esquerda
# eixo y e positivo para baixo
# entender com o balta como ele fez o calculo

class gps():
    def __init__(self):
        gpsd.connect()
        self.errors = []; self.latitude = []; self.longitude = []; self.tempo = []
        self.historico_tempo = []; self.x = []; self.y = []
        self.historico_diff_ang = []
        self.distancia_prox_cone = []
        self.historico_y = []; self.historico_x = []
        self.instante_inicial = time.time()
        self.angulo_primeiro_cone = 24.676863170337057 #(np.arctan((17/37))/(np.pi))*180
        self.angulo_segundo_cone = 29.054604099077146 #(np.arctan((10/18))/(np.pi))*180
        self.angulo_terceiro_cone = 33.690067525979785 #(np.arctan((16/24))/(np.pi))*180
        self.distancia_primeiro_cone = 40.718546143004666 #np.sqrt(17**2+37**2)
        self.distancia_segundo_cone = 20.591260281974 #np.sqrt(18**2+10**2)
        self.distancia_terceiro_cone = 28.844410203711913 #np.sqrt(16**2+24**2)
        self.cone_atual = 1 # primeiro cone
        self.primeiro_cone_xy = [19.706534,-39.04558] # mudar aqui dependendo da convencao lat long
        self.segundo_cone_xy = [-11.29724,10.991958] # mudar aqui dependendo da convencao lat long
        self.terceiro_cone_xy = [16.121901,24.63018] # mudar aqui dependendo da convencao lat long
        self.distancia_rel_inicial = []
        self.historico_diff_ang.append(0)
        self.distancia_prox_cone.append(0)#gambiarra
#        self.LatitudeCone1  = #a
#        self.LongitudeCone1 = #b
#        self.LatitudeCone2  = #c
#        self.LongitudeCone2 = #d
#        self.LatitudeCone3  = #e
#        self.LongitudeCone3 = #f
    #while  True:
        # Get gpsd position

    def confirmacao_cone(self):
        self.cone_atual += 1 # vamos para o proximo cone
        self.errors = []; self.latitude = []; self.longitude = []; self.tempo = []
        self.historico_tempo = []; self.historico_diff_ang = []
        self.historico_y = []; self.historico_x = []
        self.distancia_prox_cone = []
    def obter_leituras(self):
        self.x = []
        self.y = []
 
        for i in range(0,20):
            packet = gpsd.get_current()
            
            self.pp = packet.position()
            # See the inline docs for GPSResponse for the available data
            self.y.append(111030 * self.pp[0]) #lat -NOSSA E NEGATIVA
            self.x.append(101930 * self.pp[1]) #long -NOSSA E NEGATIVA
            #print(self.pp)
            #sleep(0.3)
            
            pos_prec = packet.position_precision()
            #print(pos_prec)
            #sleep(0.3)
            
            for keys,values in packet.error.items():
                self.errors.append([keys,values])
            #    print([keys,values])
            #sleep(0.3)
            
            self.speed = packet.speed()
            #print(packet.speed())
            #sleep(0.3)
            
            self.mov = packet.movement()
            #print(packet.movement())
            #sleep(0.3)
        
        self.historico_tempo.append(time.time() - self.instante_inicial)
        self.historico_y.append(np.median(self.y))
        self.historico_x.append(np.median(self.x))
        #print("Tempo (s): " + str(self.historico_tempo))
        #print("X (m): " + str(self.historico_y))
        #print("Y (m): " + str(self.historico_y))
        #tem que transformar em um vetor de mediana x = np.median(y)
        #self.posicao_leitura = [y,x]
        
        return self.historico_tempo, self.historico_y, self.historico_x

    # lat long SCdS -23.6267678,-46.5939195

    def logica_localizacao(self):
        
        self.obter_leituras()
        self.obter_leituras()

        if (self.cone_atual == 1):
                
            diff_x = self.historico_x[-1] - self.historico_x[0]
            diff_y = self.historico_y[-1] - self.historico_y[0]        
            #print("Diff_x: " + str(diff_x) + " Diff_y: " + str(diff_y) + "\n")
            ang_atual = (np.arctan((diff_y/diff_x))/(np.pi))*180
            #print("ang_atual: " + str(ang_atual))
            diff_ang = ang_atual - self.angulo_primeiro_cone
            #print("diff_atual: " + str(diff_ang))
            self.historico_diff_ang.append(diff_ang)
            
            self.distancia_prox_cone_x = self.primeiro_cone_xy[0] - diff_x
            self.distancia_prox_cone_y = self.primeiro_cone_xy[1] - diff_y
            print("dist prox cone x: " + str(self.distancia_prox_cone_x) + "dist prox cone y: " + str(self.distancia_prox_cone_y) + "\n" + "angulo com angulo principal: " + str(diff_ang))
            #self.distancia_rel_inicial.append(np.sqrt(diff_x**2+diff_y**2))
            self.distancia_prox_cone.append(np.sqrt(self.distancia_prox_cone_x**2+self.distancia_prox_cone_y**2))
             
        elif (self.cone_atual == 2):
            
            diff_x = self.historico_x[-1] - self.historico_x[0]
            diff_y = self.historico_y[-1] - self.historico_y[0]        
            
            ang_atual = (np.arctan((diff_y/diff_x))/(np.pi))*180
            diff_ang = ang_atual - self.angulo_segundo_cone
            
            self.historico_diff_ang.append(diff_ang)
            
            self.distancia_prox_cone_x = self.segundo_cone_xy[0] - diff_x
            self.distancia_prox_cone_y = self.segundo_cone_xy[1] - diff_y
            
            self.distancia_prox_cone.append(np.sqrt(self.distancia_prox_cone_x**2+self.distancia_prox_cone_y**2))
            
        elif (self.cone_atual == 3):
            
            diff_x = self.historico_x[-1] - self.historico_x[0]
            diff_y = self.historico_y[-1] - self.historico_y[0]        
            
            ang_atual = (np.arctan((diff_y/diff_x))/(np.pi))*180
            diff_ang = ang_atual - self.angulo_terceiro_cone
            
            self.historico_diff_ang.append(diff_ang)
            
            self.distancia_prox_cone_x = self.terceiro_cone_xy[0] - diff_x
            self.distancia_prox_cone_y = self.terceiro_cone_xy[1] - diff_y
            
            self.distancia_prox_cone.append(np.sqrt(self.distancia_prox_cone_x**2+self.distancia_prox_cone_y**2))
        return self.historico_diff_ang, self.distancia_prox_cone#self.distancia_rel_inicial
    
    # Pensar em uma forma em que o robo checa a sua posicao atual e se direciona para o seu destino 
    ## se o robo estiver fora do eixo, calcular o angulo necessario para se direcionar ao destino
