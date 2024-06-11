



def dms2dd(dms):
    """Quick conversion from sexagesimal (dms) to decimal (dd).
    Assumes [long, lat] form of input."""

    dd = []

    for p in dms:
        d, m, s = p
        p_dd = d + (m / 60) + (s / 3600)
        dd.append(p_dd)

    return dd


def dd2dms(dd):
    """Quick conversion from decimal (dd) to sexagesimal (dms).
    Assumes [long, lat] form of input."""

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


def test_conversions():

    point_1 = [78.9239722, 11.9233056]

    print("Test Point:")
    print(point_1)
    identify_point_type(point_1)

    print("Converting point from DMS to DD:")
    point_1_dms = dd2dms(point_1)
    print(point_1_dms)
    print("Converting point from DD to DMS:")
    print(dms2dd(point_1_dms))

    point_2 = [(78, 56, 34.68), (11, 51, 19.78)]

    print("Test Point:")
    print(point_2)
    identify_point_type(point_2)

    print("Converting point from DMS to DD:")
    point_2_dd = dms2dd(point_2)
    print(point_2_dd)
    print("Converting point from DD to DMS:")
    print(dd2dms(point_2_dd))



if __name__ == '__main__':

    test_conversions()
