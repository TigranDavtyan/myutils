import cv2
import numpy as np
class map:
    """List of available maps [Yerevan,Dilijan]"""
    def __init__(self,mapName='Yerevan',scale = 12000):
        self.mapName = mapName
        if mapName == 'Yerevan':
            pass
        elif mapName = 'Dilijan':
            self.boundaries={'north':40.756399,'south':40.738668,'west':44.829089 ,'east':44.905993}
            self.Map = cv2.imread('DilijanMap.jpg')[150:735,435:2970]#[104:759,424:2831]
            self.scale = scale
            self.map_shape = tuple((int((Map.shape[1]*(scale/12000))),int((Map.shape[0]*(scale/12000)))))
            self.Map = cv2.resize(Map,self.map_shape)

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
    
    def show_way(self,waypoints,size=2,color=(255,0,0),animation = False):
        '''Takes (lat,lng) waypoints
            Draws on map'''
        board = self.Map.copy()
        if animation:
            for waypoint in waypoints:
                point = self.ltop(waypoint[::-1])
                cv2.circle(board,point,size,color,-1)
                cv2.imshow('Map',board)
                cv2.waitKey(40)
            cv2.waitKey(0)
        else:
            for waypoint in waypoints:
                point = self.ltop(waypoint[::-1])
                cv2.circle(board,point,size,color,-1)
            cv2.imshow('Map',board)
            cv2.waitKey(0)
        cv2.destroyAllWindows()