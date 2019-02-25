import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import parse
def distance(origin, destination):
     '''Takes two [x,y] points
     Returns distance'''
     return np.sqrt(   (origin[0]-destination[0])**2+(origin[1]-destination[1])**2)

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

def moving_average(arr, window=3):
     import numpy as np
     ret = np.cumsum(arr, dtype=float)
     ret[window:] = ret[window:] - ret[:-window]
     return ret[window - 1:] / window

def moving_std(arr,window,centered=False):
     import numpy as np
     stds = []
     if centered:
          margin = int(window/2)
          for i in range(margin,len(arr)- margin):
               stds.append(np.std(arr[i-margin:i+margin]))
     else:
          for i in range(window,len(arr)):
               stds.append(np.std(arr[i-window:i]))
     return np.array(stds)

def interpolate_two_points_by_line(pt1,pt2,n=8):
     """"Return a list of nb_points equally spaced points
     between pt1 and pt2
     If we have 8 intermediate points, we have 8+1=9 spaces
     between pt1 and pt2"""

     x_spacing = (pt2[0] - pt1[0]) / (n + 1)
     y_spacing = (pt2[1] - pt1[1]) / (n + 1)

     return [[pt1[0] + i * x_spacing, pt1[1] +  i * y_spacing] for i in range(1, n+1)]

def smooth(arr,window=5,centered = False):
     '''Smooths list replacing by mean
     Returns list'''
     if not centered:
          return [np.mean(arr[i-window+1 if i-window+1 >=0 else 0:i+1]) for i in range(len(arr))]
     else:
          return [np.mean(arr[i-int(np.floor(window/2)) if i-int(np.floor(window/2)) >=0 else 0:i+int(np.ceil(window/2)) if i+int(np.ceil(window/2)) < len(arr) else len(arr)]) for i in range(len(arr))]

def plot(x,y):
     plt.plot(x,y)

def get_nearby_points(point,points,radius,limit):
     '''Takes point and list of points
     Returns sorted(ascending) by distance list of points in radius and by limit'''
     return [p for p in sorted( points,key = lambda d: distance((point[0],point[1]),(d[0],d[1])))[:limit] if distance((point[0],point[1]),(p[0],p[1])) < radius]