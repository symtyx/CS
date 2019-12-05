# Based on testing harness dated 2017-06-02.

# STUDENTS: TO USE:
# 
# The following command will test all test cases on your file:
# 
#   python3 <thisfile.py> <your_one_file.py>
# 
# 
# You can also limit the tester to only the functions you want tested.
# Just add as many functions as you want tested on to the command line at the end.
# Example: to only run tests associated with func1 and func2, run this command:
# 
#   python3 <thisfile.py> <your_one_file.py> func1 func2
# 
# You really don't need to read the file any further, except that when
# a specific test fails, you'll get a line number - and it's certainly
# worth looking at those areas for details on what's being checked. This would
# all be the indented block of code starting with "class AllTests".


# INSTRUCTOR: TO PREPARE:
#  - add test cases to class AllTests. The test case functions' names must
# be precise - to test a function named foobar, the test must be named "test_foobar_#"
# where # may be any digits at the end, such as "test_foobar_13".
# - any extra-credit tests must be named "test_extra_credit_foobar_#"
# 
# - name all required definitions in REQUIRED_DEFNS, and all extra credit functions
#   in EXTRA_CREDIT_DEFNS. Do not include any unofficial helper functions. If you want
#   to make helper definitions to use while testing, those can also be added there for
#   clarity.
# 
# - to run on either a single file or all .py files in a folder (recursively):
#   python3 <thisfile.py> <your_one_file.py>
#   python3 <thisfile.py> <dir_of_files>
#   python3 <thisfile.py> .                    # current directory
# 
# A work in progress by Mark Snyder, Oct. 2015.
#  Edited by Yutao Zhong, Spring 2016.
#  Edited by Raven Russell, Spring 2017.
#  Edited by Mark Snyder, June 2017.


import unittest
import shutil
import sys
import os
import time


############################################################################
############################################################################
# BEGIN SPECIALIZATION SECTION (the only part you need to modify beyond 
# adding new test cases).

# name all expected definitions; if present, their definition (with correct
# number of arguments) will be used; if not, a decoy complainer function
# will be used, and all tests on that function should fail.
    
REQUIRED_DEFNS = ["Device",
                  "Outlet",
                  "Circuit",
                 ]

# for method names in classes that will be tested
SUB_DEFNS = [ "eq",
              "device_on_off_toggle",
              "outlet_max_watts",
              "outlet_watts_now",
              "add_device",
              "remove_device",
              "outlet_turn_off_all",
              "add_outlet",
              "circuit_max_watts",
              "circuit_watts_now",
              "circuit_turn_off_all",
            ]

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = []

# how many points are test cases worth?
weight_required = 2.5 
weight_extra_credit = 0

# don't count extra credit; usually 100% if this is graded entirely by tests.
# it's up to you the instructor to do the math and add this up!
# TODO: auto-calculate this based on all possible tests.
total_points_from_tests = 100

# how many seconds to wait between batch-mode gradings? 
# ideally we could enforce python to wait to open or import
# files when the system is ready but we've got a communication
# gap going on.
DELAY_OF_SHAME = 1


# set it to true when you run batch mode... 
CURRENTLY_GRADING = False



# what temporary file name should be used for the student?
# This can't be changed without hardcoding imports below, sorry.
# That's kind of the whole gimmick here that lets us import from
# the command-line argument without having to qualify the names.
RENAMED_FILE = "student"




# END SPECIALIZATION SECTION
############################################################################
############################################################################


# enter batch mode by giving a directory to work on as the only argument.
BATCH_MODE = len(sys.argv)==2 and (sys.argv[1] in ["."] or os.path.isdir(sys.argv[1]))

