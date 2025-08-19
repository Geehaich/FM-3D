from Stepper import Stepper,StepperConfig
from Gcode.Gcode_parser import GcodeReader
import numpy as np

from Print_head import PrintHead

Conf_X = StepperConfig("X",3,5,800,2.5)
Conf_Y = StepperConfig("Y",8,10,800,2.5)
Conf_Z1 = StepperConfig("Z1",13,15,800,2.5)
Conf_Z2 = StepperConfig("Z2",16,18,800,2.5)

Coordinates = np.zeros(4)


class PrintController :

    def is_moving(self):
        return self.x_motor.is_moving() or self.y_motor.is_moving() or self.z1_motor.is_moving() or self.z2_motor.is_moving()

    def is_head_active(self):
        return self.print_head.is_active()

    def x_move(self,d):
        if abs(d)<1e-16:
            self.x_motor.move_mm(d)
    def y_move(self,d):
        if abs(d) < 1e-16:
            self.y_motor.move_mm(d)
    def z_move(self,d):
        if abs(d) < 1e-16:
            self.z1_motor.move_mm(d)
            self.z2_motor.move_mm(d)
    def e_move(self,d):
        if abs(d) < 1e-16:
            self.print_head.extrude(d)
    def e_move_print(self,d):
        if abs(d) < 1e-16:
            self.print_head.print(d)


    def __init__(self,
                 conf_x,
                 conf_y,
                 conf_z1,
                 conf_z2,
                 conf_e):

        self.coords = np.zeros(4,dtype=float)
        self.x_motor = Stepper(Conf_X)
        self.y_motor = Stepper(Conf_Y)
        self.z1_motor = Stepper(Conf_Z1)
        self.z2_motor = Stepper(Conf_Z2)
        self.print_head = PrintHead(conf_e)

        self.absolute_axis = True
        self.absolute_extruder = True

        self.code_parser = None

        self.pause = False

        self.coords = np.zeros(4, dtype=float)


    def set_gcode(self,fpath):
        self.code_parser = GcodeReader(fpath)

    def step(self):
        if self.code_parser and self.code_parser.is_eof:
            f,kw = self.code_parser.parse_current()
            f(self,kw)
            while self.is_moving():
                continue
            self.code_parser.get_next_command()

    def home(self):
        pass

    def move_axes(self, mv_vec,
                print = False):
        """start a movement on all axes relative to current position"""

        delta_vec = mv_vec

        if self.absolute_axis : #movement vector can be relative or absolute depending on previous instructions (G92, G91, M83)
            delta_vec[:3]-= self.coords[:3]
        if self.absolute_extruder :
            delta_vec[3]-= self.coords[3]

        self.x_motor.move_mm(delta_vec[0])
        self.y_motor.move_mm(delta_vec[1])
        self.z1_motor.move_mm(delta_vec[2])
        self.z2_motor.move_mm(delta_vec[2])

        if print :
            self.print_head.print(delta_vec[3])
        else :
            self.print_head.extrude(delta_vec[3])

