import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# pin to read data from encoder
enc_pin = 14

GPIO.setup(enc_pin, GPIO.IN)

def enc_read():
    return GPIO.input(enc_pin)

state = 0
while(True):
    pv_state = state
    state = enc_read()
    if (not (state == pv_state)):
        print("changed to", state)