# This class contains multiple "unit tests" that each check
# various inputs to specific functions, checking that we get
# the correct behavior (output value) from completing the call.
class AllTests (unittest.TestCase):

    ############################################################################
    
    # helper function to ensure that Device.__eq__ works before attempting anything that relies upon it.
    def ensure_Device_eq(self):
        try:
            self.assertEqual(Device("a",1,True),Device("a",1,True))
            self.assertEqual(Device("b",1,False)==Device("c",1,True), False)
        except:
            self.fail("you need to correctly define __eq__ for Device before debugging this one (it relies on it!)")
    
    #---------------------------------------------------------------------------
    
    def test_Device_1(self):
        """Device.__init__"""
        d = Device("bulb",75,True)
        self.assertEqual(d.name,  "bulb")
        self.assertEqual(d.watts, 75    )
        self.assertEqual(d.on,    True  )
        
    def test_Device_2(self):
        """Device.__init__ with defaults"""
        d = Device("curling iron")
        self.assertEqual(d.name,  "curling iron")
        self.assertEqual(d.watts, 100           )
        self.assertEqual(d.on,    False         )
    
    def test_Device_3(self):
        """Device.__str__"""
        self.assertEqual(str(Device("nightlight",30,True )),"(+30W: nightlight)")
        self.assertEqual(str(Device("TV",30,False)),"(+0W: TV)")
    
    def test_Device_4(self):
        """Device.__repr__"""
        self.assertEqual(repr(Device("nightlight",30,True )),"Device('nightlight', 30, True)")
        self.assertEqual(repr(Device("TV",30,False)),"Device('TV', 30, False)")
    
    #---------------------------------------------------------------------------
    
    def test_Outlet_1(self):
        """Outlet.__init__"""
        
        # first, ensure that Device.__eq__ works before attempting anything that relies upon it.
        self.ensure_Device_eq()
        
        # empty list given.
        v1 = Outlet([])
        self.assertEqual(v1.devices,[])
        
        # default None means an empty list should be created.
        v2 = Outlet() 
        self.assertEqual(v2.devices,[])
        
        # non-empty list given.
        v3 = Outlet([Device("a",1,True),Device("b",2,False)])
        self.assertEqual(v3.devices,[Device("a",1,True),Device("b",2,False)])
        
        # another using the default; add to it, show it's not sharing with v2.
        v4 = Outlet()
        v4.devices.append(Device("d",4,True))
        self.assertEqual(v2.devices,[]) # this should still be empty (no sharing from a complex default argument.)
    
    def test_Outlet_2(self):
        """Outlet.__str__"""
        self.ensure_Device_eq() # we need Device.__eq__ to work.
        v1 = Outlet([])
        v2 = Outlet([Device("a",1,True),Device("b",2,False),Device("c",3,True)])
        
        self.assertEqual(str(v1),"Outlet([])")
        self.assertEqual(str(v2),"Outlet([(+1W: a), (+0W: b), (+3W: c)])")
    
    def test_Outlet_3(self):
        """Outlet.__repr__"""
        self.ensure_Device_eq() # we need Device.__eq__ to work.
        # same expected output as str. hint: just use str()...
        v1 = Outlet([])
        v2 = Outlet([Device("a",1,True),Device("b",2,False),Device("c",3,True)])
        
        self.assertEqual(repr(v1),"Outlet([])")
        self.assertEqual(repr(v2),"Outlet([Device('a', 1, True), Device('b', 2, False), Device('c', 3, True)])")
    
    #---------------------------------------------------------------------------
    
    def test_Circuit_1(self):
        """Outlet.__init__  (empty)"""
        c = Circuit([])
        self.assertEqual(c.outlets,[])
    
    def test_Circuit_2(self):
        """Outlet.__init__  (non-empty)"""
        self.ensure_Device_eq()
        ds2 = [Device("a",1,True),Device("b",2,False)]
        outs = [Outlet([]), Outlet(ds2)]
        c = Circuit(outs)
        self.assertEqual(c.outlets,outs)
    
    def test_Circuit_3(self):
        """Outlet.__init__  (using default arg.)"""
        self.ensure_Device_eq()
        c = Circuit()
        self.assertEqual(c.outlets,[])
        c.outlets.append(Outlet([Device("A",10,True)]))
        self.assertEqual(c.outlets[0].devices[0],Device("A",10,True))
        
    ############################################################################
    ############################################################################
    
    def test_device_on_off_toggle_1(self):
        """Device.on"""
        d = Device("Anathema",20,False) # Anathema Device, witch.
        self.assertEqual(d.on, False) # isn't on yet
        d.turn_on()
        self.assertEqual(d.on, True)  # now it's on
        
    def test_device_on_off_toggle_2(self):
        """Device.off"""
        d = Device("Jensen's",60,True) # it's a device
        self.assertEqual(d.on, True)  # isn't off yet
        d.turn_off()
        self.assertEqual(d.on, False) # now it's off
        
    def test_device_on_off_toggle_3(self):
        """Device.toggle"""
        d = Device("left to my own",30,True)
        self.assertEqual(d.on, True)  # starts on.
        d.toggle()
        self.assertEqual(d.on, False) # now it's off
        d.turn_on()
        self.assertEqual(d.on, True)  # now it's on again
        d.turn_off()
        self.assertEqual(d.on, False) # now it's off again
        d.toggle()
        self.assertEqual(d.on, True)  # now it's on again
    
    #---------------------------------------------------------------------------
    
    # tests each class's __eq__ definition in a separate test case.
    
    def test_eq_1(self):
        """ Device.__eq__  """
        dA = Device("a",50, True)
        dB = Device("b",100,False)
        self.assertEqual(dA==dB,False) # equality check should report False, because they have different field values.
        
        d1 = Device("a",50,False)
        d2 = Device("a",50,False)
        self.assertEqual(d1==d2,True) # different id()'s, but same field values. equal.

        d1 = Device("a",50,False)
        d2 = Device("a",50,True)
        self.assertEqual(d1==d2,False)
        d2.on = False
        self.assertEqual(d1==d2,True)
        d1.watts = 25
        self.assertEqual(d1==d2,False)
    
    def test_eq_2(self):
        """ Outlet.__eq__ """
        self.ensure_Device_eq() # we need Device.__eq__ to work.
        v1 = Outlet([])
        v2 = Outlet([])
        self.assertEqual(v1,v2)
        
        v1 = Outlet([Device("a",1,True),Device("b",2,False)])
        self.assertNotEqual(v1,v2)
        
        v2 = Outlet([Device("a",1,True),Device("b",2,False)])
        self.assertEqual(v1,v2)
    
    def test_eq_3(self):
        """ Circuit.__eq__ """
        self.ensure_Device_eq() # we need Device.__eq__ to work.
        c1 = Circuit([])
        c2 = Circuit([])
        self.assertEqual(c1,c2)
        
        c1 = Circuit([Outlet([Device("a",1,True),Device("b",2,False)])])
        self.assertNotEqual(c1,c2)
        
        c2 = Circuit([Outlet([Device("a",1,True),Device("b",2,False)])])
        self.assertEqual(c1,c2)
    
    #---------------------------------------------------------------------------
    
    def test_outlet_max_watts_1(self):
        """outlet max_watts, all on."""
        v1 = Outlet([])
        self.assertEqual(v1.max_watts(),0)
        v2 = Outlet([Device("five",5,True),Device("twenty",20,True),Device("thousand",1000,True)])
        self.assertEqual(v2.max_watts(),1025)
        
    def test_outlet_max_watts_2(self):
        """outlet max_watts, some on."""
        v1 = Outlet([Device("fan",200,True),Device("toothbrush",10,False)])
        self.assertEqual(v1.max_watts(),210)
        
        v2 = Outlet([Device("three",3,True),Device("twenty",20,False),Device("thousand",1000,True)])
        self.assertEqual(v2.max_watts(),1023)
    
    #---------------------------------------------------------------------------
    
    def test_outlet_watts_now_1(self):
        """outlet watts_now, all on."""
        v1 = Outlet([])
        self.assertEqual(v1.watts_now(),0)
        v2 = Outlet([Device("five",5,True),Device("twenty",20,True),Device("thousand",1000,True)])
        self.assertEqual(v2.watts_now(),1025)
    
    def test_outlet_watts_now_2(self):
        """outlet watts_now, some on."""
        v1 = Outlet([Device("fan",200,True),Device("toothbrush",10,False)])
        self.assertEqual(v1.watts_now(),200)
        
        v2 = Outlet([Device("three",3,True),Device("twenty",20,False),Device("thousand",1000,True)])
        self.assertEqual(v2.watts_now(),1003)
    
    #---------------------------------------------------------------------------
    
    def test_add_device_1(self):
        """Outlet add_device, starting empty"""
        self.ensure_Device_eq()
        v = Outlet([])
        self.assertEqual(v.devices,[])
        v.add_device(Device("a",1,True))
        self.assertEqual(v.devices,[Device("a",1,True)])
        
    def test_add_device_2(self):
        """Outlet add_device, starting non-empty"""
        self.ensure_Device_eq()
        v = Outlet([Device("a",1,True),Device("b",2,False)])
        self.assertEqual(v.devices,[Device("a",1,True),Device("b",2,False)])
        v.add_device(Device("c",3,True))
        self.assertEqual(v.devices,[Device("a",1,True),Device("b",2,False),Device("c",3,True)])
        
    def test_add_device_3(self):
        """Outlet add_device, multiple adds"""
        self.ensure_Device_eq()
        v = Outlet([])
        self.assertEqual(v.devices,[])
        v.add_device(Device("a",1,True))
        self.assertEqual(v.devices,[Device("a",1,True)])
        v.add_device(Device("b",2,False))
        self.assertEqual(v.devices,[Device("a",1,True),Device("b",2,False)])
        v.add_device(Device("c",3,True))
        self.assertEqual(v.devices,[Device("a",1,True),Device("b",2,False),Device("c",3,True)])
    
    #---------------------------------------------------------------------------
    
    def test_remove_device_1(self):
        """ Outlet.remove_device (item present) """
        ds = [Device("a",1,True),Device("b",2,False),Device("c",3,True)]
        out = Outlet(ds)
        out.remove_device("a")
        self.assertEqual(out.devices, [Device("b",2,False),Device("c",3,True)])
    
    def test_remove_device_2(self):
        """ Outlet.remove_device (item present, returned) """
        ds = [Device("a",1,True),Device("b",2,False),Device("c",3,True)]
        out = Outlet(ds)
        ans = out.remove_device("b")
        # did it return the value?
        self.assertEqual(ans, Device("b",2,False))
        self.assertEqual(out.devices,[Device("a",1,True),Device("c",3,True)])
    
    def test_remove_device_3(self):
        """ Outlet.remove_device (item NOT present) """
        ds = [Device("a",1,True),Device("b",2,False),Device("c",3,True)]
        out = Outlet(ds)
        ans = out.remove_device("d")
        self.assertEqual(ans,None)
        self.assertEqual(out.devices, ds)
    
    #---------------------------------------------------------------------------
    
    def test_outlet_turn_off_all_1(self):
        """ Outlet.turn_off_all (one device) """
        ds = [Device("a",1,True)]
        out = Outlet(ds)
        out.turn_off_all()
        self.assertEqual(out.devices[0].on,False)
        
    def test_outlet_turn_off_all_2(self):
        """ Outlet.turn_off_all (multiple devices) """
        ds = [Device("a",1,True),Device("b",2,False),Device("c",3,True)]
        out = Outlet(ds)
        out.turn_off_all()
        # a loop would be better code, but this may give easier error messages.
        self.assertEqual(out.devices[0].on,False)
        self.assertEqual(out.devices[1].on,False)
        self.assertEqual(out.devices[2].on,False)
        
    def test_outlet_turn_off_all_3(self):
        """ Outlet.turn_off_all (multiple devices, check id's) """
        ds = [Device("a",1,True),Device("b",2,False),Device("c",3,True)]
        id0 = id(ds[0])
        id1 = id(ds[1])
        id2 = id(ds[2])
        
        out = Outlet(ds)
        out.turn_off_all()
        # a loop would be better code, but this may give easier error messages.
        self.assertEqual(out.devices[0].on,False)
        self.assertEqual(out.devices[1].on,False)
        self.assertEqual(out.devices[2].on,False)
        # need to have the same id's (didn't regenerate the objects)
        self.assertEqual(id0,id(out.devices[0]))
        self.assertEqual(id1,id(out.devices[1]))
        self.assertEqual(id2,id(out.devices[2]))
    
    #---------------------------------------------------------------------------
    
    def test_add_outlet_1(self):
        """ Circuit.add_outlet (empty) """
        self.ensure_Device_eq()
        c = Circuit([])
        c.add_outlet(Outlet([Device("e",5,True)]))
        self.assertEqual(c.outlets,[Outlet([Device("e",5,True)])])
        
    def test_add_outlet_2(self):
        """ Circuit.add_outlet (add twice) """
        c = Circuit([])
        c.add_outlet(Outlet([]))
        self.assertEqual(c.outlets,[Outlet([])])
        c.add_outlet(Outlet([]))
        self.assertEqual(c.outlets,[Outlet([]), Outlet([])])
        
    def test_add_outlet_3(self):
        """ Circuit.add_outlet (starts non-empty) """
        self.ensure_Device_eq()
        c = Circuit([Outlet([Device("a",1,True)]), Outlet([Device("b",2,True),Device("c",3,True)])])
        c.add_outlet(Outlet([Device("e",5,True)]))
        self.assertEqual(c.outlets,[Outlet([Device("a",1,True)]), Outlet([Device("b",2,True),Device("c",3,True)]), Outlet([Device("e",5,True)])])
        
    
    #---------------------------------------------------------------------------
    
    def test_circuit_max_watts_1(self):
        """ circuit_max_watts (empty lists) """
        c1 = Circuit([])
        self.assertEqual(c1.max_watts(),0)
        c2 = Circuit([Outlet([]),Outlet([])])
        self.assertEqual(c2.max_watts(),0)
        
    def test_circuit_max_watts_2(self):
        """ circuit_max_watts (all on) """
        outs = [Outlet([Device("a",1,True)]),
                Outlet([Device("b",2,True),Device("c",3,True)]),
                Outlet([Device("e",5,True)])
               ]
        c = Circuit(outs)
        self.assertEqual(c.max_watts(),11)
        
    def test_circuit_max_watts_3(self):
        """ circuit_max_watts (some on, still add up all wattage) """
        outs = [Outlet([Device("a",1,False)]),
                Outlet([Device("b",2,True),Device("c",3,False)]),
                Outlet([Device("e",5,True)])
               ]
        c = Circuit(outs)
        self.assertEqual(c.max_watts(),11)
        
    
    #---------------------------------------------------------------------------
    
    def test_circuit_watts_now_1(self):
        """ circuit_watts_now (empty lists) """
        c1 = Circuit([])
        self.assertEqual(c1.watts_now(),0)
        c2 = Circuit([Outlet([]),Outlet([])])
        self.assertEqual(c2.watts_now(),0)
        
    def test_circuit_watts_now_2(self):
        """ circuit_watts_now (all on) """
        outs = [Outlet([Device("a",1,True)]),
                Outlet([Device("b",2,True),Device("c",3,True)]),
                Outlet([Device("e",5,True)])
               ]
        c = Circuit(outs)
        self.assertEqual(c.watts_now(),11)
        
    def test_circuit_watts_now_3(self):
        """ circuit_watts_now (some on, still add up all wattage) """
        outs = [Outlet([Device("a",1,False)]),
                Outlet([Device("b",2,True),Device("c",3,False)]),
                Outlet([Device("e",5,True)])
               ]
        c = Circuit(outs)
        self.assertEqual(c.watts_now(),7)
        
    
    #---------------------------------------------------------------------------
    
    def test_circuit_turn_off_all_1(self):
        """ Circuit.turn_off_all (all were on) """
        c = Circuit([Outlet([Device("a",1,True)]),Outlet([Device("b",2,True),Device("c",3,True)])])
        offs = [Outlet([Device("a",1,False)]),Outlet([Device("b",2,False),Device("c",3,False)])]
        c.turn_off_all()
        # compare to the answer stored above.
        self.assertEqual(c.outlets,offs)
    
    def test_circuit_turn_off_all_2(self):
        """ Circuit.turn_off_all (some were off) """
        c = Circuit([Outlet([Device("a",1,True)]),Outlet([Device("b",2,False),Device("c",3,True)])])
        offs = [Outlet([Device("a",1,False)]),Outlet([Device("b",2,False),Device("c",3,False)])]
        c.turn_off_all()
        # compare to the answer stored above.
        self.assertEqual(c.outlets,offs)
    
    ############################################################################

