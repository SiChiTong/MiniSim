# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:43:14 2016

@author: don
"""


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import QGLWidget
from pworld import PWorld
from pray import PRay
from robot import Robot
from ode_graphics import CGraphics

#######################################################
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#######################################################

import ode

class GLWidget(QGLWidget):

    clicked = pyqtSignal()
    selectedRobot = pyqtSignal()
    closeSignal = pyqtSignal(bool)
    toggleFullScreen = pyqtSignal(bool)
    robotTurnedOnOff = pyqtSignal(int, bool)  
    
#######################################################
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)
#######################################################    
    
    
    def __init__(self, parent = None):
        super(GLWidget, self).__init__(parent)
        self.m_frames = 0
        self.m_state = 0
        self.m_first_time = True
        self.m_g = CGraphics(self)
        self.m_lastPos = QPoint()
        self.m_ctrl = False         
        self.m_alt = False
        
        self.m_xRot = 0
        self.m_yRot = 0
        self.m_zRot = 0
        
        #Timer
        self.m_time = QTime()
        self.m_rendertimer = QTime()
        self.m_fps = 0.0 
        
        
        #!!!!!!!!!!        
        #self.m_g.setViewpoint(0, -100, 3, 90, -45, 0)
        self.m_pworld = PWorld(0.05, 9.81, self.m_g, self)
        
        self.m_robot = Robot(self.m_pworld, 5, (0, 8, 0))       
        self.m_ray = PRay(50)        
        
        self.m_pworld.addObject(self.m_ray)

        self.m_pworld.initAllObjects()        
    
##################    

##############################   
        
        self.m_fullScreen = False
        self.m_currentRobot = 0
        self.m_currentPart = 0
        self.m_camMode = 0
        self.setMouseTracking(True)

        self.createContextMenu()


############################################
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 *16
        while angle > 360 * 16:
            angle -= 360 * 16 
        return angle
############################################
        
        
    def initializeGL(self):
        self.m_pworld.glinit()
        self.m_g.initScene(self.width(), self.height(), 0, 0.7, 1)


    def paintGL(self):

        self.m_g.enableGraphics()        
        
        self.m_g.initScene(self.width(), self.height(), 0, 0.7, 1)        
        self.m_pworld.draw()


    def step(self):
        self.m_rendertimer.restart()
        self.m_fps = self.m_frames / (self.m_time.elapsed()/ 1000.0)
        print 'fps:'
        print self.m_fps
        if (self.m_frames % int(60) == 0):
            self.m_time.restart()
            self.m_frames = 0
            
        if ( self.m_first_time == True ):
            self.m_g.initScene(self.width(), self.height(), 0, 0.7, 1)
            self.m_pworld.step()
            self.m_pworld.draw()
            self.m_first_time = False
        else:
            ddt = self.m_rendertimer.elapsed() / 1000.0
            if ddt > 0.05:
                ddt = 0.05
            self.m_g.initScene(self.width(), self.height(), 0, 0.7, 1)
            self.m_pworld.step(ddt)
            self.m_pworld.draw()
        self.m_frames = self.m_frames + 1
        print 'frames:'
        print self.m_frames
                
    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.customContextMenuRequested.connect(self.showContextMenu)  
  
        #Create a QMenu
        self.m_contextMenu = QMenu(self)
        self.m_robotsMenu = QMenu(u'&Robots')
        self.m_robotsMenu.addAction(u'Put all inside with formation 1')
        self.m_robotsMenu.addAction(u'Put all inside with formation 2')
        self.m_robotsMenu.addAction(u'Turn all off')
        self.m_robotsMenu.addAction(u'Turn all on')
        self.m_moveRobotAct = QAction(u'&Locate robot', self)
        self.m_selectRobotAct = QAction(u'&Select robot', self)
        self.m_resetRobotAct = QAction(u'R&eset robot', self)
        self.m_onOffRobotAct = QAction(u'Turn &off', self)
        self.m_lockToRobotAct = QAction(u'&Lock camera to this robot', self)

        #Add in the context Menu
        self.m_contextMenu.addMenu(self.m_robotsMenu)
        self.m_contextMenu.addAction(self.m_moveRobotAct)
        self.m_contextMenu.addAction(self.m_selectRobotAct)
        self.m_contextMenu.addAction(self.m_resetRobotAct)
        self.m_contextMenu.addAction(self.m_onOffRobotAct)
        self.m_contextMenu.addAction(self.m_lockToRobotAct)        
                
        # Associated the callbacks to different actions
        self.m_moveRobotAct.triggered.connect(self.moveRobot)  
        self.m_selectRobotAct.triggered.connect(self.selectRobot)
        self.m_resetRobotAct.triggered.connect(self.resetRobot)
        self.m_onOffRobotAct.triggered.connect(self.switchRobotOnOff)
        self.m_lockToRobotAct.triggered.connect(self.lockCameraToRobot)

    def showContextMenu(self, pos):  
        '''Showing up the right click menu'''
        self.m_contextMenu.move(self.pos() + pos)  
        self.m_contextMenu.show()  


    def moveRobot(self):
        pass
    
    def selectRobot(self):
        pass
    
    def resetRobot(self):
        pass
    
    def switchRobotOnOff(self):
        pass
    
    def lockCameraToRobot(self):
        pass
    
    
        
        
    def getFPS(self):
        pass
    
    def update3DCursor(self, mouse_x, mouse_y):
        pass
    
    def reset(self, robot_id):
        pass
    
    def step(self):
        pass

    def changeCameraMode(self):
        pass
    
    def RobotMenuTriggered(self, act):
        pass
    
    def mousePressEvent(self, event):
        if (self.m_g.isGraphicsEnabled() == False): return
        self.m_lastPos = event.pos()
        if (event.buttons() == Qt.LeftButton):
            if self.m_state == 1:
                pass
                #moving the robot and hide the 3D Cursor
        elif self.m_state == 2:
            pass
            #move the ball and hide the 3D Cursor
        else:
            pass
            #select specific robot
        if (event.buttons() == Qt.RightButton):
            pass
            #show the selected robot color
            #if it is on, show "Turn off" menu action
            #if it is off, show "Turn on" menu action
        
    def wheelEvent(self, event):
        if (self.m_g.isGraphicsEnabled() == False): return
        self.m_g.zoomCamera(-event.delta() * 0.02 )
        #update the 3D Cursor in the new relative position
        self.updateGL()        
        
    def mouseMoveEvent(self, event):
        if (self.m_g.isGraphicsEnabled() == False): return
        dx = -(event.x() - self.m_lastPos.x())
        dy = -(event.y() - self.m_lastPos.y())
        #print dx, dy
        
        if (event.buttons() == Qt.LeftButton):
            if (self.m_ctrl == True):
                self.m_g.cameraMotion(4, dx, dy)
                self.updateGL()
            else:
                self.m_g.cameraMotion(5, dx, dy)
                #self.m_g.cameraMotion(1, dx, dy) 
        
        self.m_lastPos = event.pos()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Control):
            self.m_ctrl = not self.m_ctrl
        if (event.key() == Qt.Key_Alt):
            self.m_alt = True
        if (event.key() == Qt.Key_0):
            xyz, hpr = self.m_g.getViewpoint()
            print xyz, hpr
        if (event.key() == Qt.Key_F1):
            self.m_g.lookAt(0, 0, 0)
            self.updateGL()
            
if __name__=='__main__':  
    import sys
    app = QApplication(sys.argv)  
    widget = GLWidget()
    widget.show()  
    sys.exit(app.exec_())  