import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import parse
from pprint import pprint
from winsound import Beep as beep

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
          for i in range(window-1,len(arr)):
               stds.append(np.std(arr[i-window+1:i+1]))
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
     plt.figure(figsize=(10,8))
     plt.plot(x,y)

def get_nearby_points(point,points,radius,limit):
     '''Takes point and list of points
     Returns sorted(ascending) by distance list of points in radius and by limit'''
     return [p for p in sorted( points,key = lambda d: distance((point[0],point[1]),(d[0],d[1])))[:limit] if distance((point[0],point[1]),(p[0],p[1])) < radius]

def get_function_code(func_name):
     '''Takes function name
     Returns function code string'''
     import inspect
     print( inspect.getsource(func_name))

def multiprocessing_example():

     print('''
     from multiprocessing import Pool
     from test import f

     p = Pool(5)

     for i in p.imap(f, [1, 2, 3]):
     print(i)
     ''')

def upper_and_lower_stds(arr):
     '''Takes array
     Returns lower std,std and upper std'''
     mean = np.mean(arr)
     arr = np.array(arr)    

     ustd = np.sqrt(np.mean((arr[arr>mean]-mean)**2))
     lstd = np.sqrt(np.mean((arr[arr<mean]-mean)**2))
     return lstd,np.std(arr),ustd

def random_point_within(poly,n):
     '''from shapely.geometry import Polygon, Point
          yerevan = Polygon([(40.226411, 44.451349), (40.216974, 44.582842), (40.142085, 44.540785), (40.155469, 44.467657)])
          
     Takes polygon and n
     Returns n length array of random points within polygon'''
     from shapely.geometry import Polygon, Point
     min_x, min_y, max_x, max_y = poly.bounds

     points = []

     while len(points) < n:
          random_point = Point([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
          if (random_point.within(poly)):
               points.append(random_point)

     return points

def json_to_dict(filename):
     '''Takes json file name
     Returns dict object'''
     import json
     from collections import namedtuple
     with open(filename, 'r') as file:
          obj = json.loads(file.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
     return obj

def compare_datetimes(dt1,dt2):
     '''Takes two datetime objects
     Checks if they are equal by second precision'''
     return dt1.year == dt2.year and dt1.month == dt2.month and dt1.day == dt2.day and dt1.hour == dt2.hour and dt1.minute == dt2.minute and dt1.second == dt2.second

def show_percentages(names,values,maximums):
     from IPython.display import clear_output
     for name,value,maximum in zip(names,values,maximums):
          p = value/maximum*100
          p = 100 if p>100 else 0 if p<0 else p
          if value % int((maximum/500))== 0:
               clear_output()
               h = round(p+0.0001)>int(p)
               t = '{}   |{}{}|  {}%'.format(name,'█'*int(p),('▄' if h else '')+'_'*(100 - int(p) - (1 if h else 0) ),round(p,1))
               print(t,flush=True)

def send_email(text='45',FROM = 'tigodav@gmail.com',to = 'tigrandavtyan97@gmail.com'):
     import smtplib
     from getpass import getpass

     TO = recipient if isinstance(to, list) else [to]
     SUBJECT = 'Email from python'
     TEXT = str(text)

     # Prepare actual message
     message = """From: %s\nTo: %s\nSubject: %s\n\n%s
     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
     try:
          server = smtplib.SMTP("smtp.gmail.com", 587)
          server.ehlo()
          server.starttls()
          server.login(FROM, getpass())
          server.sendmail(FROM, TO, message)
          server.close()
          print ('successfully sent the mail')
     except:
          print('Failed to send the email')

def load_keras_model(filename):
     '''Takes filename (without json or h5 ending)'''
     from keras.models import model_from_json
     with open(filename+'.json', 'r') as json_file:
          loaded_model_json = json_file.read()
     model = model_from_json(loaded_model_json)
     model.load_weights(filename+".h5")
     print("Loaded model from disk")
     return model

def save_keras_model(model,filename):
     '''Takes keras model and filename(without json or h5 ending)'''
     model_json = model.to_json()
     with open(filename+".json", "w") as json_file:
          json_file.write(model_json)
     model.save_weights(filename+".h5")
     print("Saved model to disk")

class Dimension:
    def __init__(self,size,dimension):
        self.size = size
        self.dimension = dimension
        self._get_next = [0] * size
    def reset(self):
        self._get_next = [0] * self.size
        
    def next(self):
        self._get_next[self.size-1] += 1
        for i in range(self.size-1,0,-1):
            if self._get_next[i] == self.dimension:
                self._get_next[i] = 0
                self._get_next[i-1] += 1
        if self._get_next[0] >= self.dimension:
            return [self.dimension-1]*self.size
        return self._get_next
 