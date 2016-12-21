# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 18:12:29 2016

@author: don
"""
from pobject import PObject
import ode

class PGround(PObject):
    def __init__(self):
        super(PGround, self).__init__(0, 0, 0, 0, 1, 0, 0) #?
        
    def init(self):
        self.m_geom = ode.GeomPlane(self.m_space_ID, 0, 0, 1, 0)
        
    def draw(self):
        super(PGround, self).draw()