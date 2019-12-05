class Device:
    def __init__(self,name, watts = 100, on = False):
        self.name = name
        self.watts = watts
        self.on = on
    
    def __str__(self):
        if self.on == True:
            return '(+' + str(self.watts) + 'W' + ': ' + self.name + ')'
        if self.on == False:
            return '(+0W' + ': ' + self.name + ')'
        
    def __repr__(self):
        return "Device" + '(' + '\'' + self.name + '\'' + ', ' + str(self.watts) + ', ' + str(self.on) + ')'

    def __eq__(self, other):
        if (self.name == other.name) and (self.watts == other.watts) and (self.on == other.on):
            return True
        else:
            return False

    def turn_on(self):
        self.on = True
    def turn_off(self):
        self.on = False
    def toggle(self):
        if self.on == True:
            self.on = False
        elif self.on == False:
            self.on = True

class Outlet:
    def __init__(self, devices=None):
        self.devices = devices
        if self.devices == None:
            self.devices = []

    def __str__(self):
        #for d in self.devices:
        #   return "Outlet({})".format(str(d))
        string = 'Outlet(['
        if len(self.devices) == 0:
            return 'Outlet([])'
        for item in self.devices:
            if self.devices[item] == self.devices[0]:
                string += Device.__str__(self.devices[item])
            if self.devices[item] != self.devices[0]:
                string += ' ' + Device.__str__(self.devices[item])
        
        return string
    def __repr__(self):
        return "Outlet({})".format(self.devices)
        
    def __eq__(self, other):
        if self.devices == other.devices:
            return True

    def max_watts(self):
        wattage = 0
        if len(self.devices) == 0:
            return wattage
        else:
            '''for item in self.devices:
                if item == len(self.devices)-1:
                    wattage += self.devices
            return wattage'''
            for item in self.devices:
                wattage += int(Device.__str__(watts))

            return wattage

class Circuit:
    def __init__(self, outlets=None):
        self.outlets = outlets
        if self.outlets == None:
            self.outlets = []
    
    #def __str__(self):

    def __repr__(self):
        return "Outlet({})".format(self.outlets)