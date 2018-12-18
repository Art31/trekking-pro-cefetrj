#!/usr/bin/python

# Read the L3G4200D sensor
# Code based on https://github.com/bashardawood/L3G4200D-Python
# by bashardawood
# Adapted to python3 by Lucas Fernandes

#from time import sleep
from time import time
#import smbus to access i2c port
import smbus
from multiprocessing import Process
from multiprocessing import Queue
#import threading

class Gyroscope:
    def __init__(self):
        #open /dev/i2c-1
        self.i2c_bus=smbus.SMBus(1)
        #i2c slave address of the L3G4200D
        self.i2c_address=0x69

        #initialise the L3G4200D

        #normal mode and all axes on to control reg1
        self.i2c_bus.write_byte_data(self.i2c_address,0x20,0x0F)
        #full 2000dps to control reg4
        #self.i2c_bus.write_byte_data(self.i2c_address,0x23,0x20)
        #self.i2c_bus.write_byte_data(self.i2c_address,0x23,0xA0)
        self.i2c_bus.write_byte_data(self.i2c_address,0x23,0x80)

        self.offset = (1.0549967208814246,
                       -0.23210027544595899,
                       1.5920714192025232)

        self.degree = Queue()
        #thread = threading.Thread(target=self.updateDeg, args=())
        thread = Process(target=self.updateDeg, args=())
        #thread.daemon = True
        thread.start()


    #converts 16 bit two's compliment reading to signed int
    def getSignedNumber(self,number):
        if number & (1 << 15):
            return number | ~65535
        else:
            return number & 65535


    #read lower and upper bytes, combine and display
    def read(self):


        self.i2c_bus.write_byte(self.i2c_address,0x28)
        self.X_L = self.i2c_bus.read_byte(self.i2c_address)
        self.i2c_bus.write_byte(self.i2c_address,0x29)
        self.X_H = self.i2c_bus.read_byte(self.i2c_address)
        self.X = self.X_H << 8 | self.X_L

        self.i2c_bus.write_byte(self.i2c_address,0x2A)
        self.Y_L = self.i2c_bus.read_byte(self.i2c_address)
        self.i2c_bus.write_byte(self.i2c_address,0x2B)
        self.Y_H = self.i2c_bus.read_byte(self.i2c_address)
        self.Y = self.Y_H << 8 | self.Y_L

        self.i2c_bus.write_byte(self.i2c_address,0x2C)
        self.Z_L = self.i2c_bus.read_byte(self.i2c_address)
        self.i2c_bus.write_byte(self.i2c_address,0x2D)
        self.Z_H = self.i2c_bus.read_byte(self.i2c_address)
        self.Z = self.Z_H << 8 | self.Z_L

        self.X = self.getSignedNumber(self.X)
        self.Y = self.getSignedNumber(self.Y)
        self.Z = self.getSignedNumber(self.Z)

        #print(str(self.X).rjust(10), end='')
        #print(str(self.Y).rjust(10), end='')
        #print(str(self.Z).rjust(10))
        #sleep(0.01)

        return (self.X * 0.00875 - self.offset[0],
                self.Y * 0.00875 - self.offset[1],
                self.Z * 0.00875 - self.offset[2])

    def readInTime(self):
        t = time()
        r = self.read()
        while (time() - t < 0.01):
            pass
        return r

    def _writeDeg(self, deg):
        try:
            self.degree.get_nowait()
        except:
            self.degree.put_nowait(deg)

    def updateDeg(self):

        self.rx, self.ry, self.rz = (0, 0, 0)

        #ttp = time()
        while True:
            
            ix, iy, iz = self.readInTime()
            self.rx += ix /100
            self.ry += iy /100
            self.rz += iz /100

            self._writeDeg((self.rx, self.ry, self.rz))

            #if (time() - ttp > 1):
            #    print(self.rx, self.ry, self.rz)
            #    ttp = time()


    def getDeg(self):
        return self.degree.get()