# This class digs through AllTests, counts and builds all the tests,
# so that we have an entire test suite that can be run as a group.
class TheTestSuite (unittest.TestSuite):
    # constructor.
    def __init__(self,wants):
        self.num_req = 0
        self.num_ec = 0
        # find all methods that begin with "test".
        fs = []
        for w in wants:
            for func in AllTests.__dict__:
                # append regular tests
                # drop any digits from the end of str(func).
                dropnum = str(func)
                while dropnum[-1] in "1234567890":
                    dropnum = dropnum[:-1]
                
                if dropnum==("test_"+w+"_") and (not (dropnum==("test_extra_credit_"+w+"_"))):
                    fs.append(AllTests(str(func)))
                if dropnum==("test_extra_credit_"+w+"_") and not BATCH_MODE:
                    fs.append(AllTests(str(func)))
        
#       print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
        # call parent class's constructor.
        unittest.TestSuite.__init__(self,fs)

class TheExtraCreditTestSuite (unittest.TestSuite):
        # constructor.
        def __init__(self,wants):
            # find all methods that begin with "test_extra_credit_".
            fs = []
            for w in wants:
                for func in AllTests.__dict__:
                    if str(func).startswith("test_extra_credit_"+w):
                        fs.append(AllTests(str(func)))
        
