************************

## Circle of GPS Co-ords

    - An example of the direct problem of geodesy...
    - For fun, have attempted to do this 'properly', though completely unnecessarily.
    - Version_1_Haversine uses the spherical Haversine formula to the determine the points list.
    - This version uses geopy to use an ellipsoidal model. It also produces well-formatted gpx files.

******************************************

## What I Learnt

### In general:

- An indirect problem in geodesy is the problem of finding the distance and bearing between two co-ordinate points.
- A direct problem referes to finding a destination co-ordinate, given an origin, bearing and distance.
- Beaing can be given in true heading which is degrees clockwise from North.
- We recall that latitudes are horizontal and parallel, while longitudes (a.k.a. meridans) are great circles vertical on the globe.

### Models and Accuarcy...

- There are many formula, depending on the model: https://www.movable-type.co.uk/scripts/latlong.html
- For the actual problem in which distances are less than a kilometre, the Euclidean (flat) model would work fine. This is true for distances up to around 10 km. But for the fun of learning, I have ignored this case.
- The spherical model works if moving along distances in longitutde but not latitude, and if the polar regions where the planet is squashed are not in play. The haversine formula is used in this case, which has an accuracy of metres on kilometre scales.
- A better approximation to the real shape of the Earth is the Ellipsoidal model. There are several formula to calculate the distance in this case, the most standard (to me at least, since impmented in geopy) is the Karney formula, which is an adaption of the Vincenty formula. In general, the Vincenty formula has millimeter precision, though may not converge for antipodal points, whle the Kerney has nanometer precision and does not have convergence problems. https://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing

### Haversine function:

- Half Versed Sine.
- Is used for calculating the distance on a sphere. Also called the great circle formula.
- Can be used for the indirect problem if the spherical approximation is valid.  https://community.esri.com/t5/coordinate-reference-systems-blog/distance-on-a-sphere-the-haversine-formula/ba-p/902128#:~:text=All%20of%20these%20can%20be,longitude%20of%20the%20two%20points
- Havng said that however, for small distances the standard law of cosines may be a better approach as it avoids computational round-off (this comparison can only be made for spherical models), while for larger distances, it is better to not use the haversine but an ellipsoidal model. https://gis.stackexchange.com/questions/4906/why-is-law-of-cosines-more-preferable-than-haversine-when-calculating-distance-b

### Misc.

DD vs. DMS:

- In converting from the deciaml (DD, decimal degrees) to sexagesimal (DMS, degrees minutes seconds) systems, use:  (degrees)+(minutes/60)+(seconds/3600) = decimal degrees. https://www.fao.org/4/y4816e/y4816e0e.htm#:~:text=The%20first%20method%20divides%20each,12%C2%B0%2030'00%E2%80%9D.

Decimals & precision in co-ordinates:
- Approximately, 4 decimals corrsponds to a street, 6 to a person, 7 is practical limit of srveying, and 8 is in the purview of specialised studies. https://hikingguy.com/how-to-hike/what-is-a-gpx-file/
Geocentric vs Geodetic Latitudes:
- Geocentric latatitudes are latitudes on a sphere, geodetic latitudes are latitudes on a ellipsoid.
- Most map applications use geodetic form.
- Android getLocation can be assumed to use geodetic latitudes for the GPS location.
- GPS uses the WGS84 ellipsoid model.
- Simply, spherical formula cannot be applied to geodetic (ellipsoidal) data, ie GPS co-ordinates. https://gis.stackexchange.com/questions/296608/what-kind-of-margin-of-error-can-i-expect-in-figuring-distance

GPS exchange format: .gpx
- An open standard xml file for GPS trackers. Good practice to validate, new lines/indents between tags are necessary.
- It is recommended to reference two namespaces. I have not done this, and it still seems to work/validate... https://www.topografix.com/gpx_manual.asp

*******************************************
