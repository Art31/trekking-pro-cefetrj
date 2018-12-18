# --------------------------------------------------------------------------- #
# Title: Wifi/Ethernet communication client script
# Author: Arthur Telles
# Date: 04/07/2018 (DD/MM/YYYY)
# Description: This function opens up a port for wifi/ethernet communication 
# and sends a message with a specific content. Another function is responsible
# for sending the flag message, which deactivates the listening mode in the 
# server and breaks communication.
# --------------------------------------------------------------------------- #

# taken from https://pymotw.com/3/socket/tcp.html

import socket

class wifi():
    # the message at the moment of development represented the angle between the
    # object center and the center of the camera
    def __init__(self,message):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port on the server given by the caller
        server_address = ("192.168.43.62", 10000)
        #print (str(sys.stderr) + 'connecting to %s port %s' % server_address)
        self.sock.connect(server_address)

        try:
            message = str(message).encode('UTF-8')
            #print (str(sys.stderr) + 'sending "%s"' % message)
            self.sock.sendall(message)
        except:
            pass
        finally:
            self.sock.close()
            
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port on the server given by the caller
        server_address = ("192.168.43.62", 10000)
        sock.connect(server_address)
        
    def flag(self):
        message2 = b"flag"
        self.sock.sendall(message2)
        self.sock.close()

#a = wifi("10.2")
#a.flag()