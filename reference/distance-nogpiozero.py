from hcsr04sensor import sensor

def main():
    '''Calculate the distance of an object in centimeters using a HCSR04 sensor
       and a Raspberry Pi'''

    trig_pin = 14
    echo_pin = 15

    #  Create a distance reading with the hcsr04 sensor module
    value = sensor.Measurement(trig_pin, echo_pin)
    while (True): 
        raw_measurement = value.raw_distance()

        # Calculate the distance in centimeters
        metric_distance = value.distance_metric(raw_measurement)
        print("The Distance = {} centimeters".format(metric_distance))

if __name__ == "__main__":
    main()
