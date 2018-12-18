import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
PinServo = 0 #definir pino
GPIO.setup(PinServo, GPIO.OUT)

AngServo = GPIO.PWM(PinServo,100) # channel = PinServo frequency = 50Hz
AngServo.start(0) #dutycycle


def ServoControl(Angulo):
    """
    Recebe um ângulo para o qual desejamos que o servo esteja
    """
    #converter angulo do servo para PWM do servo
    #chamar função AngServo.changeDutyCycle(dc)

    pass

def RobotControl(Angulo):
    """
    Recebe um ângulo para o qual vai virar o robô.
    """
    # converter angulo do robo pra angulo do servo
    # chamar função de controle do servo

    pass





