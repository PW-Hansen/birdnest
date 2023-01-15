import math
import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime
from django.utils import dateparse

from .models import Drone, Pilot


# calc_distance constants
NEST_X, NEST_Y = 250.0, 250.0

# read_xml constants
GUARDB1RD_URL = 'https://assignments.reaktor.com/birdnest/drones'
INFORMATION = ['serialNumber', 'positionX', 'positionY']

# query_pilot constants
PILOT_URL = 'https://assignments.reaktor.com/birdnest/pilots/'

# update_drones constants
PERSIST_TIME = 60 * 2 # Seconds
NDZ_PERIMETER = 100 # Meters

# generate_violating_pilots_string constants
BASE_STRING = '''{PILOT_NAME} flew within {DRONE_DISTANCE} of the bird nest using the drone {DRONE_DB}, last seen {DRONE_TIME}. Contact them at {PILOT_PHONE} or {PILOT_EMAIL}.  
'''

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

    timestamp = root.find('capture').attrib['snapshotTimestamp'] # The milliseconds are superflous.
    time = dateparse.parse_datetime(timestamp)

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

def query_pilot(drone_db):
    pilot_url = PILOT_URL + drone_db.serial_number
 
    r = requests.get(pilot_url)
    pilot_string = r.content.decode('utf-8')
    pilot_JSON = json.loads(pilot_string)

    name = f"{pilot_JSON['firstName']} {pilot_JSON['lastName']}"
    phone = pilot_JSON['phoneNumber']
    email = pilot_JSON['email']

    pilot = Pilot(drone = drone_db, name = name, email = email, phone = phone)
    pilot.save()


def update_drones():
    time, drone_list = read_guardb1rd_xml()

    for drone in drone_list:
        serial_number, distance = drone['serialNumber'], drone['distance']
        # Update drone if it already exists in the database.
        if Drone.objects.filter(serial_number = serial_number).exists():
            drone_db = Drone.objects.get(serial_number = serial_number)

            if drone_db.closest_approach > distance:
                drone_db.closest_approach = distance

            drone_db.last_seen = time

            drone_db.save()


        # If the drone isn't in the database and is too close to the birdnest, add the drone to the database.
        elif distance < NDZ_PERIMETER:
            drone_db = Drone(serial_number = serial_number, closest_approach = distance, last_seen = time)

            drone_db.save()
            query_pilot(drone_db)


    for db_drone in Drone.objects.all():
        last_seen_delta = (time - db_drone.last_seen).total_seconds()

        # Delete drones from database if they're not currently seen and haven't violated the NDZ.
        if db_drone.last_seen != time:
            if db_drone.closest_approach > NDZ_PERIMETER:
                db_drone.delete()
            # Otherwise, the drone's information will persist for a number of seconds equal to the persist time constant.
            else:
                if last_seen_delta > PERSIST_TIME:
                    db_drone.delete()

def generate_violating_pilots_string():
    update_drones()

    violating_pilots_string = ''

    for pilot in Pilot.objects.all():
        drone = pilot.drone

        time = f'{drone.last_seen:%H:%M:%S}'

        pilot_string = BASE_STRING.format(
            PILOT_NAME = pilot.name,
            PILOT_PHONE = pilot.phone,
            PILOT_EMAIL = pilot.email,
            DRONE_DISTANCE = drone.closest_approach,
            DRONE_DB = drone.serial_number,
            DRONE_TIME = time
        )

        violating_pilots_string += pilot_string
    
    return violating_pilots_string