#           print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
            # call parent class's constructor.
            unittest.TestSuite.__init__(self,fs)

# all (non-directory) file names, regardless of folder depth,
# under the given directory 'dir'.
def files_list(dir):
    this_file = __file__
    if dir==".":
        dir = os.getcwd()
    info = os.walk(dir)
    filenames = []
    for (dirpath,dirnames,filez) in info:
#       print(dirpath,dirnames,filez)
        if dirpath==".":
            continue
        for file in filez:
            if file==this_file:
                continue
            filenames.append(os.path.join(dirpath,file))
#       print(dirpath,dirnames,filez,"\n")
    return filenames

def main():
    if len(sys.argv)<2:
        raise Exception("needed student's file name as command-line argument:"\
            +"\n\t\"python3 testerX.py gmason76_2xx_Px.py\"")
    
    if BATCH_MODE:
        print("BATCH MODE.\n")
        run_all()
        return
        
    else:
        want_all = len(sys.argv) <=2
        wants = []
        # remove batch_mode signifiers from want-candidates.
        want_candidates = sys.argv[2:]
        for i in range(len(want_candidates)-1,-1,-1):
            if want_candidates[i] in ['.'] or os.path.isdir(want_candidates[i]):
                del want_candidates[i]
    
        # set wants and extra_credits to either be the lists of things they want, or all of them when unspecified.
        wants = []
        extra_credits = []
        if not want_all:
            for w in want_candidates:
                if w in REQUIRED_DEFNS:
                    wants.append(w)
                elif w in SUB_DEFNS:
                    wants.append(w)
                elif w in EXTRA_CREDIT_DEFNS:
                    extra_credits.append(w)
                else:
                    raise Exception("asked to limit testing to unknown function '%s'."%w)
        else:
            wants = REQUIRED_DEFNS + SUB_DEFNS
            extra_credits = EXTRA_CREDIT_DEFNS
        
        # now that we have parsed the function names to test, run this one file.    
        run_one(wants,extra_credits)    
        return
    return # should be unreachable! 

