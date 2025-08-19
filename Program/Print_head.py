
from Stepper import *
from gpiozero import PWMLED


class PrintHead :
    """Represents the printing head containing the laser module, the extruder and the various sensors (TBI)"""
    def __init__(self,e_config,laser_pin_id):
        self.laser_blink = PWMLED(laser_pin_id,
                             frequency=100)
        self.e_motor = Stepper(e_config)
        self.e_pos = 0

        self.feedrate = 20
        self.max_feedrate = 25

    def set_laser_power(self,percent):
        self.laser_blink.value = percent/100.0

    def start_laser(self, new_percent = 0):
        if new_percent:
            self.set_laser_power(new_percent)
        self.laser_blink.on()
    def stop_laser(self):
        self.laser_blink.off()

    def is_active(self):
        return self.laser_blink.is_active() or self.e_motor.is_moving()

    def extrude(self,E_ex_mm):
        self.e_motor.move_mm(E_ex_mm)

    def print(self,E_ex_mm):
        self.start_laser()
        self.extrude(E_ex_mm)
        while self.e_motor.is_moving() :
            continue
        self.stop_laser()
        self.e_pos += E_ex_mm


    def stop(self):
        self.stop_laser()
        self.Axis_E.stop()