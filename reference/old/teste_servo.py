import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 50)
p.start(2.5)

try:
    while True:

        p.ChangeDutyCycle(10)
        time.sleep(0.1)

        
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
