# --------------------------------------------------------------------------- #
# Title: Bluetooth communication server script
# Author: Arthur Telles
# Date: 02/07/2018 (DD/MM/YYYY)
# Description: This function opens up a port for bluetooth communication 
# and waits for the client to send a message, answering with an echo response.
# --------------------------------------------------------------------------- #

# Taken from http://blog.kevindoran.co/bluetooth-programming-with-python-3/

import bluetooth

hostMACAddress = 'B8:27:EB:E6:57:B7' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data) # Echo back to client
except:	
    print("Closing socket")
    client.close()
    s.close()