# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:54:04 2016

@author: don
"""



from pobject import PObject
import ode

class PCylinder(PObject):
    def __init__(self, x, y, z, R, radius, length, mass, r, g, b):
        super(PCylinder, self).__init__(x, y, z, R, r, g, b, mass)
        self.m_radius = radius
        self.m_length = length
    
    def setMass(self, mass):
        self.m_mass = mass
        m = ode.Mass()  
        m.setCylinderTotal(mass, 1, self.m_radius, self.m_length)
        self.m_body_ID.setMass(m)
        
    def init(self):
        self.m_body_ID = ode.Body(self.m_world_ID)
        self.initPosBody()          #Let ODE know the initial pos,rot of the PCylinder Object
        self.setMass(self.m_mass)
        self.m_geom = ode.GeomCylinder(None, self.m_radius, self.m_length)
        self.m_geom.setBody(self.m_body_ID)
        self.m_space_ID.add(self.m_geom)
        
    def draw(self):
        super(PCylinder, self).draw()
        self.m_cgraphics.drawCylinder(self.m_body_ID.getPosition(), self.m_body_ID.getRotation(), self.m_length, self.m_radius)    