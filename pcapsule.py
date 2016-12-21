# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 08:33:12 2016

@author: don
"""



from pobject import PObject
import ode

class PCapsule(PObject):
    def __init__(self, x, y, z, radius, length, mass, r, g, b):
        super(PCapsule, self).__init__(x, y, z, r, g, b, mass) #?
        self.m_radius = radius
        self.m_length = length
    
    def setMass(self, mass):
        self.m_mass = mass
        m = ode.Mass()  
        m.setCapsuleTotal(mass, 1, self.m_radius, self.m_length)
        self.m_body_ID.setMass(m)
        
    def init(self):
        self.m_body_ID = ode.Body(self.m_world_ID)
        self.initPosBody()
        self.setMass(self.m_mass)
        self.m_geom = ode.GeomCapsule(None, self.m_radius, self.m_length)
        self.m_geom.setBody(self.m_body_ID)
        self.m_space_ID.add(self.m_geom)
        
    def draw(self):
        super(PCapsule, self).draw()
        self.m_cgraphics.drawCapsule(self.m_geom.getPosition, self.m_geom.getRotation, self.m_length, self.m_radius)    
