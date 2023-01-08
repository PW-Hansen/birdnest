import math
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

from .models import Drone


# calc_distance constants
NEST_X, NEST_Y = 250.0, 250.0

# read_xml constants
GUARDB1RD_URL = 'https://assignments.reaktor.com/birdnest/drones'
INFORMATION = ['serialNumber', 'positionX', 'positionY']

# update_drones constants
PERSIST_TIME = 1 # Minutes
NDZ_PERIMETER = 100 # Meters

def calc_distance(pos_x, pos_y):
    '''
    Takes in x- and y-positions (in meters) and returns their distance (in meters) to the bird nest.
    '''
    delta_x = NEST_X - float(pos_x)
    delta_y = NEST_Y - float(pos_y)

    dist = math.sqrt((delta_x**2 + delta_y ** 2))

    return dist

def read_guardb1rd_xml():
    '''
    Takes a GUARDB1RD XML-file and returns the time as well as a list of drone dictionaries, 
    each of which contains information about a drone, such as its serial number and positional values.
    '''
    r = requests.get(GUARDB1RD_URL)

    guardb1rd_xml = r.content.decode('utf-8')

    tree = ET.ElementTree(ET.fromstring(guardb1rd_xml))
    root = tree.getroot()

    time = root.find('capture').attrib['snapshotTimestamp'][:-5] # The milliseconds are superflous.

    drone_list = []

    drones = root.find('capture').findall('drone')

    for drone in drones:
        drone_dict = {}
        
        for info in INFORMATION:
            value = drone.find(info).text
            if 'position' in info:
                value = float(value) / 1000.0 # Converts to m, rather than mm.
            drone_dict[info] = value

        distance = calc_distance(drone_dict['positionX'], drone_dict['positionY'])

        drone_dict['distance'] = round(distance,2)

        drone_list.append(drone_dict)
        
    return time, drone_list

def update_drones():
    time, drone_list = read_guardb1rd_xml()

    time = time[11:]
    dt_time = datetime.strptime(time, "%H:%M:%S")

    for drone in drone_list:
        serial_number, distance = drone['serialNumber'], drone['distance']
        # Update drone if it already exists in the database.
        if Drone.objects.filter(serial_number = serial_number).exists():
            drone_db = Drone.objects.get(serial_number = serial_number)

            if drone_db.closest_approach > distance:
                drone_db.closest_approach = distance

            drone_db.last_seen = time

        # Otherwise, add the drone to the database.
        else:
            drone_db = Drone(serial_number = serial_number, closest_approach = distance, last_seen = time)

        drone_db.save()

    for db_drone in Drone.objects.all():
        # Delete drones from database if they're not currently seen and if they haven't violated the NDZ.
        if db_drone.last_seen != time:
            if db_drone.closest_approach > NDZ_PERIMETER:
                db_drone.delete()
            # Otherwise, the drone's information will persist for a number of minutes equal to the persist time constant.
            else:
                dt_last_seen = datetime.strptime(db_drone.last_seen, "%H:%M:%S")

                delta = dt_time - dt_last_seen
                time_delta = delta.total_seconds() / 60 # Minutes

                if time_delta > PERSIST_TIME:
                    db_drone.delete()



