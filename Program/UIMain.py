from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout
import PyQt6.QtWidgets as pqw
from Step_controller import PrintController

from Stepper import StepperConfig
# Only needed for access to command line arguments
import sys

class TestUI(QWidget):

    def __init__(self,print_controller : PrintController):
        super().__init__()

        self.con_ref = print_controller
        self.lay = QGridLayout()
        self.but_Xplus = QPushButton("X+")
        self.but_Xminus = QPushButton("X-")
        self.but_Eplus = QPushButton("E+")
        self.but_Eminus = QPushButton("E-")

        if self.con_ref !=None:
            self.but_Xplus.pressed.connect(lambda : self.con_ref.x_motor.move_rpm(60))
            self.but_Xplus.released.connect(lambda : self.con_ref.x_motor.stop())
            self.but_Xminus.pressed.connect(lambda : self.con_ref.x_motor.move_rpm(-60))
            self.but_Xminus.released.connect(lambda : self.con_ref.x_motor.stop())
            self.but_Eplus.pressed.connect(lambda: self.con_ref.print_head.e_motor.move_rpm(-40))
            self.but_Eplus.released.connect(lambda: self.con_ref.print_head.e_motor.stop())
            self.but_Eminus.pressed.connect(lambda: self.con_ref.print_head.e_motor.move_rpm(-40))
            self.but_Eminus.released.connect(lambda: self.con_ref.print_head.e_motor.stop())


        radio_lay = QHBoxLayout()
        self.rad_las_off = pqw.QRadioButton("OFF")
        self.rad_las_oneperc = pqw.QRadioButton("1%")
        self.rad_las_on = pqw.QRadioButton("ON")
        self.rad_las_off.toggled.connect(self.las_pow_select)
        self.rad_las_oneperc.toggled.connect(self.las_pow_select)
        self.rad_las_on.toggled.connect(self.las_pow_select)

        radio_lay.addWidget(self.rad_las_off)
        radio_lay.addWidget(self.rad_las_oneperc)
        radio_lay.addWidget(self.rad_las_on)


        self.lay.addWidget(QLabel("X axis"),0,0)
        self.lay.addWidget(self.but_Xplus,0,1)
        self.lay.addWidget(self.but_Xminus,0,2)
        self.lay.addWidget(QLabel("E axis"),1,0)
        self.lay.addWidget(self.but_Eplus,1,1)
        self.lay.addWidget(self.but_Eminus,1,2)
        self.lay.addWidget(QLabel("Laser"),2,0)
        self.lay.addLayout(radio_lay,2,1)

        self.setLayout(self.lay)

    def las_pow_select(self):

        if self.rad_las_on.isChecked():
            self.con_ref.print_head.start_laser(80)
        if self.rad_las_oneperc.isChecked():
            self.con_ref.print_head.start_laser(1)
        if self.rad_las_off.isChecked():
            self.con_ref.print_head.stop_laser()



conf_X = StepperConfig("X",3,4,800,10)
conf_E = StepperConfig("E",14,15,800,4)
print(conf_E)
prin_conf = PrintController(conf_X,None,None,None,conf_E,21)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
Testwid = TestUI(prin_conf)
Testwid.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
