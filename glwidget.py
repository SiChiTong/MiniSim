# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:43:14 2016

@author: don
"""




####Need a GLQGraphicView to handle the user signals slope

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import QGLWidget
from pworld import PWorld
from pray import PRay
from pcylinder import PCylinder
from robot import Robot
from ode_graphics import CGraphics
from setcamerawidget import SetCameraWidget

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
        self.m_setCameraWidget = SetCameraWidget()
        self.m_lastPos = QPoint()
        self.m_ctrl = False         
        self.m_alt = False
        
        #aa
        self.m_xRot = 0
        self.m_yRot = 0
        self.m_zRot = 0
        
        #Timer
        self.m_time = QTime()
        self.m_rendertimer = QTime()
        self.m_fps = 0.0 
        
        
        self.m_pworld = PWorld(0.05, 0, self.m_g, self)
        
        
        self.m_robot = Robot(self.m_pworld, 5, (0, 0, 0))       
        self.m_ray = PRay(50)        
        
        self.m_pworld.addObject(self.m_ray)

        self.m_pworld.initAllObjects()        
    
##############################    

##############################   
        
        self.m_fullScreen = False
        self.m_currentRobot = 0
        self.m_currentPart = 0
        self.m_camMode = 0
        self.setMouseTracking(True)

        self.createContextMenu()
        self.m_setCameraWidget.m_okBtn.clicked.connect(self.setCamera)

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

        self.m_g.setViewpoint(self.m_g.m_view_xyz, (self.m_xRot/16.0, self.m_yRot/16.0, self.m_zRot/16.0))        
        
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
        self.m_setCameraAct = QAction(u'&Set Camera',self)

        #Add in the context Menu
        self.m_contextMenu.addMenu(self.m_robotsMenu)
        self.m_contextMenu.addAction(self.m_moveRobotAct)
        self.m_contextMenu.addAction(self.m_selectRobotAct)
        self.m_contextMenu.addAction(self.m_resetRobotAct)
        self.m_contextMenu.addAction(self.m_onOffRobotAct)
        self.m_contextMenu.addAction(self.m_lockToRobotAct)
        self.m_contextMenu.addAction(self.m_setCameraAct)
                
        # Associated the callbacks to different actions
        self.m_moveRobotAct.triggered.connect(self.moveRobot)  
        self.m_selectRobotAct.triggered.connect(self.selectRobot)
        self.m_resetRobotAct.triggered.connect(self.resetRobot)
        self.m_onOffRobotAct.triggered.connect(self.switchRobotOnOff)
        self.m_lockToRobotAct.triggered.connect(self.lockCameraToRobot)
        self.m_setCameraAct.triggered.connect(self.setCameraClicked)


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
        if (event.key() == Qt.Key_Up):
            self.m_g.cameraMotion(1, 0, 0.05)
            self.updateGL()
        if (event.key() == Qt.Key_Down):
            self.m_g.cameraMotion(1, 0, -0.05)
            self.updateGL()
        if (event.key() == Qt.Key_Left):
            self.m_g.cameraMotion(2, -0.05, 0)
            self.updateGL()
        if (event.key() == Qt.Key_Right):
            self.m_g.cameraMotion(2, 0.05, 0)
            self.updateGL()

            
    def setCameraClicked(self):
        self.m_setCameraWidget.show()       
        
    def setCamera(self):
        self.m_g.setViewpoint_2(
                           self.m_setCameraWidget.m_x.text().toFloat()[0], 
                           self.m_setCameraWidget.m_y.text().toFloat()[0],
                           self.m_setCameraWidget.m_z.text().toFloat()[0],
                           self.m_setCameraWidget.m_h.text().toFloat()[0],
                           self.m_setCameraWidget.m_p.text().toFloat()[0],
                           self.m_setCameraWidget.m_r.text().toFloat()[0])
        self.updateGL()


    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.m_xRot:
            self.m_xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.m_yRot:
            self.m_yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.m_zRot:
            self.m_zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()


            
class GLDockWidget(QDockWidget):
    def __init__(self, parent = None):
        super(GLDockWidget, self).__init__(parent)
        self.m_glWidget = GLWidget(self)

        self.m_xSlider = self.createSlider()
        self.m_ySlider = self.createSlider()
        self.m_zSlider = self.createSlider()

        self.m_xSlider.valueChanged.connect(self.m_glWidget.setXRotation)
        self.m_glWidget.xRotationChanged.connect(self.m_xSlider.setValue)
        self.m_ySlider.valueChanged.connect(self.m_glWidget.setYRotation)
        self.m_glWidget.yRotationChanged.connect(self.m_ySlider.setValue)
        self.m_zSlider.valueChanged.connect(self.m_glWidget.setZRotation)
        self.m_glWidget.zRotationChanged.connect(self.m_zSlider.setValue)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.m_glWidget)
        mainLayout.addWidget(self.m_xSlider)
        mainLayout.addWidget(self.m_ySlider)
        mainLayout.addWidget(self.m_zSlider)

        tmpWidget = QWidget(self)
        tmpWidget.setLayout(mainLayout)
        tmpWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        self.setWidget = tmpWidget


        self.m_xSlider.setValue(15 * 16)
        self.m_ySlider.setValue(345 * 16)
        self.m_zSlider.setValue(0 * 16)

        self.setWindowTitle("Hello GL")

    def createSlider(self):
        slider = QSlider(Qt.Vertical, self)

        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        return slider    
    
if __name__=='__main__':  
    import sys
    app = QApplication(sys.argv)  
    widget = GLWidget()
    widget.show()  
    sys.exit(app.exec_())  