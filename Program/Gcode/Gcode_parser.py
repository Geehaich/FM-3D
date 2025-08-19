import os
from Gcode_cmds import GcodeCommands

def check_file(filename):
    """count non-comment lines in a gcode file and check if every code present has been implemented"""
    tot_count = 0
    count = 0
    nimp = []
    first_com_line = -1 #locate first non comment line to go there later
    with open(filename) as f:
        for line in f:
            tot_count+=1
            if not line.startswith(';') :
                count += 1
                if line.split(" ")[0] and line.split(" ")[0] not in GcodeCommands.__dict__:
                     if line.split(' ')[0] not in nimp:
                         nimp.append(line.split(" ")[0])
                if first_com_line == -1:
                    first_com_line = tot_count
        if nimp:
            raise NotImplementedError(", ".join(nimp)+" not implemented")
    return count, first_com_line


class GcodeReader :

    def __init__(self,filepath):
        self.total_lines, first_com = check_file(filepath)
        self.f_obj = open(filepath,'r')
        self.is_eof = False
        self.current_com = self.get_next_command()


    def get_next_command(self):
        nextline = self.f_obj.readline()
        while nextline and (nextline.startswith(';') or len(nextline)==0):
            nextline = self.f_obj.readline()

        if nextline is None :
            self.is_eof = True
        self.current_com = nextline.strip().split(";")[0]
        return self.current_com

    def __del__(self):
        self.f_obj.close()

    def parse_current(self):
        s_com = self.current_com.split(" ")
        func = s_com[0]
        args = {}
        for i in range(1,len(s_com)-1):
            if s_com[i] :
                args[s_com[i][0]] = float(s_com[i][1:]) if len(s_com[i])>1 else None
        return (GcodeCommands.__dict__[func],args)


