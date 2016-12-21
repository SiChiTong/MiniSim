# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 18:06:18 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from glwidget import GLWidget
from robotwidget import RobotWidget


class MainWindow(QMainWindow):
    
    
    def __init__(self, parent = None):
        self.m_timer = QTimer(self)
        self.m_workspace = QWorkspace(self)
        self.m_glWidget = GLWidget(self)
        self.m_robotWidget = RobotWidget(self)
        
        self.m_showSimulator = QAction(u'', self)
        self.m_showConfig = QAction(u'', self)
        self.m_fullScreenAct = QAction(u'', self)

        self.m_fpsLabel = QLabel(self)
        self.m_cursorLabel = QLabel(self)
        self.m_selectingLabel = QLabel(self)
        
        self.m_vanishLabel = QLabel(self)
        self.m_noiseLabel = QLabel(self)
        
        self.m_current_dir = QString("123")
        
        self.m_scene = QGraphicsScene(0, 0, 800, 600)
        self.m_        
        self.m_lastSize = QSize(0,0)
        
    #slots
    def update(self):
        pass

    def updateRobotLabel(self):
        pass

    def showHideConfig(self, v):
        pass

    def showHideSimulator(self, v):
        pass

    def changeCurrentRobot(self):
        pass

    def changeGravity(self):
        pass
    
    def changeTimer(self):
        pass
    
    def restartSimulator(self):
        pass
    
    def toggleFullScreen(self, bool):
        pass
    
    def setCurrentRobotPosition(self):
        pass
    
    def customFPS(self, fps):
        pass
    
    def showAbout(self):
        pass
    
    #internal function
    def getInterval(self):
        import math
        return math.ceil(1000.0/ 60.0)