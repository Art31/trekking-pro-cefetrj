import RPi.GPIO as GPIO #https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python
import threading
GPIO.setmode(GPIO.BCM)

#biblias https://github.com/datitran/object_detector_app/blob/master/object_detection_multithreading.py
# https://towardsdatascience.com/building-a-real-time-object-recognition-app-with-tensorflow-and-opencv-b7a2b4ebdc32
# https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
# https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python

class Encoder(threading.Thread):
    def __init__(self, enc_pin):
        self.pin = enc_pin
        GPIO.setup(self.pin, GPIO.IN)

    # mudar essa chamada self para nao roubar memoria, pois uma funcao chama a outra "eternamente"
    def start(self,threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
        state = GPIO.input(self.pin) # ele le o pino pra ver se ta comecando em 1 ou 0
        if state: 
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.detect_fall) # se comecou em 1, detectar descida
        else:
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.detect_rise) # se comecou em 0, detectar subida


    def detect_fall(self, channel):
        print("changed to 0")
        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.detect_rise)

    def detect_rise(self, channel):
        print("changed to 1")
        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.detect_fall)


if __name__ == "__main__":
    enc = Encoder(4)
    enc.start(1, "Encoder-Thread", 1)
    while True:
        pass
