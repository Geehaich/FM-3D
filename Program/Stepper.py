import gpiozero
from gpiozero import DigitalOutputDevice
from collections import namedtuple

#config object for Stepper class so we can serialize it.
#note : step_per_rev is the actual amounts of steps per revolution, not the driver's.
#it's identical for motors with 1.8° resolution but some have 0.9 and will need twice that.
StepperConfig = namedtuple("StepperConfig",
                                ["Name","pin_step_id",
                                "step_per_rev",
                                "dir_pin_id"])

class Stepper:
    """Stepper motor driver wrapper class. Intended to be used with DM320T drivers"""
    def __init__(self,step_config : StepperConfig) :

        self.config = step_config
        
        self.step_pin = DigitalOutputDevice(step_config.pin_step_id,
                                            initial_value=False,
                                            active_high=True)
        #the drill motors only turn in one direction and won't require a DIR pin
        self.dir_pin = DigitalOutputDevice(step_config.dir_pin_id,
                                           initial_value=False,
                                           active_high=True) if step_config.dir_pin_id else None
        
        #cap movement speed to something reasonable
        Stepper.capped_rpm = 300
        
        
        
    def reach_position_step(self,step_numb,rpm = None, duty_ratio=0.2) :
        """move a certain number of steps (driver microsteps, not motor steps).
        step_numb : number of steps to move. sign gives direction.
        rpm : speed to use. defaults at max speed *0.4
        duty_ratio : ratio of step signal"""
        if self.dir_pin :
            self.dir_pin.on() if step_numb >0 else  self.dir_pin.off()
            
        actual_rpm = Stepper.capped_rpm*0.4 if rpm is None else min(abs(rpm),Stepper.capped_rpm)
        t_pulse = 1/((actual_rpm/60)*self.config.step_per_rev)
        
        self.step_pin.blink(t_pulse*duty_ratio,
                            t_pulse*(1-duty_ratio),
                            n=abs(step_numb),
                            background=True)
                            
        self.dir_pin.off()
        self.step_pin.off()

    def spin(self,rpm=100, duty_ratio=0.2) :
        """start rotating at given speed.
        args :
        rpm : speed in rounds per minute. sign gives direction.
        step_ratio : the cyclic ratio of the pulses sent."""
        if self.dir_pin :
            self.dir_pin.on() if rpm >0 else self.dir_pin.off()
        
        actual_rpm = min(abs(rpm),Stepper.capped_rpm)
        
        t_pulse = 1/((actual_rpm/60)*self.config.step_per_rev)
        print(t_pulse)
        self.step_pin.blink(t_pulse*duty_ratio,
                            t_pulse*(1-duty_ratio))

    def stop(self):
        """stop motor by setting PUL and DIR to OFF."""
        self.step_pin.off()
        self.dir_pin.off()
        
    def __del__(self):
            self.stop()
