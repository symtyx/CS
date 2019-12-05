#Name: Mohammed Zafir Rahman
#Homework
#Due Date: 12/3/2019
#------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that
# violates the ethical guidelines set forth by professor and class syllabus.
#------------------------------------------------------------------------------
# References: (Zybook, Teacher Help, Piazza, Advice from Nafiz Ahmed)

#Use python testerH8.py mrahma32_201_H8.py for testing
#Use python -i mrahma32_201_H8.py to fix tests

class Device:
    def __init__(self, name, watts=100, on=False):
        self.name = name
        self.watts = watts
        self.on = on
    def __str__(self):
        self.W = "(+" + str(self.watts) + "W:" + ' ' + str(self.name) + ")"
        self.WF = "(+" + str(0) + "W:" + ' ' + str(self.name) + ")"
        if self.on == False:
            return self.WF
        else:    
            return self.W
    def __repr__(self):
        R = "Device(" + "'" + str(self.name) + "'" + ',' + ' '
        E = str(self.watts) + ',' + ' ' + str(self.on) + ')' 
        self.RE = R + E
        return self.RE
    def __eq__(self,other): 
        if self.name == other.name:
            if self.watts == other.watts:
                if self.on == other.on:
                    return True
        else:
            return False
    def turn_on (self):
        self.on = True
    def turn_off(self):
        self.on = False
    def toggle (self):
        if self.on == True:
            self.on = False
        else:
            self.on = True
        
class Outlet:	
    def __init__(self, devices=None):
        if devices == None:
            self.devices = []
        else:
            self.devices = devices
    def __str__(self): 
        if len(self.devices) == 0:
            return 'Outlet(' + str(self.devices) + ')'
        else:
            NF = 'Outlet(['
            for i in range(len(self.devices)):
                if i == 0:
                    NF += Device.__str__(self.devices[i])
                else:
                    NF += ' ' + Device.__str__(self.devices[i])
                if i != len(self.devices) - 1:
                    NF += ','
            NF += '])'
            return NF
    def __repr__(self):
        RF = 'Outlet(['
        for i in range(len(self.devices)):
            if i == 0:
                RF += Device.__repr__(self.devices[i])
            else:
                RF += ' ' + Device.__repr__(self.devices[i])
            if i != len(self.devices) - 1:
                RF += ','
        RF += '])'
        return RF
    def __eq__(self,other):
        self.other = other
        if self.devices == self.other:
            return True
        elif self.devices != self.other:
            return False
    def max_watts(self):
        sum = 0
        RF = []
        for i in range(len(self.devices)):
            RF.append(Device.__repr__(self.devices[i])) 
        for i in range(len(RF)):
            RF[i] = RF[i].strip('Device()')
            RF[i] = int(RF[i].split(",")[1].strip())
        for i in RF:
            sum += i            
        return sum
    def watts_now(self): 
        sum = 0
        RF = []
        copy = []
        for i in range(len(self.devices)):
            RF.append(Device.__repr__(self.devices[i])) 
        for i in range(len(RF)):
            RF[i] = RF[i].strip('Device()')
        for i in RF:
            if 'Tr' in i:            
                copy.append(i)
        for i in range(len(copy)):
            copy[i] = int(copy[i].split(",")[1].strip())
        for i in copy:
            sum += i            
        return sum
    def add_device(self, device): 
        self.devices.append(device)
    def remove_device(self, name):
        step = []
        for i in self.devices:
            if i.name == name:
                step.append(self.devices.pop(self.devices.index(i)))
                return step[-1]
    def turn_off_all(self):
        for i in self.devices:
            if i.on == True:
                i.on = False
#python testerH8.py mrahma32_201_H8.py
class Circuit: 
    def __init__(self, outlets=None):
        if outlets == None:
            self.outlets = []
        else:
            self.outlets = outlets
    def __str__(self):
        if len(self.outlets) == 0:
            return 'Circuit(' + str(self.outlets) + ')'
        else:
            NF = 'Circuit(['
            for i in range(len(self.outlets)):
                if i == 0:
                    NF += Outlet.__str__(self.outlets[i])
                else:
                    NF += ' ' + Outlet.__str__(self.outlets[i])
                if i != len(self.outlets) - 1:
                    NF += ','
            NF += '])'
            return NF
    def __repr__(self):
        return None
    def __eq__(self,other):
            if self.outlets == other:
                return True
            else:
                return False
    def add_outlet(self, outlet):
        self.outlets.append(outlet)
    def max_watts(self):
        sum = 0
        RF = []
        for i in range(len(self.outlets)):
            RF.append(Outlet.__repr__(self.outlets[i])) 
        for i in range(len(RF)):
            RF[i] = RF[i].strip('Device()')
            RF[i] = int(RF[i].split(",")[1].strip())
        for i in RF:
            sum += i + 1           
        return sum
    def watts_now(self):
        sum = 0
        RF = []
        copy = []
        for i in range(len(self.outlets)):
            RF.append(Outlet.__repr__(self.outlets[i])) 
        for i in range(len(RF)):
            RF[i] = RF[i].strip('Device()')
        for i in RF:
            if 'Tr' in i:            
                copy.append(i)
        for i in range(len(copy)):
            copy[i] = int(copy[i].split(",")[1].strip())
        for i in copy:
            sum += i            
        return sum
    def turn_off_all(self): 
        for i in self.outlets:
            i.turn_off_all()