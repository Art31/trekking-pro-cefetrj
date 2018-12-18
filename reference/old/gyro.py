# L3G4200D

import smbus
import time

class Gyroscope:
    def __init__(self):
            
        # Get I2C bus
        self.bus = smbus.SMBus(1)

        # L3G4200D address, 0x69(105)
        # Select Control register1, 0x20(32)
        # 0x0F(15) Normal mode, X, Y, Z-Axis enabled
        self.bus.write_byte_data(0x69, 0x20, 0x0F)
        # L3G4200D address, 0x69(105)
        # Select Control register4, 0x23(35)
        # 0x30(48) Continous update, Data LSB at lower address
        # FSR 2000dps, Self test disabled, 4-wire interface
        self.bus.write_byte_data(0x69, 0x23, 0x30)

        time.sleep(0.5)

    def read(self):
        # L3G4200D address, 0x69(105)
        # Read data back from 0x28(40), 2 bytes, X-Axis LSB first
        data0 = self.bus.read_byte_data(0x69, 0x28)
        data1 = self.bus.read_byte_data(0x69, 0x29)

        # Convert the data
        xGyro = data1 * 256 + data0
        if xGyro > 32767 :
                xGyro -= 65536

        # L3G4200D address, 0x69(105)
        # Read data back from 0x2A(42), 2 bytes, Y-Axis LSB first
        data0 = self.bus.read_byte_data(0x69, 0x2A)
        data1 = self.bus.read_byte_data(0x69, 0x2B)

        # Convert the data
        yGyro = data1 * 256 + data0
        if yGyro > 32767 :
                yGyro -= 65536

        # L3G4200D address, 0x69(105)
        # Read data back from 0x2C(44), 2 bytes, Z-Axis LSB first
        data0 = self.bus.read_byte_data(0x69, 0x2C)
        data1 = self.bus.read_byte_data(0x69, 0x2D)

        # Convert the data
        zGyro = data1 * 256 + data0
        if zGyro > 32767 :
                zGyro -= 65536

        return (xGyro, yGyro, zGyro)