# only used for non-batch mode, since it does the printing.
# it nicely prints less info when no extra credit was attempted.
def run_one(wants, extra_credits):
    
    has_reqs = len(wants)>0
    has_ec   = len(extra_credits)>0
    
    # make sure they exist.
    passed1 = 0
    passed2 = 0
    tried1 = 0
    tried2 = 0
    
    # only run tests if needed.
    if has_reqs:
        print("\nRunning required definitions:")
        (tag, passed1,tried1) = run_file(sys.argv[1],wants,False)
    if has_ec:
        print("\nRunning extra credit definitions:")
        (tag, passed2,tried2) = run_file(sys.argv[1],extra_credits,True)
    
    # print output based on what we ran.
    if has_reqs and not has_ec:
        print("\n%d/%d Required test cases passed (worth %.1f each)" % (passed1,tried1,weight_required) )
        print("\nScore based on test cases: %.2f/%d (%.2f*%.1f) " % (
                                                                passed1*weight_required, 
                                                                total_points_from_tests,
                                                                passed1,
                                                                weight_required
                                                             ))
    elif has_ec and not has_reqs:
        print("%d/%d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
    else: # has both, we assume.
        print("\n%d / %d Required test cases passed (worth %d each)" % (passed1,tried1,weight_required) )
        print("%d / %d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
        print("\nScore based on test cases: %.2f / %d ( %d * %d + %d * %d) " % (
                                                                passed1*weight_required+passed2*weight_extra_credit, 
                                                                total_points_from_tests,
                                                                passed1,
                                                                weight_required,
                                                                passed2,
                                                                weight_extra_credit
                                                             ))
    if CURRENTLY_GRADING:
        print("( %d %d %d %d )\n%s" % (passed1,tried1,passed2,tried2,tag))

# only used for batch mode.
def run_all():
        filenames = files_list(sys.argv[1])
        #print(filenames)
        
        wants = REQUIRED_DEFNS + SUB_DEFNS
        extra_credits = EXTRA_CREDIT_DEFNS
        
        results = []
        for filename in filenames:
            print(" Batching on : " +filename)
            # I'd like to use subprocess here, but I can't get it to give me the output when there's an error code returned... TODO for sure.
            lines = os.popen("python3 tester1p.py \""+filename+"\"").readlines()
            
            # delay of shame...
            time.sleep(DELAY_OF_SHAME)
            
            name = os.path.basename(lines[-1])
            stuff =lines[-2].split(" ")[1:-1]
            print("STUFF: ",stuff, "LINES: ", lines)
            (passed_req, tried_req, passed_ec, tried_ec) = stuff
            results.append((lines[-1],int(passed_req), int(tried_req), int(passed_ec), int(tried_ec)))
            continue
        
        print("\n\n\nGRAND RESULTS:\n")
        
            
        for (tag_req, passed_req, tried_req, passed_ec, tried_ec) in results:
            name = os.path.basename(tag_req).strip()
            earned   = passed_req*weight_required + passed_ec*weight_extra_credit
            possible = tried_req *weight_required # + tried_ec *weight_extra_credit
            print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
                                                            name,
                                                            earned,
                                                            possible, 
                                                            (earned/possible)*100,
                                                            passed_req,tried_req,weight_required,
                                                            passed_ec,tried_ec,weight_extra_credit
                                                          ))
