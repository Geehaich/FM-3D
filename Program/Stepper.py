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
        
        
        
    def move_steps(self,step_numb,rpm = None, duty_ratio=0.1) :
        """move a certain number of steps (driver microsteps, not motor steps).
        step_numb : number of steps to move. sign gives direction.
        rpm : speed to use. defaults at max speed *0.4
        duty_ratio : ratio of step signal"""
        
        if step_numb==0 :
                return
                
        if self.dir_pin :
            self.dir_pin.on() if step_numb >0 else  self.dir_pin.off()
            
        actual_rpm = Stepper.capped_rpm*0.4 if rpm is None else min(abs(rpm),Stepper.capped_rpm)
        t_pulse = 1/((actual_rpm/60)*self.config.step_per_rev)
        
        self.step_pin.blink(t_pulse*duty_ratio,
                            t_pulse*(1-duty_ratio),
                            n=abs(step_numb),
                            background=True)
                            

    def move_degs(self, degs, rpm=None, duty_ratio=0.1) :
        """rotate a certain angle in degrees."""
        
        steps = round (degs/360.0 * self.config.step_per_rev)
        self.move_steps(steps,rpm,duty_ratio)
        

    def spin(self,rpm, duty_ratio=0.1) :
        """start rotating at given speed.
        args :
        rpm : speed in rounds per minute. sign gives direction.
        step_ratio : the cyclic ratio of the pulses sent."""
        
        if rpm==0 :
                return
        if self.dir_pin :
            self.dir_pin.on() if rpm >0 else self.dir_pin.off()
        
        actual_rpm = min(abs(rpm),Stepper.capped_rpm)
        
        t_pulse = 1/((actual_rpm/60)*self.config.step_per_rev)
        self.step_pin.blink(t_pulse*duty_ratio,
                            t_pulse*(1-duty_ratio))

    def stop(self):
        """stop motor by setting PUL and DIR to OFF."""
        self.step_pin._stop_blink()
        if self.dir_pin is not None:
            self.dir_pin._stop_blink()
        
    def __del__(self):
            self.stop()
            
