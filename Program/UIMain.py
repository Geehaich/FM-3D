from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout, QLineEdit
import PyQt6.QtWidgets as pqw
from Step_controller import PrintController

from Stepper import StepperConfig
# Only needed for access to command line arguments
import sys

class TestUI(QWidget):

    def __init__(self,print_controller : PrintController):
        super().__init__()

        self.con_ref = print_controller
        self.lay = QVBoxLayout()

        hlx = QHBoxLayout() #group of controls for the X axis. buttons for mvt in either direction, QLine edit for speed in rpm
        self.but_Xplus = QPushButton("X+")
        self.but_Xplus.setFixedSize(60, 30)
        self.but_Xminus = QPushButton("X-")
        self.but_Xminus.setFixedSize(60, 30)
        self.qlin_x_spd = QLineEdit("60")
        self.qlin_x_spd.setValidator(QIntValidator(1, 100))
        self.qlin_x_spd.setFixedSize(60, 30)

        hlx.addWidget(QLabel("X")) #add to layout
        hlx.addWidget(self.but_Xplus)
        hlx.addWidget(self.but_Xminus)
        hlx.addWidget(self.qlin_x_spd)

        self.lay.addLayout(hlx)

        hle = QHBoxLayout() #same for E (extruder) axis
        self.but_Eplus = QPushButton("E+")
        self.but_Eminus = QPushButton("E-")
        self.but_Eplus.setFixedSize(60,30)
        self.but_Eminus.setFixedSize(60,30)
        self.qlin_e_spd = QLineEdit("40")
        self.qlin_e_spd.setValidator(QIntValidator(1,100))
        self.qlin_e_spd.setFixedSize(60, 30)

        hle.addWidget(QLabel("E"))
        hle.addWidget(self.but_Eplus)
        hle.addWidget(self.but_Eminus)
        hle.addWidget(self.qlin_e_spd)
        self.lay.addLayout(hle)

        self.print_but = QPushButton('PRINT')
        self.print_but.setFixedSize(150,50)
        self.lay.addWidget(self.print_but,alignment=Qt.AlignmentFlag.AlignCenter)

        if self.con_ref is not None:
            self.but_Xplus.pressed.connect(lambda : self.con_ref.x_motor.move_rpm(int(self.qlin_x_spd.text())))
            self.but_Xplus.released.connect(lambda : self.con_ref.x_motor.stop())
            self.but_Xminus.pressed.connect(lambda : self.con_ref.x_motor.move_rpm(-int(self.qlin_x_spd.text())))
            self.but_Xminus.released.connect(lambda : self.con_ref.x_motor.stop())
            self.but_Eplus.pressed.connect(lambda: self.con_ref.print_head.e_motor.move_rpm(int(self.qlin_e_spd.text())))
            self.but_Eplus.released.connect(lambda: self.con_ref.print_head.e_motor.stop())
            self.but_Eminus.pressed.connect(lambda: self.con_ref.print_head.e_motor.move_rpm(-int(self.qlin_e_spd.text())))
            self.but_Eminus.released.connect(lambda: self.con_ref.print_head.e_motor.stop())


        radio_lay = QHBoxLayout()
        radio_lay.addWidget(QLabel("Laser"))
        self.rad_las_off = pqw.QRadioButton("OFF")
        self.rad_las_oneperc = pqw.QRadioButton("1%")
        self.rad_las_on = pqw.QRadioButton("ON")
        self.rad_las_off.toggled.connect(self.las_pow_select)
        self.rad_las_oneperc.toggled.connect(self.las_pow_select)
        self.rad_las_on.toggled.connect(self.las_pow_select)

        radio_lay.addWidget(self.rad_las_off)
        radio_lay.addWidget(self.rad_las_oneperc)
        radio_lay.addWidget(self.rad_las_on)

        self.lay.addLayout(radio_lay)
        #self.rad_las_off.click()



        self.setLayout(self.lay)

    def las_pow_select(self):

        if self.rad_las_on.isChecked():
            self.con_ref.print_head.start_laser(80)
        if self.rad_las_oneperc.isChecked():
            self.con_ref.print_head.start_laser(1)
        if self.rad_las_off.isChecked():
            self.con_ref.print_head.stop_laser()

    def print_move(self):

        self.rad_las_on.click()
        self.con_ref.x_motor.move_rpm(int(self.qlin_x_spd.text()))
        self.con_ref.print_head.e_motor.move_rpm(int(self.qlin_e_spd.text()))

    def print_stop(self):
        self.rad_las_off.click()
        self.con_ref.x_motor.stop()
        self.con_ref.print_head.stop()


#conf_X = StepperConfig("X",3,4,800,10)
#conf_E = StepperConfig("E",17,27,800,4)
#prin_conf = PrintController(conf_X,None,None,None,conf_E,21)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
Testwid = TestUI(None)
Testwid.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
