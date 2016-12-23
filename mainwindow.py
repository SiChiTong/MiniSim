# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 18:06:18 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from glwidget import WrappedGLWidget
from robotwidget import RobotDockWidget
from qtimelineeditor import QTimelineEditorDockWidget


class MainWindow(QMainWindow):
    
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)        
        
        self.m_timer = QTimer(self)
        self.m_timer.setInterval(self.getInterval())
        self.m_workspace = QWorkspace(self)
        self.setCentralWidget(self.m_workspace)
        
        self.m_glDockWidget = WrappedGLWidget(self)
        self.m_glDockWidget.setWindowTitle("Simulator")
        self.m_glDockWidget.m_glWidget.resize(512, 512)
        
        self.m_robotDockWidget = RobotDockWidget(self)
        self.m_timelineEditorDockWidget = QTimelineEditorDockWidget(self)
        

        #Status Bar
        self.m_fpsLabel = QLabel(self)
        self.m_cursorLabel = QLabel(self)
        self.m_selectingLabel = QLabel(self)
        self.m_vanishLabel = QLabel("Vanishing", self)
        self.m_noiseLabel = QLabel("Gaussian noise", self)
        
        self.m_fpsLabel.setFrameStyle(QFrame.Panel)
        self.m_cursorLabel.setFrameStyle(QFrame.Panel)
        self.m_selectingLabel.setFrameStyle(QFrame.Panel)
        self.m_vanishLabel.setFrameStyle(QFrame.Panel)
        self.m_noiseLabel.setFrameStyle(QFrame.Panel)
                
        self.statusBar().addWidget(self.m_fpsLabel)
        self.statusBar().addWidget(self.m_cursorLabel)
        self.statusBar().addWidget(self.m_selectingLabel)
        self.statusBar().addWidget(self.m_vanishLabel)
        self.statusBar().addWidget(self.m_noiseLabel)
        
        #Menus
        self.m_fileMenu = QMenu("File")
        self.menuBar().addMenu(self.m_fileMenu)
        self.m_takeSnapshotAct = QAction("Save SnapShot", self.m_fileMenu)
        self.m_takeSnapshotAct.setShortcut(QKeySequence("F3"))
        self.m_takeSnapshotToClipboardAct = QAction("Copy snapshot to clipboard", self.m_fileMenu)
        self.m_takeSnapshotToClipboardAct.setShortcut(QKeySequence("F4"))
        self.m_exit = QAction("Exit", self.m_fileMenu)
        self.m_exit.setShortcut(QKeySequence("Ctrl+X"))
        self.m_fileMenu.addAction(self.m_takeSnapshotAct)
        self.m_fileMenu.addAction(self.m_takeSnapshotToClipboardAct)
        self.m_fileMenu.addAction(self.m_exit)
        
        self.m_viewMenu = QMenu("View")
        self.menuBar().addMenu(self.m_viewMenu)
        self.m_showSimulatorAct = QAction("Simulator", self.m_viewMenu)
        self.m_showSimulatorAct.setCheckable(True)
        self.m_showSimulatorAct.setChecked(True)
        self.m_showConfigAct = QAction("Configuration", self.m_viewMenu)
        self.m_showConfigAct.setCheckable(True)
        self.m_showConfigAct.setChecked(True)
        self.m_viewMenu.addAction(self.m_showConfigAct)
        self.m_viewMenu.addAction(self.m_showSimulatorAct)
        
        self.m_simulatorMenu = QMenu("Simulator")
        self.menuBar().addMenu(self.m_simulatorMenu)
        self.m_robotMenu = QMenu("Robot")
        self.m_simulatorMenu.addMenu(self.m_robotMenu)

        
        self.m_helpMenu = QMenu("Help")
        self.menuBar().addMenu(self.m_helpMenu)
        self.m_aboutAct = QAction("About", self.m_helpMenu)
        self.m_helpMenu.addAction(self.m_aboutAct)
        
        self.m_robotMenu.addMenu(self.m_glDockWidget.m_glWidget.m_contextMenu)
        
        self.m_fullScreenAct = QAction("Full screen", self.m_simulatorMenu)
        self.m_fullScreenAct.setShortcut(QKeySequence("F2"))
        self.m_fullScreenAct.setCheckable(True)
        self.m_fullScreenAct.setChecked(False)
        self.m_simulatorMenu.addAction(self.m_fullScreenAct)
                
        #self.m_viewMenu.addMenu(self.m_glWidget.m_cameraMenu)
                
        self.addDockWidget(Qt.LeftDockWidgetArea, self.m_timelineEditorDockWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.m_robotDockWidget)
        self.m_workspace.addWindow(self.m_glDockWidget, Qt.CustomizeWindowHint 
                                                        | Qt.WindowTitleHint
                                                        | Qt.WindowSystemMenuHint 
                                                        | Qt.WindowMinimizeButtonHint
                                                        | Qt.WindowMaximizeButtonHint)
        self.m_glDockWidget.setWindowState(Qt.WindowMaximized)
        
        
        self.m_current_dir = QString("123")
        
        self.m_scene = QGraphicsScene(0, 0, 800, 600)
             
        self.m_lastSize = QSize(0,0)
        
        #self.resize(1500, 800)
        
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
        k = math.ceil(1000.0 / fps)
        self.m_timer.setInterval(k)
        #logStatus(QString("new FPS set by user: %1"))
    
    def showAbout(self):
        pass
    
    #internal function
    def getInterval(self):
        import math
        return math.ceil(1000.0/ 60.0)
        

if __name__=='__main__':  
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()  
    sys.exit(app.exec_())  