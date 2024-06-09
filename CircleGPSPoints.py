##################
# CircleGPSPoints
# Given a centre, calculate a circle of gps co-ords around this using an inverse haversine formula.
# Designed to determine co-ordinates delineating a RQZ/mobile-no-go zone around a radio observatory. 
# ESL
##################

import math
import sys
from xml.etree.ElementTree import Element, SubElement, ElementTree


def create_text_file(points, file_name="test_circle.txt"):
    """Save the list of points as a csv-style text file."""

    with open(file_name, 'w') as file:
        for lat, long in points:
            file.write(f"{lat}, {long}\n")


def create_gpx_file(points, file_name="test_circle.gpx"):
    """I asked chatgpt to write me a function to save list as gpx file...
    I have never used them so not really sure about this.
    But seems to load up ok... Tested with Organic maps."""

    gpx = Element('gpx', version="1.1", creator="GPXGenerator")
    trk = SubElement(gpx, 'trk')
    trkseg = SubElement(trk, 'trkseg')

    for lat, lon in points:
        SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))

    tree = ElementTree(gpx)
    tree.write(file_name, xml_declaration=True, encoding='utf-8')


def generate_circle(centre, radius=1000, num_points=360):
    """Create a list of co-ordinates defining a circle around some centre.
     Takes in a central co-ordinate, a radius [metres] and number of points/resolution"""

    # initialise empty points list:
    points_list = []
    # get the lat, long of centre
    lat_c, long_c = centre
    # calculate metres per degree (at this longitude):
    M_PER_DEGREE_LAT = 111320  # constant
    m_per_d_long = M_PER_DEGREE_LAT * math.cos(math.radians(lat_c))
    # loop through the number of points:
    for i in range(num_points + 1):
        # get an angle (in radians) for each point
        dtheta = math.radians(float(i) * 360.0 / num_points)
        dlat = radius * math.cos(dtheta) / M_PER_DEGREE_LAT
        dlong = radius * math.sin(dtheta) / m_per_d_long
        lat_p = lat_c + dlat
        long_p = long_c + dlong
        points_list.append((lat_p, long_p))
    # done:
    return points_list


def haversine_distance(point1, point2):
    """Given two co-ordinates, find the distance between them using the haversine formula."""

    lat1, long1 = point1
    lat2, long2 = point2

    radius_earth = 6371000  # in metres...

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(long2 - long1)

    a = (math.sin(dphi / 2.0) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2.0) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    metres = radius_earth * c
    metres = float('%.3f' % metres)

    return metres


def sanity_check(centre, coord_list):
    """Prints the results of the haversine distance formula between the centre and each point of the circle."""

    for lat, long in coord_list:
        point = [lat, long]
        distance = haversine_distance(centre, point)
        print(distance)


def main_function():
    """Load in parameters and run the component functions."""

    # some debug:
    sanity_check_switch = True
    test_point = [78.9239722, 11.9233056]       # my bedroom

    #
    centre = test_point                         # lat, long, DD (decimal) or DMS (sexagesimal) ?
    radius = 900                                # in metres

    # get the circle of points
    coord_list = generate_circle(centre, radius)
    # just for fun
    if sanity_check_switch:
        sanity_check(centre, coord_list)
    # save the circle of points
    create_text_file(coord_list)                # as csv-style text file
    create_gpx_file(coord_list)                 # as .gpx file...


if __name__ == '__main__':

    try:
        main_function()
    except Exception as e:
        print(e)
        sys.exit(1)
