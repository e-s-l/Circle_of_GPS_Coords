##################
# CircleGPSPoints
# Given a centre, calculate a circle of gps co-ords around this using an inverse haversine formula.
# In other words, we solve a direct problem of deteriming a destination given distance & bearing
# using a spherical approximation, full all bearings, thus producing a circle of points.
# This appraoch is considered to ahve m accuracy on km length scales (see links below)... Good enough.
# Designed to determine co-ordinates delineating a RQZ/mobile-no-go zone around a radio observatory.
# See http://www.movable-type.co.uk/scripts/latlong.html
# https://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing
# ESL
##################

from math import asin, atan2, cos, degrees, radians, sin, sqrt
import sys
from xml.etree.ElementTree import Element, SubElement, ElementTree


def create_text_file(points, file_name="test_circle"):
    """Save the list of points as a csv-style text file."""

    # add appropriate extension:
    file = "%s.txt" % file_name

    # open and write:
    with open(file, 'w') as file:
        for lat, long in points:
            file.write(f"{lat}, {long}\n")


def create_gpx_file(points, file_name="test_circle"):
    """I asked chatgpt to write me a function to save list as gpx file...
    I have never used them so not really sure about this.
    But seems to load up ok... Tested with Organic maps."""

    # add appropriate extension:
    file = "%s.gpx" % file_name

    # hmmm
    gpx = Element('gpx', version="1.1", creator="GPXGenerator")
    trk = SubElement(gpx, 'trk')
    trkseg = SubElement(trk, 'trkseg')

    for lat, lon in points:
        SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))

    tree = ElementTree(gpx)

    tree.write(file, xml_declaration=True, encoding='utf-8')


def generate_circle(centre, radius, num_points=360):
    """Create a list of co-ordinates defining a circle around some centre.
     Takes in a central co-ordinate, a radius [metres] and number of points/resolution"""

    # initialise empty points list:
    points_list = []

    # get the lat, long of centre
    lat_c, long_c = centre

    # convert radius to kilometres
    distance = radius / 1000.0

    # loop through the number of points:
    for i in range(num_points + 1):

        # get true bearing (ie degrees clockwise from north) for each point
        dtheta = float(i) * 360.0 / num_points

        # call get points function:
        point = get_point_at_distance(lat_c, long_c, distance, dtheta)

        # strip to 6 decimal places
        point = float(format(point[0], '.6f')), float(format(point[1], '.6f'))

        points_list.append(point)

    # done:
    return points_list


def get_point_at_distance(lat_i, long_i, d, b, r=6371):
    """Given an initial lat, long (in degrees),
     and distance (d) [km], and bearing (b) [degrees],
      uses mean radius of earth R"""

    lat1 = radians(lat_i)
    long1 = radians(long_i)
    a = radians(b)

    lat2 = asin(sin(lat1) * cos(d/r) + cos(lat1) * sin(d/r) * cos(a))
    long2 = long1 + atan2(sin(a) * sin(d/r) * cos(lat1), cos(d/r) - sin(lat1) * sin(lat2))

    return [degrees(lat2), degrees(long2)]


def haversine_distance(point1, point2, r=6371):
    """Given two co-ordinates, find the distance between them using the haversine formula."""

    lat1, long1 = point1
    lat2, long2 = point2

    phi1 = radians(lat1)
    phi2 = radians(lat2)

    dphi = radians(lat2 - lat1)
    dlambda = radians(long2 - long1)

    a = (sin(dphi / 2.0) ** 2) + cos(phi1) * cos(phi2) * (sin(dlambda / 2.0) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    metres = r * c
    metres = float('%.3f' % metres)

    return metres


def sanity_check(centre, coord_list):
    """Prints the results of the haversine distance formula between the centre and each point of the circle."""

    for lat, long in coord_list:
        point = [lat, long]
        distance = haversine_distance(centre, point)
        distance = distance*1000
        print(distance)


def main_function():
    """Load in parameters and run the component functions."""

    # some debug:
    sanity_check_switch = True                      # to print to standard output the recalculated radii
    test_point = [78.9239722, 11.9233056]           # my bedroom, in DD

    #
    centre = test_point                             # lat, long, DD (decimal) or DMS (sexagesimal) ?
    radius = 900                                    # in metres

    # get the circle of points
    coord_list = generate_circle(centre, radius)
    # just for fun
    if sanity_check_switch:
        sanity_check(centre, coord_list)

    # create 'descriptive' file name
    file_name = "%sm_RQZ_Circle_w_Centre_%.3f_%.3f" % (radius, centre[0], centre[1])
    # save the circle of points
    create_text_file(coord_list, file_name)         # as csv-style text file
    create_gpx_file(coord_list, file_name)          # as .gpx file...


if __name__ == '__main__':

    try:
        main_function()
    except Exception as e:
        print(e)
        sys.exit(1)
