# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 01:11:52 2016

@author: don
"""

from pobject import PObject
import ode

class PRay(PObject):
    def __init__(self, length):
        super(PRay, self).__init__(0, 0, 0, 0, 0, 0, 0)
        self.m_length = length
            
    def init(self):
        self.m_geom = ode.GeomRay(self.m_space_ID, self.m_length)
        
    def setPose(self, x, y, z, dx, dy, dz):
        self.m_geom.set((x, y, z), (dx, dy, dz))