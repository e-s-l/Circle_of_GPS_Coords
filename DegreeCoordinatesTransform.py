##################################
# DECICMAL/SEXAGESIMAL CONVERTOR #
##################################


def dms2dd(dms):
    """Quick conversion from sexagesimal (dms) to decimal (dd).
    Assumes [long, lat] form of input."""

    print("Converting point from DMS to DD.")

    dd = []

    for p in dms:
        d, m, s = p
        p_dd = d + (m / 60) + (s / 3600)
        dd.append(p_dd)

    return dd


def dd2dms(dd):
    """Quick conversion from decimal (dd) to sexagesimal (dms).
    Assumes [long, lat] form of input."""

    print("Converting point from DD to DMS.")

    dms = []

    for l in dd:

        # modulus to get decimal part:
        l_m = (l % 1) * 60
         # round to get whole number component:
        l_d = int(l)
        # minutes & seconds
        l_s = (l_m % 1) * 60
        l_m = int(l_m)

        dms.append((l_d, l_m, l_s))

    return dms

###

def identify_point_type(p):
    """Find whether co-ord has DD or DMS type values"""

    point_type = ""

    # first make sure is co-ordinate pair
    if len(p) == 2:

        if isinstance(p[0], float):
                point_type = "DD"

        elif len(p[0]) == 3:
            point_type = "DMS"

        print("Co-ord has %s form" % point_type)

    return point_type

###

def convert_type(coord):
    """Find coord type and convert to alternative form"""

    print(coord)

    type = identify_point_type(coord)

    if type == "DD":
        coord_converted = dd2dms(coord)
    elif type == "DMS":
         coord_converted = dms2dd(coord)

    print(coord_converted)
    return coord_converted


def test_conversions():
    """Debug: run through some example points"""

    # test points:
    p1 = [78.9239722, 11.9233056]
    p2 = [(78, 56, 34.68), (11, 51, 19.78)]

    points_original = [p1, p2]
    points_converted = []

    for point in points_original:

        p_c = convert_type(point)
        points_converted.append(p_c)

    # sanity check:
    for point in points_converted:
        convert_type(point)



if __name__ == '__main__':

    test_conversions()
