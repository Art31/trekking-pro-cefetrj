# --------------------------------------------------------------------------- #
# Title: Bluetooth communication client script
# Author: Arthur Telles
# Date: 02/07/2018 (DD/MM/YYYY)
# Description: This function opens up a port for bluetooth communication 
# and send a message to the server.
# --------------------------------------------------------------------------- #

# Taken from http://blog.kevindoran.co/bluetooth-programming-with-python-3/

import bluetooth

serverMACAddress = '4C:34:88:32:82:68'
port = 5
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = "trekking works"
    if text == "quit":
        break
    s.send(text)
sock.close()