# only used for batch mode.
def run_all_orig():
        filenames = files_list(sys.argv[1])
        #print(filenames)
        
        wants = REQUIRED_DEFNS + SUB_DEFNS
        extra_credits = EXTRA_CREDIT_DEFNS
        
        results = []
        for filename in filenames:
            # wipe out all definitions between users.
            for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS :
                globals()[fn] = decoy(fn)
                fn = decoy(fn)
            try:
                name = os.path.basename(filename)
                print("\n\n\nRUNNING: "+name)
                (tag_req, passed_req, tried_req) = run_file(filename,wants,False)
                (tag_ec,  passed_ec,  tried_ec ) = run_file(filename,extra_credits,True)
                results.append((tag_req,passed_req,tried_req,tag_ec,passed_ec,tried_ec))
                print(" ###### ", results)
            except SyntaxError as e:
                tag = filename+"_SYNTAX_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except NameError as e:
                tag =filename+"_Name_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except ValueError as e:
                tag = filename+"_VALUE_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except TypeError as e:
                tag = filename+"_TYPE_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except ImportError as e:
                tag = filename+"_IMPORT_ERROR_TRY_AGAIN"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except Exception as e:
                tag = filename+str(e.__reduce__()[0])
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
        
#           try:
#               print("\n |||||||||| scrupe: "+str(scruples))
#           except Exception as e:
#               print("NO SCRUPE.",e)
#           scruples = None
        
        print("\n\n\nGRAND RESULTS:\n")
        for (tag_req, passed_req, tried_req, tag_ec, passed_ec, tried_ec) in results:
            name = os.path.basename(tag_req)
            earned   = passed_req*weight_required + passed_ec*weight_extra_credit
            possible = tried_req *weight_required # + tried_ec *weight_extra_credit
            print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
                                                            name,
                                                            earned,
                                                            possible, 
                                                            (earned/possible)*100,
                                                            passed_req,tried_req,weight_required,
                                                            passed_ec,tried_ec,weight_extra_credit
                                                          ))

