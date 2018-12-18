from multiprocessing import Process
from threading import Thread
from lib.encoder import Encoder
from lib.gyro import Gyroscope
from hcsr04sensor import sensor as Ultra
from time import time

# = PIN DEFINITIONS =

# == RANGE ==
# Ultrasonic sensor A
trigA = 19
echoA = 22
# Ultrasonic sensor B
#trigB = 13
#echoB = 27
# Ultrasonic sensor C
#trigC = 6
#echoC = 17

# == ENCODER ==
# Encoder sensor A
pinEncA = 26
# Encoder sensor B
#pinEncB = 20

# == GYROSCOPE ==
# Gyroscope uses pins 2 and 3


# = SETUP SENSORS =
ultraA = Ultra.Measurement(trigA, echoA)
#ultraB = Ultra.Measurement(trigB, echoB)
#ultraC = Ultra.Measurement(trigC, echoC)

encA = Encoder(pinEncA)
#encB = Encoder(pinEncB)

gyroA = Gyroscope()

# = AUXILIARY FUNCTIONS =
def ultraA_read():
    tpp = time()
    while (True):
        raw = ultraA.raw_distance(sample_size=1, sample_wait=0.1)
        metric = ultraA.distance_metric(raw)

        #sleep(1)
        if (time() - tpp > 1):
            tpp = time()
            print("Distancia:", metric)

def encA_read():
    state = encA.read()
    while (True):
        pstate = state
        state = encA.read()
        if (state != pstate):
            print("Encoder: change to", state)

def gyroA_read():
    tpp = time()
    while (True):
        if (time() - tpp > 1):
            tpp = time()
            print("Ângulo: ", gyroA.getDeg()[2])
            #sleep(1)
        

# = READING FUNCTIONS =
readings = []
readings.append(Process(target=ultraA_read))
readings.append(Process(target=encA_read))
readings.append(Process(target=gyroA_read))
for reading in readings:
    reading.start()
