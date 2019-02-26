import cv2
import numpy as np
import requests


import pkg_resources
resource_package = __name__
class MAPS:
    """List of available maps [Yerevan,Dilijan]"""
    def __init__(self,mapName='Yerevan',scale = 12000):
        self.mapName = mapName
        if mapName == 'Yerevan':
            resource_path = '/'.join(('YerevanMap.bmp',)) 
            Map = pkg_resources.resource_stream(resource_package, resource_path)
            pass
        elif mapName == 'Dilijan':
            resource_path = '/'.join(('DilijanMap.jpg',)) 
            Map = pkg_resources.resource_stream(resource_package, resource_path)
            self.boundaries={'north':40.756399,'south':40.738668,'west':44.829089 ,'east':44.905993}
            self.Map = cv2.imread(Map.name)[150:735,435:2970]#[104:759,424:2831]
            self.scale = scale
            self.map_shape = tuple((int((self.Map.shape[1]*(scale/12000))),int((self.Map.shape[0]*(scale/12000)))))
            self.Map = cv2.resize(self.Map,self.map_shape)
        else:
            raise Exception('We dont supprt this map: {}'.format(mapName))

    def ltop(self,point):
        x = int((point[0]-self.boundaries['west'])/(self.boundaries['east']-self.boundaries['west'])*self.map_shape[0])
        y = int(abs(point[1]-self.boundaries['north'])/(self.boundaries['north']-self.boundaries['south'])*self.map_shape[1])
        return (x,y)

    def ptol(point):#takes x,y returns lon,lat
        return [point[0]/self.scale+self.boundaries['west'],(self.map_shape[1]-point[1])/scale+self.boundaries['south']]

    def check_boundaries(self,loc):
        if loc[0]<self.boundaries['south'] or loc[0]>self.boundaries['north'] or loc[1]<self.boundaries['west'] or loc[1]>self.boundaries['east']:
            return False
        return True

    def show_location(self,location,size=2,color=(255,0,0)):
        '''Takes (lat,lng)
            Draws on map'''
        board = self.Map.copy()
        point = self.ltop(location[::-1])
        cv2.circle(board,point,size,color,-1)
        cv2.imshow('Map',board)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def show_trip(self,waypoints,size=2,color=(255,0,0),animation = False,delay = 40,zoom = True,spaces = 0):#TODO implement spaces
        '''Takes (lat,lng,...) waypoints
            Draws on map'''
        minx,maxx,miny,maxy = 0,self.map_shape[0],0,self.map_shape[1]

        points = [self.ltop((waypoint[1],waypoint[0])) for waypoint in waypoints]
        if zoom:
            margin = 50
            x_ = [p[0] for p in points]
            y_ = [p[1] for p in points]
            minx,maxx = min(x_)-margin,max(x_)+margin
            miny,maxy = min(y_)-margin,max(y_)+margin
            minx = minx if minx>0 else 0
            maxx = maxx if maxx<self.map_shape[0] else self.map_shape[0]
            miny = miny if miny>0 else 0
            maxy = maxy if maxy<self.map_shape[1] else self.map_shape[1]
        exit = False
        while True:
            board = self.Map.copy()
            if exit :break
            prev_point = 0
            for i,point in enumerate(points):
                cv2.circle(board,point,size,color,-1)
                if prev_point!=0:
                    cv2.line(board,prev_point,point,color,int(size*0.7))
                prev_point = point
                if animation:
                    cv2.imshow('Map',board[miny:maxy,minx:maxx])
                    key = cv2.waitKey(delay)
                    if key == 27:
                        exit = True
                        break
                    elif key == 32:
                        animation = not animation
                        break
            cv2.imshow('Map',board[miny:maxy,minx:maxx])
            key = cv2.waitKey(40)
            if key == 27:
                break
            elif key == 32:
                animation = not animation
        cv2.destroyAllWindows()

    def get_trip_distance(self,trip,verbose = False):
        '''Takes (lat,lng) array 
            Returns trip distance by meters'''
        dist = 0
        for i in range(1,len(trip)-1):
            if verbose:
                print('From ',trip[i-1][::-1],' to ',trip[i][::-1],' distance is ',distance(trip[i-1],trip[i]),'m')
            dist += distance(trip[i-1],trip[i])
        return dist