def try_copy(filename1, filename2, numTries):
    have_copy = False
    i = 0
    while (not have_copy) and (i < numTries):
        try:
            # move the student's code to a valid file.
            shutil.copy(filename1,filename2)
            
            # wait for file I/O to catch up...
            if(not wait_for_access(filename2, numTries)):
                return False
                
            have_copy = True
        except PermissionError:
            print("Trying to copy "+filename1+", may be locked...")
            i += 1
            time.sleep(1)
        except BaseException as e:
            print("\n\n\n\n\n\ntry-copy saw: "+e)
    
    if(i == numTries):
        return False
    return True

def try_remove(filename, numTries):
    removed = False
    i = 0
    while os.path.exists(filename) and (not removed) and (i < numTries):
        try:
            os.remove(filename)
            removed = True
        except OSError:
            print("Trying to remove "+filename+", may be locked...")
            i += 1
            time.sleep(1)
    if(i == numTries):
        return False
    return True

def wait_for_access(filename, numTries):
    i = 0
    while (not os.path.exists(filename) or not os.access(filename, os.R_OK)) and i < numTries:
        print("Waiting for access to "+filename+", may be locked...")
        time.sleep(1)
        i += 1
    if(i == numTries):
        return False
    return True

# this will group all the tests together, prepare them as 
# a test suite, and run them.
def run_file(filename,wants=None,checking_ec = False):
    if wants==None:
        wants = []
    
    # move the student's code to a valid file.
    if(not try_copy(filename,"student.py", 5)):
        print("Failed to copy " + filename + " to student.py.")
        quit()
        
    # import student's code, and *only* copy over the expected functions
    # for later use.
    import importlib
    count = 0
    while True:
        try:
