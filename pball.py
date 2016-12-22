# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 19:57:51 2016

@author: don
"""

from pobject import PObject
import ode

class PBall(PObject):
    def __init__(self, x, y, z, radius, mass, r, g, b):
        super(PBall, self).__init__(x, y, z, (1, 0, 0, 0, 1, 0, 0, 0, 1), r, g, b, mass) #?
        self.m_radius = radius
    
    def setMass(self, mass):
        self.m_mass = mass
        m = ode.Mass()  
        m.setSphereTotal(mass, self.m_radius)
        self.m_body_ID.setMass(m)
        
    def init(self):
        self.m_body_ID = ode.Body(self.m_world_ID)
        self.initPosBody()
        self.setMass(self.m_mass)
        self.m_geom = ode.GeomSphere(None, self.m_radius)
        self.m_geom.setBody(self.m_body_ID)
        self.m_space_ID.add(self.m_geom)
        
    def draw(self):
        super(PBall, self).draw()
        self.m_cgraphics.drawCylinder(self.m_geom.getPosition, self.m_geom.getRotation, self.m_radius)    