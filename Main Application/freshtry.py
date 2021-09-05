

import sys
import numpy as np
import cv2 as cv
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from Director import Director
from freshgui import Ui_MainWindow

class ballgui(qtw.QMainWindow):
    xpos_counter = 0
    ypos_counter = 0

    def __init__(self, director, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_pg)
        self.director = director
        
        # Main Menu btns to navigate to another page
        self.ui.btn_main_position.clicked.connect(self.showPosition_pg)
        self.ui.btn_main_pattern.clicked.connect(self.showPattern_pg)
        self.ui.btn_main_joystick.clicked.connect(self.showJoystick_pg)

        # Menu buttons on each page, to return to Main Menu
        self.ui.btn_pos_menu.clicked.connect(self.showMain_pg)
        self.ui.btn_patt_menu.clicked.connect(self.showMain_pg)
        self.ui.btn_joystick_menu.clicked.connect(self.showMain_pg)

        # Position page btn event set up
        self.ui.btn_pos_center.clicked.connect(self.setup_posCenter)
        self.ui.btn_pos_position.clicked.connect(self.setup_posPoint)
        self.ui.btn_pos_reset.clicked.connect(self.setup_posReset)
        self.ui.btn_pos_xplus.clicked.connect(self.Xplus)
        self.ui.btn_pos_xminus.clicked.connect(self.Xminus)
        self.ui.btn_pos_yplus.clicked.connect(self.Yplus)
        self.ui.btn_pos_yminus.clicked.connect(self.Yminus)

        # Patterns page btn event set up
        self.ui.btn_patt_rectangle.clicked.connect(self.setup_pattRectangle)
        self.ui.btn_patt_circle.clicked.connect(self.setup_pattCircle)
        self.ui.btn_patt_infinity.clicked.connect(self.setup_pattInfinity)
        self.ui.btn_patt_center.clicked.connect(self.setup_pattCenter)
        self.ui.btn_patt_reset.clicked.connect(self.setup_pattReset)

        # Joystick page btn event set up

    

    def showMain_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_pg)  
        
    def showPosition_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.position_pg)
        self.ui.btn_pos_center.setStyleSheet(neutralbtn)
        self.ui.btn_pos_position.setStyleSheet(neutralbtn)
        self.ui.lbl_pos_showxpos.setText(str(self.xpos_counter))
        self.ui.lbl_pos_showypos.setText(str(self.ypos_counter))
        
    def showPattern_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pattern_pg)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)

    def showJoystick_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.joystick_pg)
        self.ui.btn_stick_position.setStyleSheet(neutralbtn)
        self.ui.btn_stick_angle.setStyleSheet(neutralbtn)

    def setup_posCenter(self):
        self.ui.btn_pos_center.setStyleSheet(clickedbtn)
        self.ui.btn_pos_position.setStyleSheet(neutralbtn)
        self.ui.btn_pos_menu.setEnabled(False)
        self.ui.btn_pos_menu.setStyleSheet(disablebtn)

    def setup_posPoint(self):
        self.ui.btn_pos_position.setStyleSheet(clickedbtn)
        self.ui.btn_pos_center.setStyleSheet(neutralbtn)
        self.ui.btn_pos_menu.setEnabled(False)
        self.ui.btn_pos_menu.setStyleSheet(disablebtn)

    def setup_posReset(self):
        self.ui.btn_pos_menu.setEnabled(True)
        self.ui.btn_pos_menu.setStyleSheet(whitebtn)
        self.ui.btn_pos_center.setStyleSheet(neutralbtn)
        self.ui.btn_pos_position.setStyleSheet(neutralbtn)

    def Xplus(self):
        self.xpos_counter += 2  # 2cm steps
        if self.xpos_counter >= 25:
            self.xpos_counter = 24
        self.ui.lbl_pos_showxpos.setText(str(self.xpos_counter))
        
    def Xminus(self):
        self.xpos_counter -= 2  # 2cm steps
        if self.xpos_counter <= -25:
            self.xpos_counter = -24
        self.ui.lbl_pos_showxpos.setText(str(self.xpos_counter))
        
    def Yplus(self):
        self.ypos_counter += 2  # 2cm steps
        if self.ypos_counter >= 15:
            self.ypos_counter = 14
        self.ui.lbl_pos_showypos.setText(str(self.ypos_counter))
        
    def Yminus(self):
        self.ypos_counter -= 2  # 2cm steps
        if self.ypos_counter <= -15:
            self.ypos_counter = -14
        self.ui.lbl_pos_showypos.setText(str(self.ypos_counter))
        
        

    def setup_pattRectangle(self):
        self.ui.btn_patt_rectangle.setStyleSheet(clickedbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)

    def setup_pattCircle(self):
        self.ui.btn_patt_circle.setStyleSheet(clickedbtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)

    def setup_pattInfinity(self):
        self.ui.btn_patt_infinity.setStyleSheet(clickedbtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)

    def setup_pattCenter(self):
        self.ui.btn_patt_center.setStyleSheet(clickedbtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)
    
    def setup_pattReset(self):
        self.ui.btn_patt_menu.setEnabled(True)
        self.ui.btn_patt_menu.setStyleSheet(whitebtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)

        


neutralbtn = """ 
QPushButton {
border-width: 2px;
border-style: outset;
border-radius: 7;
padding: 3px;
border-color: #0c1b33;
background-color: rgb(189, 213, 234);
color: #0c1b33;
}
"""
clickedbtn = """
QPushButton {
border-width: 2px;
border-style: outset;
border-radius: 7;
padding: 3px;
border-color: #0c1b33;
background-color: rgb(79, 178, 134);
color: #0c1b33;
}
"""
disablebtn = """
QPushButton {
border-width: 2px;
border-color: rgb(179, 179, 179);
border-style: solid;
border-radius: 7;
padding: 3px;
background-color: #fbfbff;
}
"""
whitebtn = """
QPushButton {
border-width: 2px;
border-style: solid;
border-radius: 7;
padding: 3px;
color: rgb(12, 27, 51);
border-color: rgb(12, 27, 51);
background-color: rgb(251, 251, 255);
}
"""

if __name__ == '__main__':
    directorObj = Director(0, 'COM9', True)
    app = qtw.QApplication(sys.argv)
    main_win = ballgui(directorObj)
    main_win.show()
    sys.exit(app.exec_())