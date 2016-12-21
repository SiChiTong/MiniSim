# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:54:04 2016

@author: don
"""



from pobject import PObject
import ode

class PBox(PObject):
    def __init__(self, x, y, z, w, h, l, mass, r, g, b):
        super(PBox, self).__init__(x, y, z, r, g, b, mass) #?
        self.m_w = 0.0
        self.m_h = 0.0
        self.m_l = 0.0
    
    def setMass(self, mass):
        self.m_mass = mass
        m = ode.Mass()  
        m.setBoxTotal(mass, self.m_w, self.m_h, self.m_l)
        self.m_body_ID.setMass(m)
        
    def init(self):
        self.m_body_ID = ode.Body(self.m_world_ID)
        self.initPosBody()
        self.setMass(self.m_mass)
        self.m_geom = ode.GeomBox(None, (self.m_w, self.m_h, self.m_l))
        self.m_geom.setBody(self.m_body_ID)
        self.m_space_ID.add(self.m_geom)
        
    def draw(self):
        super(PBox, self).draw()
        self.m_cgraphics.drawBox(self.m_geom.getPosition, self.m_geom.getRotation, (self.m_w, self.m_h, self.m_l))
          