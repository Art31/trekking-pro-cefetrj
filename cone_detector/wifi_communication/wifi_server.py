# --------------------------------------------------------------------------- #
# Title: Wifi/Ethernet communication server script
# Author: Arthur Telles
# Date: 04/07/2018 (DD/MM/YYYY)
# Description: This function opens up a port for wifi/ethernet communication 
# and listens to the channel, if it receives a string, it crops part of it to 
# extract the angle. If the string received contains "flag" as content, it 
# breaks the listening loop.
# --------------------------------------------------------------------------- #

# taken from https://pymotw.com/3/socket/tcp.html

import socket
import sys
import time

class wifi_rx():
    def receber(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address given on the command line
        # You may extract this address from a rpi3 with ifconfig
        server_name = '192.168.43.62' 
        server_address = (server_name, 10000)
        #print (str(sys.stderr) + 'starting up on %s port %s' % server_address)
        sock.bind(server_address)
        sock.listen(1)
        data = False
        flag = False

        while not(flag):
            #print (str(sys.stderr) + 'waiting for a connection')
            connection, client_address = sock.accept()
            try:
                #print(sys.stderr) 
                #print('client connected:')
                #print(client_address)
                while not(flag):
                    data2 = connection.recv(64)
                    #print ('received "%s' % data2)
                    #print("data 2: " + str(data2))
                    # cropping the strint to extract the desired part
                    self.angulo = str(data2)[2:-1]
                    self.retornar(self.angulo)
                    time.sleep(0.005)
                    print("Received message: {}".format(self.angulo))
                    if data2:
                        connection.sendall(data2)
                        data = data2
                        if (str(data2)[2:-1] == "flag"): 
                            flag = data                    
                            break
                    else:
                        break
            finally:
                connection.close()
    def retornar(self,angulo):
        print("Relooping and listening again...")
        return angulo

#a = wifi_rx()
#a.receber()
#b = a.retornar()
#print(b)

