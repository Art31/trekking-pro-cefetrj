import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
p = GPIO.PWM(17, 330) # 330Hz
p.start(0) # 0 = parado.
p.ChangeDutyCycle(17.5)

for i in range(0,100):
    p.ChangeDutyCycle(i)
    time.sleep(0.05)
    print(i)

for i in range(0,100):
    i = 100 - i
    p.ChangeDutyCycle(i)
    time.sleep(0.05)
    print(i)


GPIO.cleanup()
