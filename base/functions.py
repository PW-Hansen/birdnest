import math
import xml.etree.ElementTree as ET
import requests

from . import models


# calc_distance constants
NEST_X, NEST_Y = 250.0, 250.0

# read_xml constants
GUARDB1RD_URL = 'https://assignments.reaktor.com/birdnest/drones'
INFORMATION = ['serialNumber', 'positionX', 'positionY']


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

    time = root.find('capture').attrib['snapshotTimestamp'][-5] # The milliseconds are superflous.

    drone_list = []

    drones = root.find('capture').findall('drone')

    for drone in drones:
        drone_dict = {}
        
        for info in INFORMATION:
            value = drone.find(info).text
            if 'position' in info:
                value = float(value) / 1000.0 # Converts to m, rather than mm.
            drone_dict[info] = value

        drone_dict['distance'] = calc_distance(drone_dict['positionX'], drone_dict['positionY'])

        drone_list.append(drone_dict)
        
    return time, drone_list

def update_drones(xml_file):
    time, drone_list = read_guardb1rd_xml(xml_file)

    for drone in drone_list:
        serial_number, distance = drone['serialNumber'], drone['distance']
        if models.Drones.objects.get(id = serial_number):
            drone_db = models.Drones.objects.get(id = serial_number)

            if drone_db.closest_approach > distance:
                drone_db.closest_approach = distance

            drone_db.last_seen = time

        else:
            drone_db = models.Drones(serial_number = serial_number, closest_approach = distance, last_seen = time)

        drone_db.save()
    


