import gpiozero
from gpiozero import DigitalOutputDevice
from collections import namedtuple
import numpy as np
from gpiozero.threads import GPIOThread

#config object for Stepper class so we can serialize it.
#note : step_per_rev is the actual amounts of steps per revolution, not the driver's.
StepperConfig = namedtuple("StepperConfig",
                                ["Name","step_pin_id",
                                "dir_pin_id",
                                "step_per_rev",
                                "mm_per_rad"]) # linear to angular movement ratio (gear radius, lead screw pitch, etc.)

class Stepper:
    """Stepper motor driver wrapper class. Intended to be used with DM320T drivers"""
    def __init__(self,step_config : StepperConfig) :

        self.config = step_config
        
        self.step_pin = DigitalOutputDevice(step_config.step_pin_id,
                                            initial_value=False,
                                            active_high=True)
        #some motors might only turn in one direction and won't require a DIR pin
        self.dir_pin = DigitalOutputDevice(step_config.dir_pin_id,
                                           initial_value=False,
                                           active_high=True) if step_config.dir_pin_id else None

        #default speed for testing
        Stepper.default_speed = 300
        

    def is_moving(self):
        """Check if the pulse pin is currently blinking with a background thread.
        the property _blink_thread is set to non None values when blink is called and to None
        when _stop_blink is."""
        return self.step_pin._blink_thread is None
        
    def move_steps(self,step_numb,rpm = None, duty_ratio=0.1) :
        """move a certain number of steps (driver microsteps, not motor steps).
        step_numb : number of steps to move. sign gives direction.
        rpm : speed to use. defaults at max speed *0.4
        duty_ratio : ratio of step signal"""
        
        if step_numb==0 :
                return
                
        if self.dir_pin :
            self.dir_pin.on() if step_numb >0 else  self.dir_pin.off()
            
        actual_rpm = Stepper.default_speed if rpm is None else rpm
        t_pulse = 1/((actual_rpm/60)*self.config.step_per_rev)
        
        self.step_pin.blink(t_pulse*duty_ratio,
                            t_pulse*(1-duty_ratio),
                            n=abs(step_numb),
                            background=True)
                            

    def move_degs(self, degs, rpm=None, duty_ratio=0.1) :
        """rotate a certain angle in degrees."""
        
        steps = round (degs/360.0 * self.config.step_per_rev)
        self.move_steps(steps,rpm,duty_ratio)

    def move_rads(self, rads, rpm=None, duty_ratio=0.1) :
        steps = round(rads / (2*np.pi) * self.config.step_per_rev)
        self.move_steps(steps, rpm, duty_ratio)

    def move_mm(self, delta_mm, rpm=None, duty_ratio=0.1) :
        """rotate in millimeters according to config.mm_per_rad"""
        req_rads = delta_mm/self.config.mm_per_rad
        self.move_rads(req_rads, rpm, duty_ratio)

    def move_rpm(self, rpm, duty_ratio=0.1) :

        if rpm < 0 :
            self.dir_pin.off()
        else:
            self.dir_pin.on()
        pulse_duration = 1/(self.config.step_per_rev * (rpm/60))
        self.step_pin.blink(pulse_duration*duty_ratio,pulse_duration*(1-duty_ratio))


    def follow_spd_profile(self,seq, background=False):
        """iterate through a sequence [(s0,n0),(s1,n1),....] where s is the requested speed and n the numbers of steps,
        sending a square signal of varying frequency to the GPIO to move the stepper motor."""

        self.step_pin._stop_blink()
        self.dir_pin.off()
        self.step_pin._blink_thread = GPIOThread(self.iterate_profile,seq)
        self.step_pin._blink_thread.start()
        if not background :
            self._blink_thread.join()
            self._blink_thread = None

    def iterate_profile(self, seq):

        steps_taken = 0 #track movement

        for spd,n in seq :
            on_time = 5/spd
            off_time = 4*on_time
            if self.dir_pin :
                self.dir_pin._write(spd<0)
            for _ in range(n):
                self.step_pin._write(True)
                steps_taken+=1
                if self.step_pin._blink_thread.stopping.wait(on_time):
                    break
                self.step_pin._write(False)
                if self.step_pin._blink_thread.stopping.wait(off_time):
                    break
        return steps_taken



    def stop(self):
        """stop motor by setting PUL and DIR to OFF."""
        self.step_pin._stop_blink()
        if self.dir_pin is not None:
            self.dir_pin._stop_blink()
        
    def __del__(self):
            self.stop()
            
