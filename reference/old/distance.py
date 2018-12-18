# Distance sensor example

from gpiozero import DistanceSensor
import time

sensor = DistanceSensor(15,4)

def main() :
    while (True):
        distance = sensor.distance * 100 # distance in centimeters
        print("distance",distance)
        if distance >= 10.0:
            distance = 16.0

# Main program logic:
if __name__ == '__main__':
    main()