#           print("\n\n\nbegin attempt:")
            while True:
                try:
                    f = open("student.py","a")
                    f.close()
                    break
                except:
                    pass
#           print ("\n\nSUCCESS!")
                
            import student
            importlib.reload(student)
            break
        except ImportError as e:
            print("import error getting student... trying again. "+os.getcwd(), os.path.exists("student.py"),e)
            time.sleep(0.5)
            while not os.path.exists("student.py"):
                time.sleep(0.5)
            count+=1
            if count>3:
                raise ImportError("too many attempts at importing!")
        except SyntaxError as e:
            print("SyntaxError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_SYNTAX_ERROR",None, None, None)
        except NameError as e:
            print("NameError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return((filename+"_Name_ERROR",0,1))    
        except ValueError as e:
            print("ValueError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_VALUE_ERROR",0,1)
        except TypeError as e:
            print("TypeError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_TYPE_ERROR",0,1)
        except ImportError as e:            
            print("ImportError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details or try again")
            return((filename+"_IMPORT_ERROR_TRY_AGAIN   ",0,1)) 
        except Exception as e:
            print("Exception in loading"+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+str(e.__reduce__()[0]),0,1)
    
    # make a global for each expected definition.
    for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS :
        globals()[fn] = decoy(fn)
        try:
            globals()[fn] = getattr(student,fn)
        except:
            if fn in wants:
                print("\nNO DEFINITION FOR '%s'." % fn) 
    
    if not checking_ec:
        # create an object that can run tests.
        runner = unittest.TextTestRunner()
    
        # define the suite of tests that should be run.
        suite = TheTestSuite(wants)
    
    
        # let the runner run the suite of tests.
        ans = runner.run(suite)
        num_errors   = len(ans.__dict__['errors'])
        num_failures = len(ans.__dict__['failures'])
        num_tests    = ans.__dict__['testsRun']
        num_passed   = num_tests - num_errors - num_failures
        # print(ans)
    
    else:
        # do the same for the extra credit.
        runner = unittest.TextTestRunner()
        suite = TheExtraCreditTestSuite(wants)
        ans = runner.run(suite)
        num_errors   = len(ans.__dict__['errors'])
        num_failures = len(ans.__dict__['failures'])
        num_tests    = ans.__dict__['testsRun']
        num_passed   = num_tests - num_errors - num_failures
        #print(ans)
    
    # remove our temporary file.
    os.remove("student.py")
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
    if(not try_remove("student.py", 5)):
        print("Failed to remove " + filename + " to student.py.")
    
    tag = ".".join(filename.split(".")[:-1])
    
    
    return (tag, num_passed, num_tests)


# make a global for each expected definition.
def decoy(name):
        # this can accept any kind/amount of args, and will print a helpful message.
        def failyfail(*args, **kwargs):
            return ("<no '%s' definition was found - missing, or typo perhaps?>" % name)
        return failyfail

# this determines if we were imported (not __main__) or not;
# when we are the one file being run, perform the tests! :)
if __name__ == "__main__":
    main()
