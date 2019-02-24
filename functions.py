def great_circle_distance(pt1, pt2):
    """Takes two coordinates (lat,lng)
    Calculates distance considering earths roundness
    Returns distance by meters"""
    import math
    lat1, lon1 = pt1
    lat2, lon2 = pt2
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))*radius
    return c*1000


def moving_average(array, window=3):
     import numpy as np
     ret = np.cumsum(array, dtype=float)
     ret[window:] = ret[window:] - ret[:-window]
     return ret[window - 1:] / window