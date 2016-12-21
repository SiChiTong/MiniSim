# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 20:29:57 2016

@author: don
"""

#from pobject import PObject
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import QGLWidget
from ode_graphics import CGraphics
 
import ode

class PWorld(QObject):
    def __init__(self, dt, gravity, g, parent = None):
        super(PWorld, self).__init__(parent)
        #self.m_contactGroup = JointGroup()
        self.m_objects = []
        #self.m_surfaces = []
        self.m_delta_time = dt
        #self.m_sur_matrix = []
        self.m_objects_count = 0
        self.m_world = ode.World() 
        self.m_space = ode.HashSpace()
        self.m_world.setGravity((0, 0, -gravity))
        #self.sur_matrix = ()
        self.delta_time = dt
        self.m_cgraphics = g
        
        # create a plane geom to simulate a floor
        floor = ode.GeomPlane(self.m_space, (0, 1, 0), 0)
        
    def setGravity(self, gravity):
        self.m_world.setGravity(0, 0, -gravity)
    
    def addObject(self, o):
        o.m_ID = len(self.m_objects)
        if (o.m_world_ID == None): o.m_world_ID = self.m_world
        if (o.m_space_ID == None): o.m_space_ID = self.m_space
        
        #!!!!!!!!!!!!!        
        o.m_cgraphics = self.m_cgraphics
        o.init()        #additional for specific object initialization
        self.m_objects.append(o)
    
    def initAllObjects(self):
        self.m_objects_count =  len(self.m_objects)
        #surface

    #@ param o1 o2 the PObjects created in the World (Vector)    
    #def createSurface(o1, o2):
    #   pass
    
    #def findSurface(o1, o2):
    #   pass
    
    def step(self, dt = -1):
        #spaceCollide
        if dt >= 0:
            self.m_delta_time = dt
        self.m_world.step(self.m_delta_time)
        #self.contactgroup.empty()
        
    def glinit(self):
        for i in range(len(self.m_objects)):
            self.m_objects[i].glinit()
    
    def draw(self):
        for i in range(len(self.m_objects)):
            if self.m_objects[i].getVisibility():            
                self.m_objects[i].draw()
    
    #Handler for dynamic collisions
    #def handleCollisions(o1, o2):
    #    pass
    
    