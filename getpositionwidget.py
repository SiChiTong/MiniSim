# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 15:17:57 2016

@author: don
"""



from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GetPositionWidget(QWidget):
    def __init__(self, parent = None):
        super(GetPositionWidget, self).__init__(parent)
        layout = QGridLayout(self)
        self.m_okBtn = QPushButton("OK", self)
        self.m_cancelBtn = QPushButton("Cancel", self)
        self.m_x = QLineEdit(self)
        self.m_y = QLineEdit(self)
        self.m_a = QLineEdit(self)
        
        layout.addWidget(QLabel("X"), 0, 0)
        layout.addWidget(QLabel("Y"), 1, 0)
        layout.addWidget(QLabel("Angle"), 2, 0)
        layout.addWidget(self.m_okBtn, 3, 1)
        layout.addWidget(self.m_cancelBtn, 3, 0)
        layout.addWidget(self.m_x, 0, 1)
        layout.addWidget(self.m_y, 1, 1)
        layout.addWidget(self.m_a, 2, 1)
        
        
        self.setLayout(layout)
        
        self.m_cancelBtn.clicked.connect(self.cancelBtnClicked)
        
    def cancelBtnClicked(self):
        self.close()
        
if __name__=='__main__':  
    import sys
    app = QApplication(sys.argv)  
    widget = GetPositionWidget()
    widget.show()  
    sys.exit(app.exec_())  