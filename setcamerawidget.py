# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:23:11 2016

@author: don
"""


from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SetCameraWidget(QWidget):
    def __init__(self, parent = None):
        super(SetCameraWidget, self).__init__(parent)
        layout = QGridLayout(self)
        self.m_okBtn = QPushButton("OK", self)
        self.m_cancelBtn = QPushButton("Cancel", self)
        self.m_x = QLineEdit(self)
        self.m_y = QLineEdit(self)
        self.m_z = QLineEdit(self)
        self.m_h = QLineEdit(self) 
        self.m_p = QLineEdit(self)
        self.m_r = QLineEdit(self)
                
        layout.addWidget(QLabel("X"), 0, 0)
        layout.addWidget(QLabel("Y"), 1, 0)
        layout.addWidget(QLabel("Z"), 2, 0)
        layout.addWidget(QLabel("Roll"), 3, 0)
        layout.addWidget(QLabel("Pitch"), 4, 0)
        layout.addWidget(QLabel("Yaw"), 5, 0)
        layout.addWidget(self.m_okBtn, 6, 1)
        layout.addWidget(self.m_cancelBtn, 6, 0)
        layout.addWidget(self.m_x, 0, 1)
        layout.addWidget(self.m_y, 1, 1)
        layout.addWidget(self.m_z, 2, 1)
        layout.addWidget(self.m_h, 3, 1)
        layout.addWidget(self.m_p, 4, 1)
        layout.addWidget(self.m_r, 5, 1)        
        
        
        self.setLayout(layout)
      
        self.m_cancelBtn.clicked.connect(self.cancelBtnClicked)

        
    def cancelBtnClicked(self):
        self.close()