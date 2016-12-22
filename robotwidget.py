# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 13:53:38 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from getpositionwidget import GetPositionWidget
from dragdroprobotsubwidget import DragDropRobotWidget

class RobotDockWidget(QDockWidget):   
    
    def __init__(self, parent = None):
        super(RobotDockWidget, self).__init__("Current Robot", parent)
        layout = QGridLayout()
        
        self.m_robotCombo = QComboBox(self)
        self.m_teamCombo = QComboBox(self)        

        self.m_teamCombo.addItem("Blue", self)
        self.m_teamCombo.addItem("Yellow", self)        
        
        for i in range(7):
            item = QString("%d"%i)
            self.m_robotCombo.addItem(item)
        
        self.m_robotPic = DragDropRobotWidget(self)        
        
        #self.m_robotPic = QLabel(self)
        #self.m_jointLabel = QLabel("Joint", self)

        self.m_velLabel = QLabel(self)
        self.m_accLabel = QLabel(self)        
        
        self.m_resetBtn = QPushButton("Reset", self)
        self.m_locateBtn = QPushButton("Locate", self)
        self.m_onOffBtn = QPushButton("Turn Off", self)
        self.m_setPoseBtn = QPushButton("Set Position", self)
        
        
        
        layout.addWidget(self.m_robotPic, 0, 0, 5, 1)
        layout.addWidget(QLabel("Team"), 0, 1)
        layout.addWidget(self.m_teamCombo, 0, 2)
        layout.addWidget(QLabel("Index"), 1, 1)
        layout.addWidget(self.m_robotCombo, 1, 2)
        layout.addWidget(QLabel("Velocity"), 2, 1)
        layout.addWidget(self.m_velLabel, 2, 2)
        layout.addWidget(self.m_resetBtn, 3, 1)
        layout.addWidget(self.m_locateBtn, 3, 2)
        layout.addWidget(self.m_onOffBtn, 4, 1)
        layout.addWidget(self.m_setPoseBtn, 4, 2)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWidget(widget)  #Real Widget for 'Supporting'
        
        self.m_setPoseBtn.clicked.connect(self.setPoseBtnClicked)        
        

        
        self.m_getPoseWidget = GetPositionWidget()
        self.m_id = 0
        
        
    #def setPicture(self, img):
        #self.m_robotPic.setPixmap(QPixmap.fromImage(img).scaled(300, 300, Qt.IgnoreAspectRatio, Qt.FastTransformation))

    def changeRobotOnOff(self, _id, a):
        pass

    def setPoseBtnClicked(self):
        self.m_getPoseWidget.show()
        

        
if __name__=='__main__':  
    import sys
    app = QApplication(sys.argv)  
    widget = RobotDockWidget()
    #widget.setPicture(QImage('./head.png'))
    widget.show()  
    sys.exit(app.exec_())  