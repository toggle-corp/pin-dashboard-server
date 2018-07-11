from shapely.geometry import Point, asShape
import random


def get_random_point(geojson):
    polygon = asShape(geojson)
    minx, miny, maxx, maxy = polygon.bounds
    pnt = None
    while True:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        pnt = Point(x, y)
        if polygon.contains(pnt):
            break
    return pnt
