import RPi.GPIO as GPIO
import time
##import argparse
##
##ap = argparse.ArgumentParser()
##ap.add_argument("-sp", "--servo_pin", required=True,
##	help="servo_pin")
###ap.add_argument("-ar", "--ang_rotacao", required=True,
###	help="ang_rotacao")
##ap.add_argument("-p", "--posicao", required=True,
##	help="posicao")
##args = vars(ap.parse_args())

class Servo():
    def __init__(self, servo_pin):
        self.pin = servo_pin
        self.degree = 0
        self.veloc_pwm_horario = 6.8
        self.veloc_pwm_anti_horario = 7.3
        self.deg_pwm_ah_seg = -42.8571
        self.deg_pwm_h_seg = 47.3684
        self.veloc_pwm_stop = 0

        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.p = GPIO.PWM(self.pin, 50) # 50Hz
        self.p.start(0) # 0 = parado

    def rodar(self, ang_rotacao):
        self.degree = self.degree - ang_rotacao
        if ang_rotacao == 0:
            return
        elif ang_rotacao < 0:
            rotate_time = (ang_rotacao/self.deg_pwm_ah_seg)
            self.p.ChangeDutyCycle(self.veloc_pwm_anti_horario)
            time.sleep(rotate_time)
            self.p.ChangeDutyCycle(self.veloc_pwm_stop)
        elif ang_rotacao > 0:
            rotate_time = (ang_rotacao/self.deg_pwm_h_seg)
            self.p.ChangeDutyCycle(self.veloc_pwm_horario)
            time.sleep(rotate_time)
            self.p.ChangeDutyCycle(self.veloc_pwm_stop)

    def posicionar(self, posicao):
        rot = self.degree - posicao
        self.rodar(rot)


##sv = Servo(int(args["servo_pin"])) 
###sv.rodar(args["ang_rotacao"])
##sv.posicionar(int(args["posicao"]))

