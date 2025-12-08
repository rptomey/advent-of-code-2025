import math

def point_to_point_distance(point_a, point_b):
    """
    Helper function for finding the distance between two points in space where each point is a tuple of its coordinates.

    See https://en.wikipedia.org/wiki/Euclidean_distance

    Currently expects integers for the coordinate values.
    
    :param point_a: A tuple representing a point in 2d space (x,y) or 3d space (x,y,z) or even a higher number of planes.
    :param point_b: A tuple representing a point in 2d space (x,y) or 3d space (x,y,z) or even a higher number of planes.
    """
    planes = len(point_a)

    total = 0

    for i in range(planes):
        difference = point_a[i] - point_b[i]
        total += (difference ** 2)

    return math.sqrt(total)
