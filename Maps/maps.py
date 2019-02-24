import cv2
import numpy as np


import pkg_resources
resource_package = __name__  # Could be any module/package name
class maps:
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

    def show_location(self,location,size=2,color=(255,0,0)):
        '''Takes (lat,lng)
            Draws on map'''
        board = self.Map.copy()
        point = self.ltop(location[::-1])
        cv2.circle(board,point,size,color,-1)
        cv2.imshow('Map',board)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def show_way(self,waypoints,size=2,color=(255,0,0),animation = False,delay = 40,zoom = True,spaces = 0):#TODO implement spaces
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