import osmium
class NodeLocationsHandler(osmium.SimpleHandler):
    def __init__(self,node_locations_all):
        self.node_locations_all = node_locations_all
        osmium.SimpleHandler.__init__(self)

    def node(self, n):
        self.node_locations_all[n.id] = [n.location.lat,n.location.lon]

class OSRM:
    def __init__(self,host='http://127.0.0.1:5000/',get_node_locations = False):
        print('Connecting to osrm backend api . . . ',end = '')
        self.host = host
        try:
            if self.route((40.12,44.56),(40.18,44.50))['code'] != 'Ok':
                print('Thers is no osrm backend api running on the host')
                raise requests.ConnectionError
        except requests.ConnectionError:
            print('Thers is no osrm backend api running on the host')
            raise requests.ConnectionError
        print('success!\n')
        if get_node_locations:
            resource_path = '/'.join(('armenian_latest','armenia-latest.osm.pbf')) 
            Map = pkg_resources.resource_stream(resource_package, resource_path)
            
            print('Collecting all nodes` locations . . . ',end='')
            self.node_locations_all = {}
            self.h = NodeLocationsHandler(self.node_locations_all)
            self.h.apply_file(Map.name)
            print('collected {}\n'.format(len(self.node_locations_all)))

    def route(self,origin,destination):
        '''Takes two (lat,lng) locations
        Returns route detailes'''
        url = self.host + 'route/v1/driving/'

        origin = list(origin[::-1])
        destination = list(destination[::-1])

        url += str(origin) + ';' + str(destination)
        url = url.replace(' ','').replace('[','').replace(']','')
        detailes = requests.get(url)

        return detailes.json()

    def match(self,trip,use_timestamps=False,use_custom_timestamps=True,delays=1,use_bearings=False,radius = 50,bearing_error = 70):
        '''Takes (lat,lng,[timestamp],[bearing])'''
        points = ''
        datetimes = ''
        bearings = ''
        start = 0
        data = {
            'radius':radius
        }
        bearing_index = 3 if use_timestamps else 2
        for item in trip:
            item = list(item)
            points += str(item[1])+','+str(item[0])+';'
            if use_timestamps:
                datetimes += str(item[2])+';'
            elif use_custom_timestamps:
                datetimes += str(start)+';'
                start+=delays
            if use_bearings:
                bearings += str((int(item[bearing_index])+360)%360)+',{}'.format(bearing_error)+';'
        points = points[:len(points)-1]
        url = self.host + 'match/v1/driving/'+points+'?overview=simplified&geometries=geojson&tidy=true'
        if use_custom_timestamps or use_timestamps:
            datetimes = datetimes[:len(datetimes)-1]
            url+='&timestamps='+datetimes
        if use_bearings:
            bearings = bearings[:len(bearings)-1]
            url+='&bearings='+bearings
        
        res = requests.get(url,json=data)   

        return res.json()

        node_locations_all = {}

    def nearby(self,location):
        '''Takes (lat,lng)
        Returns ((lat,lng),(node_from,node_to),res.json())'''
        res = requests.get(self.host + 'nearest/v1/driving/{},{}?number=1'.format(location[1],location[0]))
        snap = res.json()['waypoints'][0]['location'][::-1]
        nodes = res.json()['waypoints'][0]['nodes']
        return snap,tuple(nodes),res.json()

    def advanced_nearby(self,locations):
        '''Takes >=8 length locations array
        Returns  -4th locations snapped location and nodes
        Some error when returns [0,0],[0,0]'''
        if len(locations)<8:
            return [0,0],[0,0]
        res = self.match(locations[-8:],)
        if res['code'] != 'Ok':
            return [0,0],[0,0]
        try:
            nodes = res['matchings'][0]['legs'][-4]['annotation']['nodes']
            snapped_location = res['tracepoints'][-4]['location'][::-1]
        except:
            return [0,0],[0,0]
        if len(nodes)>2:
            s,nodes1,_ = self.nearby(snapped_location)
            node1,node2 = nodes1
            if node1==0 or node2 == 0:
                return snapped_location,[0,0]
            else:
                try:
                    nodes = [node1,node2] if nodes.index(node1)<nodes.index(node2) else [node2,node1]
                except:
                    return snapped_location,[0,0]
        return snapped_location,tuple(nodes)

    def get_node_location(self,nodeid):
        return self.node_locations_all[nodeid]
    