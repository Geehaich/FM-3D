import gpiozero
from gpiozero import DigitalOutputDevice
from collections import namedtuple

StepperConfig = namedtuple("StepperConfig", ["Name","pin_step_id","pulse_per_rev","dir_pin_id"])

class Stepper:

    def __init__(self,step_config : StepperConfig) :

        self.config = step_config
        self.step_pin = DigitalOutputDevice(step_config.pin_step_id,
                                            initial_value=False,
                                            active_high=True)
        self.dir_pin = DigitalOutputDevice(step_config.dir_pin_id,
                                           initial_value=False,
                                           active_high=True) if step_config.dir_pin_id else None
        
        
        
        
    def reach_position(self,step_numb) :

        if self.dir_pin :
            self.dir_pin.on() if step_numb >0 else  self.dir_pin.off()
        self.step_pin.blink(on_time=1e-4,
                            off_time= 1e-4,
                            n=step_numb,
                            background=True)
        self.dir_pin.off()
        self.step_pin.off()
        
    def spin(self,rpm=100) :

        if self.dir_pin :
            self.dir_pin.on() if rpm >0 else self.dir_pin.off()

