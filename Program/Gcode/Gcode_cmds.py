import numpy as np

class GcodeCommands :
    """Translate common G-Codes found in CURA files into actions.
    Some actions don't make sense in our case (bed heating for example) and will be ignored
    """
    def G0(cls,ctrl,**kwargs): #move

        argvector = np.zeros(4)
        if "X" in kwargs :
            argvector[0] = kwargs["X"]
        if "Y" in kwargs :
            argvector[1] = kwargs["Y"]
        if "Z" in kwargs :
            argvector[2] = kwargs["Z"]
        if "E" in kwargs :
            argvector[3] = kwargs["E"]

        if "F" in kwargs :
            ctrl.print_head.feedrate = min(kwargs["F"],ctrl.print_head.max_feedrate)
        ctrl.move_axes(argvector,False)


    def G1(cls,ctrl,**kwargs): #move and print
        argvector = np.zeros(4)
        if "X" in kwargs:
            argvector[0] = kwargs["X"]
        if "Y" in kwargs:
            argvector[1] = kwargs["Y"]
        if "Z" in kwargs:
            argvector[2] = kwargs["Z"]
        if "E" in kwargs:
            argvector[3] = kwargs["E"]

        if "F" in kwargs:
            ctrl.print_head.feedrate = min(kwargs["F"], ctrl.print_head.max_feedrate)
        ctrl.move_axes(argvector, True)




    def G28(cls,ctrl):
        ctrl.home()

    def G90(self,ctrl):
        ctrl.absolute_axis= True
        ctrl.absolute_extruder= True

    def G91(self,ctrl):
        ctrl.absolute_axis = False
        ctrl.absolute_extruder = False


    def M82(self,ctrl):
        ctrl.absolute_extruder = False

    def M104(cls,ctrl): #set hotend temperature.ignored.
        pass

    def M106(cls,ctrl): #turn off fan. ignored.
        pass


    def M109(cls,ctrl): #wait for temperature.
        pass

    def M105(cls,ctrl): #report temperature. ignored, no heated bed, no heated nozzle.
        pass

    def M140(cls,ctrl): #bed heating. ignored, no heated bed
        pass

    def M190(cls,ctrl): #wait for temperature. ignored.
        pass

    def M203(cls,ctrl, **kwargs): pass
        #ctrl.print_head.max_feedrate =
    def M205(cls,ctrl): pass