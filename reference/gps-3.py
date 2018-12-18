import gpsd
from time import sleep

# Connect to the local gpsd
gpsd.connect()

# Connect to somewhere else
# gpsd.connct(host="127.0.0.1", port=123456)

while True:
    # Get gpsd position
    packet = gpsd.get_current()

    # See the inline docs for GPSResponse for the available data
    print(packet.position())
    sleep(0.3)
    print(packet.position_precision())
    sleep(0.3)
    for keys,values in packet.error.items():
        print([keys,values])
    sleep(0.3)
    print(packet.speed())
    sleep(0.3)
    print(packet.movement())
    sleep(0.3)
