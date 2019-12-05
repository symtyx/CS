# Based on testing harness dated 2017-06-02.

# STUDENTS: TO USE:
# 
# The following command will test all test cases on your file:
#   
#   MAC:
#   python3 <thisfile.py> <your_one_file.py>
# 
#   PC:
#   python <thisfile.py> <your_one_file.py>
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

#import subprocess

import importlib
import random

#from test_inputs import *
#from test_outputs import *

############################################################################
############################################################################
# BEGIN SPECIALIZATION SECTION (the only part you need to modify beyond 
# adding new test cases).

# name all expected definitions; if present, their definition (with correct
# number of arguments) will be used; if not, a decoy complainer function
# will be used, and all tests on that function should fail.
    
REQUIRED_DEFNS = [  
                    'generate_durations',
                    'generate_frequencies',
                    'random_song',
                    'find_note',
                    'change_notes',
                    'song_as_dict'
                 ]

# for method names in classes that will be tested. They have to be here
# so that we don't complain about missing global function definitions.
# Really, any chosen name for test batches can go here regardless of actual
# method names in the code.
SUB_DEFNS = []

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = []

# how many points are test cases worth?
weight_required     = 1
weight_extra_credit = 1

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


import inspect # for enforcing usage of an operator or function
import ast     # for enforcing usage of an operator or function

# checks if a call to the function is present in the code. Of course it 
# might not actually be used in their solution...
def enforce_func_usage(func, funcname):
    dumptext = ast.dump(ast.parse(inspect.getsource(func).strip()))
    batches = dumptext.split("value=Call")
    for batch in batches:
        parts = batch.split("attr=")
        for part in parts:
            if part.startswith("'"+funcname+"'"):
                return
    raise Exception("You're required to call "+funcname+" in your solution.")


# END SPECIALIZATION SECTION

################################################################################
################################################################################
################################################################################

# enter batch mode by giving a directory to work on as the only argument.
BATCH_MODE = len(sys.argv)==2 and (sys.argv[1] in ["."] or os.path.isdir(sys.argv[1]))

# This class contains multiple "unit tests" that each check
# various inputs to specific functions, checking that we get
# the correct behavior (output value) from completing the call.
class AllTests (unittest.TestCase):

    ###########################################################################
    #                        helper methods for testing                       #
    ########################################################################### 

    def assertAlmostEqualsDict(self, first, second):

        for key in second:
            if first.get(key) == None:
                self.fail(f"Your dictionary is missing a key '{key}'")
        
        for key in first:
            if second.get(key) == None:
                self.fail(f"Your dictionary has an extra key '{key}'")
            
            self.assertAlmostEqual(first[key], second[key], delta=0.00001)

    def compare_files(self, f1name, f2name):
        with open(f1name) as f1:
            with open(f2name) as f2:
                self.assertEqual(f1.readlines(), f2.readlines())
        
    ###########################################################################
    #                         generate_durations tests                        #
    ########################################################################### 

    def test_generate_durations_01(self):
        self.assertAlmostEqualsDict(generate_durations(30), {'Whole': 8.0, 'Half': 4.0, 'Quarter': 2.0, 'Eighth': 1.0, 'Sixteenth': 0.5})

    def test_generate_durations_02(self):
        self.assertAlmostEqualsDict(generate_durations(60), {'Whole': 4.0, 'Half': 2.0, 'Quarter': 1.0, 'Eighth': 0.5, 'Sixteenth': 0.25})

    def test_generate_durations_03(self):
        self.assertAlmostEqualsDict(generate_durations(90), {'Whole': 2.6666666666666665, 'Half': 1.3333333333333333, 'Quarter': 0.6666666666666666, 'Eighth': 0.3333333333333333, 'Sixteenth': 0.16666666666666666})

    def test_generate_durations_04(self):
        self.assertAlmostEqualsDict(generate_durations(120), {'Whole': 2.0, 'Half': 1.0, 'Quarter': 0.5, 'Eighth': 0.25, 'Sixteenth': 0.125})

    def test_generate_durations_05(self):
        self.assertAlmostEqualsDict(generate_durations(240), {'Whole': 1.0, 'Half': 0.5, 'Quarter': 0.25, 'Eighth': 0.125, 'Sixteenth': 0.0625})
    ###########################################################################
    #                       generate_frequencies tests                        #
    ########################################################################### 
    def test_generate_frequencies_01(self):
        self.assertAlmostEqualsDict(generate_frequencies(100), {'A0': 6.25, 'A#0': 6.621644339745596, 'B0': 7.015387801933583, 'C1': 7.432544468767007, 'C#1': 7.874506561842957, 'D1': 8.342749088562716, 'D#1': 8.838834764831844, 'E1': 9.36441923047926, 'F1': 9.921256574801248, 'F#1': 10.511205190671431, 'G1': 11.136233976754243, 'G#1': 11.79842890852117, 'A1': 12.5, 'A#1': 13.243288679491192, 'B1': 14.030775603867166, 'C2': 14.865088937534013, 'C#2': 15.749013123685915, 'D2': 16.68549817712543, 'D#2': 17.67766952966369, 'E2': 18.72883846095852, 'F2': 19.842513149602496, 'F#2': 21.022410381342862, 'G2': 22.272467953508485, 'G#2': 23.59685781704234, 'A2': 25.0, 'A#2': 26.486577358982384, 'B2': 28.061551207734325, 'C3': 29.730177875068026, 'C#3': 31.49802624737183, 'D3': 33.370996354250856, 'D#3': 35.35533905932738, 'E3': 37.45767692191704, 'F3': 39.68502629920499, 'F#3': 42.044820762685724, 'G3': 44.54493590701697, 'G#3': 47.193715634084676, 'A3': 50.0, 'A#3': 52.97315471796477, 'B3': 56.12310241546865, 'C4': 59.46035575013605, 'C#4': 62.99605249474366, 'D4': 66.74199270850171, 'D#4': 70.71067811865476, 'E4': 74.91535384383408, 'F4': 79.37005259840998, 'F#4': 84.08964152537145, 'G4': 89.08987181403393, 'G#4': 94.38743126816935, 'A4': 100.0, 'A#4': 105.94630943592954, 'B4': 112.2462048309373, 'C5': 118.9207115002721, 'C#5': 125.99210498948732, 'D5': 133.48398541700342, 'D#5': 141.4213562373095, 'E5': 149.83070768766817, 'F5': 158.74010519681994, 'F#5': 168.1792830507429, 'G5': 178.17974362806785, 'G#5': 188.77486253633867, 'A5': 200.0, 'A#5': 211.89261887185907, 'B5': 224.49240966187455, 'C6': 237.8414230005442, 'C#6': 251.98420997897463, 'D6': 266.96797083400685, 'D#6': 282.842712474619, 'E6': 299.66141537533633, 'F6': 317.4802103936399, 'F#6': 336.3585661014858, 'G6': 356.3594872561357, 'G#6': 377.54972507267735, 'A6': 400.0, 'A#6': 423.785237743718, 'B6': 448.9848193237491, 'C7': 475.6828460010884, 'C#7': 503.9684199579492, 'D7': 533.9359416680137, 'D#7': 565.685424949238, 'E7': 599.3228307506726, 'F7': 634.9604207872798, 'F#7': 672.7171322029716, 'G7': 712.7189745122713, 'G#7': 755.0994501453547, 'A7': 800.0, 'A#7': 847.570475487436, 'B7': 897.9696386474982, 'C8': 951.3656920021768})
    def test_generate_frequencies_02(self):
        self.assertAlmostEqualsDict(generate_frequencies(220),  {'A0': 13.75, 'A#0': 14.56761754744031, 'B0': 15.433853164253883, 'C1': 16.351597831287414, 'C#1': 17.323914436054505, 'D1': 18.354047994837977, 'D#1': 19.445436482630058, 'E1': 20.601722307054374, 'F1': 21.826764464562746, 'F#1': 23.12465141947715, 'G1': 24.499714748859333, 'G#1': 25.956543598746574, 'A1': 27.5, 'A#1': 29.13523509488062, 'B1': 30.867706328507765, 'C2': 32.70319566257483, 'C#2': 34.64782887210901, 'D2': 36.708095989675954, 'D#2': 38.890872965260115, 'E2': 41.20344461410875, 'F2': 43.65352892912549, 'F#2': 46.2493028389543, 'G2': 48.999429497718666, 'G#2': 51.91308719749315, 'A2': 55.0, 'A#2': 58.27047018976124, 'B2': 61.735412657015516, 'C3': 65.40639132514966, 'C#3': 69.29565774421802, 'D3': 73.4161919793519, 'D#3': 77.78174593052023, 'E3': 82.4068892282175, 'F3': 87.30705785825097, 'F#3': 92.4986056779086, 'G3': 97.99885899543733, 'G#3': 103.82617439498628, 'A3': 110.0, 'A#3': 116.54094037952248, 'B3': 123.47082531403103, 'C4': 130.8127826502993, 'C#4': 138.59131548843604, 'D4': 146.8323839587038, 'D#4': 155.56349186104046, 'E4': 164.81377845643496, 'F4': 174.61411571650194, 'F#4': 184.9972113558172, 'G4': 195.99771799087463, 'G#4': 207.65234878997256, 'A4': 220.0, 'A#4': 233.08188075904496, 'B4': 246.94165062806206, 'C5': 261.6255653005986, 'C#5': 277.1826309768721, 'D5': 293.6647679174076, 'D#5': 311.1269837220809, 'E5': 329.6275569128699, 'F5': 349.2282314330039, 'F#5': 369.9944227116344, 'G5': 391.99543598174927, 'G#5': 415.3046975799451, 'A5': 440.0, 'A#5': 466.1637615180899, 'B5': 493.883301256124, 'C6': 523.2511306011972, 'C#6': 554.3652619537442, 'D6': 587.329535834815, 'D#6': 622.2539674441618, 'E6': 659.2551138257398, 'F6': 698.4564628660078, 'F#6': 739.9888454232688, 'G6': 783.9908719634985, 'G#6': 830.6093951598903, 'A6': 880.0, 'A#6': 932.3275230361796, 'B6': 987.766602512248, 'C7': 1046.5022612023945, 'C#7': 1108.7305239074883, 'D7': 1174.65907166963, 'D#7': 1244.5079348883237, 'E7': 1318.5102276514795, 'F7': 1396.9129257320155, 'F#7': 1479.9776908465376, 'G7': 1567.9817439269968, 'G#7': 1661.2187903197805, 'A7': 1760.0, 'A#7': 1864.6550460723593, 'B7': 1975.533205024496, 'C8': 2093.004522404789})
    def test_generate_frequencies_03(self):
        self.assertAlmostEqualsDict(generate_frequencies(440),  {'A0': 27.5, 'A#0': 29.13523509488062, 'B0': 30.867706328507765, 'C1': 32.70319566257483, 'C#1': 34.64782887210901, 'D1': 36.708095989675954, 'D#1': 38.890872965260115, 'E1': 41.20344461410875, 'F1': 43.65352892912549, 'F#1': 46.2493028389543, 'G1': 48.999429497718666, 'G#1': 51.91308719749315, 'A1': 55.0, 'A#1': 58.27047018976124, 'B1': 61.73541265701553, 'C2': 65.40639132514966, 'C#2': 69.29565774421802, 'D2': 73.41619197935191, 'D#2': 77.78174593052023, 'E2': 82.4068892282175, 'F2': 87.30705785825099, 'F#2': 92.4986056779086, 'G2': 97.99885899543733, 'G#2': 103.8261743949863, 'A2': 110.0, 'A#2': 116.54094037952248, 'B2': 123.47082531403103, 'C3': 130.8127826502993, 'C#3': 138.59131548843604, 'D3': 146.8323839587038, 'D#3': 155.56349186104046, 'E3': 164.813778456435, 'F3': 174.61411571650194, 'F#3': 184.9972113558172, 'G3': 195.99771799087466, 'G#3': 207.65234878997256, 'A3': 220.0, 'A#3': 233.08188075904496, 'B3': 246.94165062806206, 'C4': 261.6255653005986, 'C#4': 277.1826309768721, 'D4': 293.6647679174076, 'D#4': 311.1269837220809, 'E4': 329.6275569128699, 'F4': 349.2282314330039, 'F#4': 369.9944227116344, 'G4': 391.99543598174927, 'G#4': 415.3046975799451, 'A4': 440.0, 'A#4': 466.1637615180899, 'B4': 493.8833012561241, 'C5': 523.2511306011972, 'C#5': 554.3652619537442, 'D5': 587.3295358348151, 'D#5': 622.2539674441618, 'E5': 659.2551138257398, 'F5': 698.4564628660078, 'F#5': 739.9888454232688, 'G5': 783.9908719634985, 'G#5': 830.6093951598903, 'A5': 880.0, 'A#5': 932.3275230361799, 'B5': 987.766602512248, 'C6': 1046.5022612023945, 'C#6': 1108.7305239074883, 'D6': 1174.65907166963, 'D#6': 1244.5079348883237, 'E6': 1318.5102276514797, 'F6': 1396.9129257320155, 'F#6': 1479.9776908465376, 'G6': 1567.981743926997, 'G#6': 1661.2187903197805, 'A6': 1760.0, 'A#6': 1864.6550460723593, 'B6': 1975.533205024496, 'C7': 2093.004522404789, 'C#7': 2217.4610478149766, 'D7': 2349.31814333926, 'D#7': 2489.0158697766474, 'E7': 2637.020455302959, 'F7': 2793.825851464031, 'F#7': 2959.955381693075, 'G7': 3135.9634878539937, 'G#7': 3322.437580639561, 'A7': 3520.0, 'A#7': 3729.3100921447185, 'B7': 3951.066410048992, 'C8': 4186.009044809578})
    def test_generate_frequencies_04(self):
        self.assertAlmostEqualsDict(generate_frequencies(555),  {'A0': 34.6875, 'A#0': 36.75012608558806, 'B0': 38.93540230073138, 'C1': 41.250621801656884, 'C#1': 43.703511418228416, 'D1': 46.302257441523075, 'D#1': 49.05553294481674, 'E1': 51.972526729159895, 'F1': 55.06297399014693, 'F#1': 58.33718880822644, 'G1': 61.806098570986045, 'G#1': 65.4812804422925, 'A1': 69.375, 'A#1': 73.50025217117611, 'B1': 77.87080460146277, 'C2': 82.50124360331377, 'C#2': 87.40702283645683, 'D2': 92.60451488304615, 'D#2': 98.11106588963348, 'E2': 103.94505345831979, 'F2': 110.12594798029386, 'F#2': 116.67437761645289, 'G2': 123.61219714197209, 'G#2': 130.962560884585, 'A2': 138.75, 'A#2': 147.00050434235223, 'B2': 155.7416092029255, 'C3': 165.00248720662753, 'C#3': 174.81404567291366, 'D3': 185.20902976609227, 'D#3': 196.22213177926696, 'E3': 207.89010691663958, 'F3': 220.2518959605877, 'F#3': 233.34875523290577, 'G3': 247.22439428394418, 'G#3': 261.92512176916995, 'A3': 277.5, 'A#3': 294.00100868470446, 'B3': 311.483218405851, 'C4': 330.00497441325507, 'C#4': 349.62809134582733, 'D4': 370.41805953218454, 'D#4': 392.4442635585339, 'E4': 415.7802138332791, 'F4': 440.5037919211754, 'F#4': 466.69751046581155, 'G4': 494.4487885678883, 'G#4': 523.8502435383399, 'A4': 555.0, 'A#4': 588.0020173694089, 'B4': 622.966436811702, 'C5': 660.0099488265101, 'C#5': 699.2561826916547, 'D5': 740.8361190643691, 'D#5': 784.8885271170678, 'E5': 831.5604276665582, 'F5': 881.0075838423506, 'F#5': 933.3950209316231, 'G5': 988.8975771357766, 'G#5': 1047.7004870766798, 'A5': 1110.0, 'A#5': 1176.0040347388178, 'B5': 1245.9328736234038, 'C6': 1320.0198976530203, 'C#6': 1398.5123653833093, 'D6': 1481.672238128738, 'D#6': 1569.7770542341357, 'E6': 1663.1208553331164, 'F6': 1762.0151676847013, 'F#6': 1866.7900418632462, 'G6': 1977.7951542715532, 'G#6': 2095.4009741533596, 'A6': 2220.0, 'A#6': 2352.008069477635, 'B6': 2491.8657472468076, 'C7': 2640.0397953060406, 'C#7': 2797.024730766618, 'D7': 2963.344476257476, 'D#7': 3139.5541084682714, 'E7': 3326.2417106662324, 'F7': 3524.0303353694026, 'F#7': 3733.5800837264924, 'G7': 3955.590308543106, 'G#7': 4190.801948306719, 'A7': 4440.0, 'A#7': 4704.01613895527, 'B7': 4983.731494493615, 'C8': 5280.079590612081})
    def test_generate_frequencies_05(self):
        self.assertAlmostEqualsDict(generate_frequencies(880),  {'A0': 55.0, 'A#0': 58.27047018976124, 'B0': 61.73541265701553, 'C1': 65.40639132514966, 'C#1': 69.29565774421802, 'D1': 73.41619197935191, 'D#1': 77.78174593052023, 'E1': 82.4068892282175, 'F1': 87.30705785825099, 'F#1': 92.4986056779086, 'G1': 97.99885899543733, 'G#1': 103.8261743949863, 'A1': 110.0, 'A#1': 116.54094037952248, 'B1': 123.47082531403106, 'C2': 130.8127826502993, 'C#2': 138.59131548843604, 'D2': 146.83238395870382, 'D#2': 155.56349186104046, 'E2': 164.813778456435, 'F2': 174.61411571650197, 'F#2': 184.9972113558172, 'G2': 195.99771799087466, 'G#2': 207.6523487899726, 'A2': 220.0, 'A#2': 233.08188075904496, 'B2': 246.94165062806206, 'C3': 261.6255653005986, 'C#3': 277.1826309768721, 'D3': 293.6647679174076, 'D#3': 311.1269837220809, 'E3': 329.62755691287, 'F3': 349.2282314330039, 'F#3': 369.9944227116344, 'G3': 391.9954359817493, 'G#3': 415.3046975799451, 'A3': 440.0, 'A#3': 466.1637615180899, 'B3': 493.8833012561241, 'C4': 523.2511306011972, 'C#4': 554.3652619537442, 'D4': 587.3295358348151, 'D#4': 622.2539674441618, 'E4': 659.2551138257398, 'F4': 698.4564628660078, 'F#4': 739.9888454232688, 'G4': 783.9908719634985, 'G#4': 830.6093951598903, 'A4': 880.0, 'A#4': 932.3275230361799, 'B4': 987.7666025122483, 'C5': 1046.5022612023945, 'C#5': 1108.7305239074883, 'D5': 1174.6590716696303, 'D#5': 1244.5079348883237, 'E5': 1318.5102276514797, 'F5': 1396.9129257320155, 'F#5': 1479.9776908465376, 'G5': 1567.981743926997, 'G#5': 1661.2187903197805, 'A5': 1760.0, 'A#5': 1864.6550460723597, 'B5': 1975.533205024496, 'C6': 2093.004522404789, 'C#6': 2217.4610478149766, 'D6': 2349.31814333926, 'D#6': 2489.0158697766474, 'E6': 2637.0204553029594, 'F6': 2793.825851464031, 'F#6': 2959.955381693075, 'G6': 3135.963487853994, 'G#6': 3322.437580639561, 'A6': 3520.0, 'A#6': 3729.3100921447185, 'B6': 3951.066410048992, 'C7': 4186.009044809578, 'C#7': 4434.922095629953, 'D7': 4698.63628667852, 'D#7': 4978.031739553295, 'E7': 5274.040910605918, 'F7': 5587.651702928062, 'F#7': 5919.91076338615, 'G7': 6271.926975707987, 'G#7': 6644.875161279122, 'A7': 7040.0, 'A#7': 7458.620184289437, 'B7': 7902.132820097984, 'C8': 8372.018089619156})
    def test_generate_frequencies_06(self):
        self.assertAlmostEqualsDict(generate_frequencies(123),  {'A0': 7.6875, 'A#0': 8.144622537887082, 'B0': 8.628926996378306, 'C1': 9.142029696583418, 'C#1': 9.685643071066838, 'D1': 10.26158137893214, 'D#1': 10.871766760743169, 'E1': 11.51823565348949, 'F1': 12.203145587005537, 'F#1': 12.92878238452586, 'G1': 13.697567791407717, 'G#1': 14.51206755748104, 'A1': 15.375, 'A#1': 16.289245075774165, 'B1': 17.257853992756612, 'C2': 18.284059393166835, 'C#2': 19.371286142133677, 'D2': 20.52316275786428, 'D#2': 21.743533521486338, 'E2': 23.03647130697898, 'F2': 24.406291174011074, 'F#2': 25.85756476905172, 'G2': 27.395135582815435, 'G#2': 29.02413511496208, 'A2': 30.75, 'A#2': 32.57849015154833, 'B2': 34.51570798551322, 'C3': 36.56811878633367, 'C#3': 38.742572284267354, 'D3': 41.046325515728554, 'D#3': 43.487067042972676, 'E3': 46.07294261395796, 'F3': 48.81258234802214, 'F#3': 51.71512953810344, 'G3': 54.79027116563087, 'G#3': 58.04827022992415, 'A3': 61.5, 'A#3': 65.15698030309666, 'B3': 69.03141597102643, 'C4': 73.13623757266734, 'C#4': 77.48514456853471, 'D4': 82.09265103145711, 'D#4': 86.97413408594535, 'E4': 92.14588522791591, 'F4': 97.62516469604428, 'F#4': 103.43025907620688, 'G4': 109.58054233126173, 'G#4': 116.0965404598483, 'A4': 123.0, 'A#4': 130.31396060619332, 'B4': 138.06283194205287, 'C5': 146.27247514533468, 'C#5': 154.97028913706941, 'D5': 164.18530206291422, 'D#5': 173.9482681718907, 'E5': 184.29177045583182, 'F5': 195.25032939208853, 'F#5': 206.86051815241376, 'G5': 219.16108466252345, 'G#5': 232.19308091969657, 'A5': 246.0, 'A#5': 260.62792121238664, 'B5': 276.12566388410573, 'C6': 292.54495029066936, 'C#6': 309.94057827413883, 'D6': 328.3706041258284, 'D#6': 347.8965363437814, 'E6': 368.58354091166365, 'F6': 390.50065878417706, 'F#6': 413.7210363048275, 'G6': 438.3221693250469, 'G#6': 464.38616183939314, 'A6': 492.0, 'A#6': 521.2558424247732, 'B6': 552.2513277682115, 'C7': 585.0899005813387, 'C#7': 619.8811565482775, 'D7': 656.7412082516568, 'D#7': 695.7930726875628, 'E7': 737.1670818233272, 'F7': 781.0013175683541, 'F#7': 827.442072609655, 'G7': 876.6443386500937, 'G#7': 928.7723236787863, 'A7': 984.0, 'A#7': 1042.5116848495463, 'B7': 1104.502655536423, 'C8': 1170.1798011626774})
    def test_generate_frequencies_07(self):
        self.assertAlmostEqualsDict(generate_frequencies(456),  {'A0': 28.5, 'A#0': 30.194698189239915, 'B0': 31.990168376817138, 'C1': 33.89240277757755, 'C#1': 35.90774992200389, 'D1': 38.04293584384599, 'D#1': 40.305086527633215, 'E1': 42.70175169098543, 'F1': 45.24092998109369, 'F#1': 47.931095669461726, 'G1': 50.78122693399934, 'G#1': 53.800835822856534, 'A1': 57.0, 'A#1': 60.38939637847983, 'B1': 63.980336753634276, 'C2': 67.7848055551551, 'C#2': 71.81549984400777, 'D2': 76.08587168769198, 'D#2': 80.61017305526643, 'E2': 85.40350338197086, 'F2': 90.48185996218739, 'F#2': 95.86219133892345, 'G2': 101.56245386799868, 'G#2': 107.60167164571307, 'A2': 114.0, 'A#2': 120.77879275695966, 'B2': 127.96067350726852, 'C3': 135.5696111103102, 'C#3': 143.63099968801555, 'D3': 152.17174337538393, 'D#3': 161.22034611053286, 'E3': 170.80700676394173, 'F3': 180.96371992437474, 'F#3': 191.7243826778469, 'G3': 203.12490773599737, 'G#3': 215.20334329142614, 'A3': 228.0, 'A#3': 241.55758551391932, 'B3': 255.92134701453705, 'C4': 271.1392222206204, 'C#4': 287.2619993760311, 'D4': 304.34348675076785, 'D#4': 322.4406922210657, 'E4': 341.6140135278834, 'F4': 361.9274398487495, 'F#4': 383.4487653556938, 'G4': 406.24981547199474, 'G#4': 430.4066865828523, 'A4': 456.0, 'A#4': 483.11517102783864, 'B4': 511.8426940290741, 'C5': 542.2784444412408, 'C#5': 574.5239987520622, 'D5': 608.6869735015357, 'D#5': 644.8813844421314, 'E5': 683.2280270557668, 'F5': 723.8548796974989, 'F#5': 766.8975307113876, 'G5': 812.4996309439895, 'G#5': 860.8133731657044, 'A5': 912.0, 'A#5': 966.2303420556773, 'B5': 1023.685388058148, 'C6': 1084.5568888824816, 'C#6': 1149.0479975041244, 'D6': 1217.3739470030712, 'D#6': 1289.7627688842629, 'E6': 1366.4560541115336, 'F6': 1447.7097593949977, 'F#6': 1533.7950614227752, 'G6': 1624.999261887979, 'G#6': 1721.6267463314089, 'A6': 1824.0, 'A#6': 1932.4606841113543, 'B6': 2047.370776116296, 'C7': 2169.1137777649633, 'C#7': 2298.0959950082483, 'D7': 2434.7478940061424, 'D#7': 2579.5255377685257, 'E7': 2732.9121082230668, 'F7': 2895.4195187899954, 'F#7': 3067.5901228455505, 'G7': 3249.9985237759574, 'G#7': 3443.2534926628177, 'A7': 3648.0, 'A#7': 3864.9213682227087, 'B7': 4094.741552232592, 'C8': 4338.227555529927})
    def test_generate_frequencies_08(self):
        self.assertAlmostEqualsDict(generate_frequencies(789),  {'A0': 49.3125, 'A#0': 52.24477384059275, 'B0': 55.351409757255965, 'C1': 58.64277585857168, 'C#1': 62.12985677294093, 'D1': 65.82429030875983, 'D#1': 69.73840629452326, 'E1': 73.88526772848137, 'F1': 78.27871437518185, 'F#1': 82.93340895439759, 'G1': 87.86488607659098, 'G#1': 93.08960408823204, 'A1': 98.625, 'A#1': 104.4895476811855, 'B1': 110.70281951451193, 'C2': 117.28555171714336, 'C#2': 124.25971354588187, 'D2': 131.64858061751966, 'D#2': 139.47681258904652, 'E2': 147.77053545696273, 'F2': 156.5574287503637, 'F#2': 165.86681790879518, 'G2': 175.72977215318195, 'G#2': 186.17920817646407, 'A2': 197.25, 'A#2': 208.979095362371, 'B2': 221.40563902902383, 'C3': 234.57110343428673, 'C#3': 248.51942709176373, 'D3': 263.29716123503925, 'D#3': 278.95362517809303, 'E3': 295.54107091392547, 'F3': 313.1148575007274, 'F#3': 331.73363581759037, 'G3': 351.4595443063639, 'G#3': 372.3584163529281, 'A3': 394.5, 'A#3': 417.958190724742, 'B3': 442.81127805804766, 'C4': 469.14220686857345, 'C#4': 497.03885418352746, 'D4': 526.5943224700785, 'D#4': 557.9072503561861, 'E4': 591.0821418278508, 'F4': 626.2297150014548, 'F#4': 663.4672716351807, 'G4': 702.9190886127277, 'G#4': 744.7168327058562, 'A4': 789.0, 'A#4': 835.916381449484, 'B4': 885.6225561160953, 'C5': 938.2844137371469, 'C#5': 994.0777083670549, 'D5': 1053.188644940157, 'D#5': 1115.8145007123721, 'E5': 1182.1642836557016, 'F5': 1252.4594300029094, 'F#5': 1326.9345432703615, 'G5': 1405.8381772254554, 'G#5': 1489.4336654117121, 'A5': 1578.0, 'A#5': 1671.832762898968, 'B5': 1771.2451122321902, 'C6': 1876.5688274742938, 'C#6': 1988.1554167341098, 'D6': 2106.377289880314, 'D#6': 2231.6290014247443, 'E6': 2364.3285673114033, 'F6': 2504.9188600058187, 'F#6': 2653.869086540723, 'G6': 2811.676354450911, 'G#6': 2978.8673308234243, 'A6': 3156.0, 'A#6': 3343.6655257979355, 'B6': 3542.4902244643804, 'C7': 3753.1376549485876, 'C#7': 3976.3108334682192, 'D7': 4212.754579760628, 'D#7': 4463.258002849489, 'E7': 4728.657134622807, 'F7': 5009.837720011637, 'F#7': 5307.738173081446, 'G7': 5623.352708901821, 'G#7': 5957.7346616468485, 'A7': 6312.0, 'A#7': 6687.331051595871, 'B7': 7084.980448928761, 'C8': 7506.275309897175})
    def test_generate_frequencies_09(self):
        self.assertAlmostEqualsDict(generate_frequencies(1000),  {'A0': 62.5, 'A#0': 66.21644339745596, 'B0': 70.15387801933582, 'C1': 74.32544468767007, 'C#1': 78.74506561842958, 'D1': 83.42749088562717, 'D#1': 88.38834764831844, 'E1': 93.64419230479261, 'F1': 99.2125657480125, 'F#1': 105.11205190671431, 'G1': 111.36233976754242, 'G#1': 117.9842890852117, 'A1': 125.0, 'A#1': 132.43288679491192, 'B1': 140.30775603867164, 'C2': 148.65088937534014, 'C#2': 157.49013123685916, 'D2': 166.85498177125433, 'D#2': 176.7766952966369, 'E2': 187.28838460958522, 'F2': 198.425131496025, 'F#2': 210.22410381342863, 'G2': 222.72467953508485, 'G#2': 235.9685781704234, 'A2': 250.0, 'A#2': 264.86577358982385, 'B2': 280.6155120773433, 'C3': 297.3017787506803, 'C#3': 314.9802624737183, 'D3': 333.7099635425086, 'D#3': 353.5533905932738, 'E3': 374.57676921917044, 'F3': 396.8502629920499, 'F#3': 420.44820762685725, 'G3': 445.4493590701697, 'G#3': 471.93715634084674, 'A3': 500.0, 'A#3': 529.7315471796477, 'B3': 561.2310241546866, 'C4': 594.6035575013606, 'C#4': 629.9605249474366, 'D4': 667.4199270850172, 'D#4': 707.1067811865476, 'E4': 749.1535384383408, 'F4': 793.7005259840998, 'F#4': 840.8964152537145, 'G4': 890.8987181403393, 'G#4': 943.8743126816935, 'A4': 1000.0, 'A#4': 1059.4630943592954, 'B4': 1122.4620483093731, 'C5': 1189.2071150027211, 'C#5': 1259.9210498948732, 'D5': 1334.8398541700344, 'D#5': 1414.213562373095, 'E5': 1498.3070768766815, 'F5': 1587.4010519681995, 'F#5': 1681.792830507429, 'G5': 1781.7974362806785, 'G#5': 1887.7486253633867, 'A5': 2000.0, 'A#5': 2118.9261887185908, 'B5': 2244.924096618746, 'C6': 2378.4142300054423, 'C#6': 2519.8420997897465, 'D6': 2669.6797083400684, 'D#6': 2828.42712474619, 'E6': 2996.614153753363, 'F6': 3174.802103936399, 'F#6': 3363.585661014858, 'G6': 3563.594872561357, 'G#6': 3775.4972507267735, 'A6': 4000.0, 'A#6': 4237.852377437181, 'B6': 4489.848193237492, 'C7': 4756.828460010885, 'C#7': 5039.684199579492, 'D7': 5339.359416680137, 'D#7': 5656.85424949238, 'E7': 5993.228307506725, 'F7': 6349.604207872798, 'F#7': 6727.171322029716, 'G7': 7127.189745122713, 'G#7': 7550.994501453547, 'A7': 8000.0, 'A#7': 8475.704754874361, 'B7': 8979.696386474983, 'C8': 9513.65692002177})
    def test_generate_frequencies_10(self):
        self.assertAlmostEqualsDict(generate_frequencies(10000), {'A0': 625.0, 'A#0': 662.1644339745595, 'B0': 701.5387801933583, 'C1': 743.2544468767006, 'C#1': 787.4506561842958, 'D1': 834.2749088562716, 'D#1': 883.8834764831845, 'E1': 936.4419230479261, 'F1': 992.1256574801249, 'F#1': 1051.120519067143, 'G1': 1113.6233976754243, 'G#1': 1179.842890852117, 'A1': 1250.0, 'A#1': 1324.328867949119, 'B1': 1403.0775603867166, 'C2': 1486.5088937534013, 'C#2': 1574.9013123685916, 'D2': 1668.5498177125432, 'D#2': 1767.766952966369, 'E2': 1872.8838460958523, 'F2': 1984.2513149602498, 'F#2': 2102.241038134286, 'G2': 2227.2467953508485, 'G#2': 2359.685781704234, 'A2': 2500.0, 'A#2': 2648.657735898238, 'B2': 2806.1551207734324, 'C3': 2973.0177875068025, 'C#3': 3149.802624737183, 'D3': 3337.099635425086, 'D#3': 3535.533905932738, 'E3': 3745.7676921917046, 'F3': 3968.5026299204987, 'F#3': 4204.482076268572, 'G3': 4454.493590701697, 'G#3': 4719.371563408467, 'A3': 5000.0, 'A#3': 5297.315471796476, 'B3': 5612.310241546865, 'C4': 5946.035575013605, 'C#4': 6299.605249474366, 'D4': 6674.199270850172, 'D#4': 7071.067811865476, 'E4': 7491.535384383407, 'F4': 7937.0052598409975, 'F#4': 8408.964152537144, 'G4': 8908.987181403392, 'G#4': 9438.743126816935, 'A4': 10000.0, 'A#4': 10594.630943592952, 'B4': 11224.62048309373, 'C5': 11892.07115002721, 'C#5': 12599.210498948732, 'D5': 13348.398541700344, 'D#5': 14142.135623730952, 'E5': 14983.070768766815, 'F5': 15874.010519681993, 'F#5': 16817.92830507429, 'G5': 17817.974362806784, 'G#5': 18877.48625363387, 'A5': 20000.0, 'A#5': 21189.261887185905, 'B5': 22449.240966187455, 'C6': 23784.14230005442, 'C#6': 25198.420997897465, 'D6': 26696.797083400685, 'D#6': 28284.271247461904, 'E6': 29966.14153753363, 'F6': 31748.021039363986, 'F#6': 33635.85661014858, 'G6': 35635.94872561357, 'G#6': 37754.97250726774, 'A6': 40000.0, 'A#6': 42378.5237743718, 'B6': 44898.48193237491, 'C7': 47568.28460010884, 'C#7': 50396.841995794915, 'D7': 53393.59416680137, 'D#7': 56568.54249492381, 'E7': 59932.28307506725, 'F7': 63496.04207872797, 'F#7': 67271.71322029716, 'G7': 71271.89745122714, 'G#7': 75509.94501453548, 'A7': 80000.0, 'A#7': 84757.0475487436, 'B7': 89796.96386474982, 'C8': 95136.56920021768})





    ###########################################################################
    #                            change_notes tests                           #
    ########################################################################### 

    def test_change_notes_01(self):
        change_notes('p5_files/small.song',{},1)
        self.compare_files('p5_files/small_changed.song', 'p5_expected_results/small_changed1.song')
        os.remove('p5_files/small_changed.song')

    def test_change_notes_02(self):
        change_notes('p5_files/small.song',{},-1)
        self.compare_files('p5_files/small_changed.song', 'p5_expected_results/small_changed2.song')
        os.remove('p5_files/small_changed.song')

    def test_change_notes_03(self):
        change_notes('p5_files/small.song',{'A4':'B4',"B4":"A4"},10)
        self.compare_files('p5_files/small_changed.song', 'p5_expected_results/small_changed3.song')
        os.remove('p5_files/small_changed.song')

    def test_change_notes_04(self):
        change_notes('p5_files/medium.song',{},7)
        self.compare_files('p5_files/medium_changed.song', 'p5_expected_results/medium_changed1.song')
        os.remove('p5_files/medium_changed.song')  

    def test_change_notes_05(self):
        change_notes('p5_files/medium.song',{},-7)
        self.compare_files('p5_files/medium_changed.song', 'p5_expected_results/medium_changed2.song')
        os.remove('p5_files/medium_changed.song') 

    def test_change_notes_06(self):
        change_notes('p5_files/medium.song',{'G7':'G6','B2':'C#4'},15)
        self.compare_files('p5_files/medium_changed.song', 'p5_expected_results/medium_changed3.song')
        os.remove('p5_files/medium_changed.song') 

    def test_change_notes_07(self):
        change_notes('p5_files/large.song',{},4)
        self.compare_files('p5_files/large_changed.song', 'p5_expected_results/large_changed1.song')
        os.remove('p5_files/large_changed.song') 

    def test_change_notes_08(self):
        change_notes('p5_files/large.song',{},15)
        self.compare_files('p5_files/large_changed.song', 'p5_expected_results/large_changed2.song')
        os.remove('p5_files/large_changed.song') 

    def test_change_notes_09(self):
        change_notes('p5_files/large.song',{'C2':'E2','C8':"A0"},-20)
        self.compare_files('p5_files/large_changed.song', 'p5_expected_results/large_changed3.song')
        os.remove('p5_files/large_changed.song') 

    def test_change_notes_10(self):
        change_notes('p5_files/large.song',{'A0':'B1','B1':"C5","D#7":'C8'},-20)
        self.compare_files('p5_files/large_changed.song', 'p5_expected_results/large_changed4.song')
        os.remove('p5_files/large_changed.song') 

    def test_change_notes_11(self):
        change_notes('p5_files/huge.song',{'A0':'B1','B1':"C5","D#7":'C8'},-25)
        self.compare_files('p5_files/huge_changed.song', 'p5_expected_results/huge_changed1.song')
        os.remove('p5_files/huge_changed.song') 
    
    def test_change_notes_12(self):
        change_notes('p5_files/huge.song',{'C1':"A1","C2":"A2","C3":'A3',"C4":"A4",'C5':'A5','C6':'A6','C7':'A7'},25)
        self.compare_files('p5_files/huge_changed.song', 'p5_expected_results/huge_changed2.song')
        os.remove('p5_files/huge_changed.song') 
    
    def test_change_notes_13(self):
        change_notes('p5_files/huge.song',{'C1':"A1","C2":"A2","C3":'A3',"C4":"A4",'C5':'A5','C6':'A6','C7':'A7'},300)
        self.compare_files('p5_files/huge_changed.song', 'p5_expected_results/huge_changed3.song')
        os.remove('p5_files/huge_changed.song') 

    def test_change_notes_14(self):
        change_notes('p5_files/huge.song',{'C1':"A1","C2":"A2","C3":'A3',"C4":"A4",'C5':'A5','C6':'A6','C7':'A7'},-300)
        self.compare_files('p5_files/huge_changed.song', 'p5_expected_results/huge_changed4.song')
        os.remove('p5_files/huge_changed.song') 

    def test_change_notes_15(self):
        change_notes('p5_files/biggest.song',{},-12)
        self.compare_files('p5_files/biggest_changed.song', 'p5_expected_results/biggest_changed1.song')
        os.remove('p5_files/biggest_changed.song') 
    
    def test_change_notes_16(self):
        change_notes('p5_files/biggest.song',{},12)
        self.compare_files('p5_files/biggest_changed.song', 'p5_expected_results/biggest_changed2.song')
        os.remove('p5_files/biggest_changed.song') 
    
    def test_change_notes_17(self):
        change_notes('p5_files/biggest.song',{'G#4':'D#2','G#5':'F#7','G#6':'G#7'},-24)
        self.compare_files('p5_files/biggest_changed.song', 'p5_expected_results/biggest_changed3.song')
        os.remove('p5_files/biggest_changed.song') 

    def test_change_notes_18(self):
        change_notes('p5_files/biggest.song',{},24)
        self.compare_files('p5_files/biggest_changed.song', 'p5_expected_results/biggest_changed4.song')
        os.remove('p5_files/biggest_changed.song')   
    ###########################################################################
    #                            random_song tests                            #
    ########################################################################### 
    
    def test_random_song_1(self):
        random.seed(0)
        random_song('p5_outputs/student_random1.song',120,440,1)
        self.compare_files('p5_expected_results/random1.song','p5_outputs/student_random1.song')
        
    def test_random_song_2(self):
        random.seed(0)
        random_song('p5_outputs/student_random2.song',120,440,2)
        self.compare_files('p5_expected_results/random2.song','p5_outputs/student_random2.song')
        
    def test_random_song_3(self):
        random.seed(0)
        random_song('p5_outputs/student_random3.song',60,220,5)
        self.compare_files('p5_expected_results/random3.song','p5_outputs/student_random3.song')
        
    def test_random_song_4(self):
        random.seed(100)
        random_song('p5_outputs/student_random4.song',120,440,7)
        self.compare_files('p5_expected_results/random4.song','p5_outputs/student_random4.song')
        
    def test_random_song_5(self):
        random.seed(100)
        random_song('p5_outputs/student_random5.song',120,440,8)
        self.compare_files('p5_expected_results/random5.song','p5_outputs/student_random5.song')
        
    def test_random_song_6(self):
        random.seed(200)
        random_song('p5_outputs/student_random6.song',90,100,10)
        self.compare_files('p5_expected_results/random6.song','p5_outputs/student_random6.song')
        
    def test_random_song_7(self):
        random.seed(200)
        random_song('p5_outputs/student_random7.song',250,150,15)
        self.compare_files('p5_expected_results/random7.song','p5_outputs/student_random7.song')
        
    def test_random_song_8(self):
        random.seed(500)
        random_song('p5_outputs/student_random8.song',240,880,20)
        self.compare_files('p5_expected_results/random8.song','p5_outputs/student_random8.song')
        
    def test_random_song_9(self):
        random.seed(1000)
        random_song('p5_outputs/student_random9.song',90,440,25)
        self.compare_files('p5_expected_results/random9.song','p5_outputs/student_random9.song')

    def test_random_song_10(self):
        random.seed(1000)
        random_song('p5_outputs/student_random10.song',90,440,30)
        self.compare_files('p5_expected_results/random10.song','p5_outputs/student_random10.song')

    def test_random_song_11(self):
        random.seed(1234)
        random_song('p5_outputs/student_random11.song',90,440,35)
        self.compare_files('p5_expected_results/random11.song','p5_outputs/student_random11.song')

    def test_random_song_12(self):
        random.seed(1234)
        random_song('p5_outputs/student_random12.song',90,440,40)
        self.compare_files('p5_expected_results/random12.song','p5_outputs/student_random12.song')


    def test_random_song_13(self):
        random.seed(4321)
        random_song('p5_outputs/student_random13.song',90,440,45)
        self.compare_files('p5_expected_results/random13.song','p5_outputs/student_random13.song')

    def test_random_song_14(self):
        random.seed(4321)
        random_song('p5_outputs/student_random14.song',90,440,50)
        self.compare_files('p5_expected_results/random14.song','p5_outputs/student_random14.song')

    def test_random_song_15(self):
        random.seed(5000)
        random_song('p5_outputs/student_random15.song',90,440,100)
        self.compare_files('p5_expected_results/random15.song','p5_outputs/student_random15.song')


    ###########################################################################
    #                             find_note tests                             #
    ########################################################################### 
    def test_find_note_01(self): 
        self.assertEqual(find_note("p5_files/small.song", True), 'B4')
    
    def test_find_note_02(self): 
        self.assertEqual(find_note("p5_files/small.song", False), 'A4')
    
    def test_find_note_03(self): 
        self.assertEqual(find_note("p5_files/medium.song", True), 'G7')
    def test_find_note_04(self): 
        self.assertEqual(find_note("p5_files/medium.song", False), 'A1')

    def test_find_note_05(self): 
        self.assertEqual(find_note("p5_files/mediumsharp.song", True), 'G#7')
    
    def test_find_note_06(self): 
        self.assertEqual(find_note("p5_files/mediumsharp.song", False), 'A0')

    def test_find_note_07(self): 
        self.assertEqual(find_note("p5_files/large.song", True), 'B7')
    
    def test_find_note_08(self): 
        self.assertEqual(find_note("p5_files/large.song", False), 'C#1')

    def test_find_note_09(self): 
        self.assertEqual(find_note("p5_files/xtralarge.song", True), 'C8')
    
    def test_find_note_10(self): 
        self.assertEqual(find_note("p5_files/xtralarge.song", False), 'C1')
    
    def test_find_note_11(self): 
        self.assertEqual(find_note("p5_files/huge.song", True), 'B7')

    def test_find_note_12(self): 
        self.assertEqual(find_note("p5_files/huge.song", False), 'C1')
    
    ###########################################################################
    #                          song_as_dict tests                             #
    ########################################################################### 

    def test_song_as_dict_01(self):
        self.assertEqual(song_as_dict('p5_files/small.song'),{'tempo': 90, 'tuning': 440.0, 'notes': {'A': {4: 1}, 'B': {4: 1}}, 'types': {'Quarter': 2}})
    def test_song_as_dict_02(self):
        self.assertEqual(song_as_dict('p5_files/medium.song'), {'tempo': 120, 'tuning': 220.0, 'notes': {'A': {1: 1}, 'B': {2: 1}, 'C': {3: 1}, 'D': {4: 1}, 'E': {5: 1}, 'F': {6: 1}, 'G': {7: 1}}, 'types': {'Quarter': 2, 'Half': 2, 'Whole': 3}})
    
    def test_song_as_dict_03(self):
        self.assertEqual(song_as_dict('p5_files/mediumsharp.song'),{'tempo': 120, 'tuning': 220.0, 'notes': {'A': {0: 1}, 'B': {2: 1}, 'C#': {3: 1}, 'D#': {4: 1}, 'E': {5: 1}, 'F#': {6: 1}, 'G#': {7: 1}}, 'types': {'Quarter': 2, 'Half': 2, 'Whole': 3}})
    
    def test_song_as_dict_04(self):
        self.assertEqual(song_as_dict('p5_files/littlelamb.song'),{'tempo': 120, 'tuning': 440.0, 'notes': {'E': {4: 11}, 'D': {4: 10}, 'C': {4: 3}, 'G': {4: 2}}, 'types': {'Quarter': 22, 'Half': 4}})
    
    def test_song_as_dict_05(self):
        self.assertEqual(song_as_dict('p5_files/large.song'), {'tempo': 60, 'tuning': 440.0, 'notes': {'G': {4: 2, 5: 1, 6: 1}, 'C#': {1: 1, 5: 2, 4: 1, 7: 1}, 'D#': {1: 1, 2: 1, 6: 3, 7: 1}, 'F#': {2: 1, 6: 1, 1: 1, 3: 1}, 'A': {1: 1, 5: 1, 7: 1}, 'D': {2: 2, 7: 3, 6: 1, 4: 1, 5: 1}, 'G#': {3: 1, 5: 2}, 'B': {6: 2, 5: 2, 7: 1}, 'A#': {3: 1, 4: 2}, 'F': {6: 2, 5: 1, 7: 2}, 'E': {5: 1, 2: 1, 3: 1, 1: 1}, 'C': {2: 3, 3: 1}}, 'types': {'Half': 6, 'Sixteenth': 20, 'Eighth': 16, 'Quarter': 11, 'Whole': 1}})
    
    def test_song_as_dict_06(self):
        self.assertEqual(song_as_dict('p5_files/xtralarge.song'),{'tempo': 60, 'tuning': 440.0, 'notes': {'G#': {7: 3, 4: 1, 5: 2, 2: 2, 6: 1, 3: 1}, 'C': {5: 5, 3: 4, 7: 1, 6: 1, 1: 1, 8: 1, 4: 3}, 'F#': {4: 3, 7: 2, 3: 3, 6: 1, 5: 2, 1: 2}, 'A': {7: 2, 6: 1, 2: 5, 1: 2, 4: 1, 3: 1}, 'C#': {3: 2, 5: 3, 1: 1, 4: 1}, 'D': {6: 3, 3: 3, 7: 1, 2: 1, 5: 1}, 'B': {2: 1, 5: 1, 6: 1, 7: 2, 3: 2}, 'E': {3: 1, 5: 1, 6: 1, 1: 3, 4: 1, 2: 2}, 'A#': {1: 2, 7: 2, 6: 2, 5: 4, 2: 1, 3: 2}, 'F': {3: 2, 4: 3, 1: 3, 7: 3, 5: 1}, 'G': {2: 1, 6: 1, 7: 1, 1: 1}, 'D#': {1: 1, 5: 1, 2: 1, 6: 2}}, 'types': {'Whole': 4, 'Half': 19, 'Sixteenth': 44, 'Eighth': 30, 'Quarter': 20}})
    
    def test_song_as_dict_07(self):
        self.assertEqual(song_as_dict('p5_files/huge.song'), {'tempo': 120, 'tuning': 883.0, 'notes': {'F#': {1: 8, 6: 10, 7: 7, 2: 3, 5: 5, 4: 8, 3: 4}, 'G#': {4: 6, 6: 5, 1: 2, 3: 8, 7: 5, 5: 8, 2: 3}, 'G': {3: 6, 1: 4, 5: 3, 2: 4, 6: 6, 4: 5, 7: 3}, 'D#': {5: 5, 6: 8, 2: 7, 1: 5, 7: 3, 3: 3, 4: 5}, 'E': {2: 6, 1: 8, 6: 2, 3: 7, 4: 5, 7: 4, 5: 8}, 'A': {7: 5, 6: 6, 4: 5, 5: 3, 2: 10, 3: 4, 1: 10}, 'A#': {3: 8, 7: 6, 1: 9, 2: 4, 5: 6, 4: 5, 6: 9}, 'F': {4: 9, 5: 10, 6: 5, 1: 11, 7: 7, 3: 6, 2: 2}, 'B': {7: 7, 5: 6, 3: 4, 2: 6, 4: 6, 6: 7, 1: 2}, 'C#': {3: 4, 7: 7, 1: 6, 5: 10, 4: 11, 2: 2}, 'D': {1: 5, 3: 4, 6: 8, 4: 8, 2: 6, 5: 6, 7: 7}, 'C': {1: 8, 5: 7, 4: 6, 6: 2, 3: 10, 7: 5, 2: 3}}, 'types': {'Half': 63, 'Quarter': 94, 'Whole': 17, 'Eighth': 130, 'Sixteenth': 188}})
    
    def test_song_as_dict_08(self):
        self.assertEqual(song_as_dict('p5_files/rand1.song'), {'tempo': 120, 'tuning': 440.0, 'notes': {'F#': {1: 4, 6: 6, 7: 4, 2: 1, 5: 2, 4: 3}, 'G#': {4: 4, 6: 4, 1: 1, 3: 4, 7: 2, 5: 4, 2: 1}, 'G': {3: 5, 1: 3, 5: 2, 2: 2, 6: 2, 4: 3, 7: 2}, 'D#': {5: 3, 6: 3, 2: 3, 1: 3, 7: 2, 3: 2, 4: 3}, 'E': {2: 3, 1: 4, 6: 1, 3: 4, 4: 4, 7: 4, 5: 5}, 'A': {7: 1, 6: 4, 4: 4, 5: 1, 2: 4, 3: 1, 1: 5}, 'A#': {3: 5, 7: 4, 1: 5, 2: 2, 5: 2, 4: 2, 6: 4}, 'F': {4: 5, 5: 6, 6: 3, 1: 6, 7: 1, 3: 2}, 'B': {7: 4, 5: 3, 3: 2, 2: 3, 4: 5, 6: 3, 1: 2}, 'C#': {3: 2, 7: 5, 1: 2, 5: 5, 4: 7, 2: 2}, 'D': {1: 4, 3: 1, 6: 3, 4: 5, 2: 2, 5: 2, 7: 3}, 'C': {1: 5, 5: 2, 4: 3, 6: 1, 3: 4, 7: 3}}, 'types': {'Half': 28, 'Quarter': 47, 'Whole': 10, 'Eighth': 60, 'Sixteenth': 108}})    
    
    def test_song_as_dict_09(self):
        self.assertEqual(song_as_dict('p5_files/rand2.song'), {'tempo': 120, 'tuning': 440.0, 'notes': {'A#': {6: 5, 1: 4, 2: 2, 3: 3, 4: 3, 7: 2, 5: 4}, 'B': {2: 3, 6: 4, 4: 1, 5: 3, 7: 3, 3: 2}, 'A': {3: 3, 6: 2, 1: 5, 5: 2, 7: 4, 2: 6, 4: 1}, 'C#': {4: 4, 7: 2, 1: 4, 5: 5, 3: 2}, 'F#': {2: 2, 6: 4, 7: 3, 1: 4, 5: 3, 3: 4, 4: 5}, 'D': {4: 3, 2: 4, 7: 4, 6: 5, 5: 4, 3: 3, 1: 1}, 'G#': {3: 4, 1: 1, 5: 4, 7: 3, 4: 2, 2: 2, 6: 1}, 'D#': {2: 4, 4: 2, 5: 2, 3: 1, 1: 2, 6: 5, 7: 1}, 'F': {7: 6, 4: 4, 1: 5, 3: 4, 6: 2, 5: 4, 2: 2}, 'C': {1: 3, 3: 6, 7: 2, 2: 3, 5: 5, 6: 1, 4: 3}, 'G': {2: 2, 3: 1, 6: 4, 4: 2, 5: 1, 7: 1, 1: 1}, 'E': {5: 3, 2: 3, 3: 3, 1: 4, 6: 1, 4: 1}}, 'types': {'Quarter': 47, 'Eighth': 70, 'Half': 35, 'Sixteenth': 80, 'Whole': 7}})
    
    def test_song_as_dict_10(self):
        self.assertEqual(song_as_dict('p5_files/biggest.song'), {'tempo': 200, 'tuning': 200.0, 'notes': {'F#': {1: 12, 6: 14, 7: 12, 2: 10, 5: 9, 4: 14, 3: 9}, 'G#': {4: 15, 6: 13, 1: 13, 3: 10, 7: 10, 5: 11, 2: 12}, 'G': {3: 11, 1: 9, 5: 7, 2: 8, 6: 12, 4: 9, 7: 6}, 'D#': {5: 9, 6: 12, 2: 11, 1: 8, 7: 9, 3: 9, 4: 16}, 'E': {2: 10, 1: 13, 6: 6, 3: 12, 4: 13, 7: 12, 5: 17}, 'A': {7: 13, 6: 11, 4: 10, 5: 7, 2: 15, 3: 11, 1: 11}, 'A#': {3: 14, 7: 12, 1: 13, 2: 9, 5: 10, 4: 10, 6: 15}, 'F': {4: 11, 5: 16, 6: 9, 1: 14, 7: 13, 3: 10, 2: 11}, 'B': {7: 15, 5: 13, 3: 8, 2: 8, 4: 15, 6: 13, 1: 5}, 'C#': {3: 9, 7: 10, 1: 7, 5: 21, 4: 19, 2: 5, 6: 6}, 'D': {1: 8, 3: 9, 6: 14, 4: 15, 2: 13, 5: 10, 7: 11}, 'C': {1: 13, 5: 13, 4: 13, 6: 7, 3: 12, 7: 12, 2: 12}}, 'types': {'Half': 121, 'Quarter': 181, 'Whole': 40, 'Eighth': 266, 'Sixteenth': 336}})
    
    def test_song_as_dict_11(self):
        self.assertEqual(song_as_dict('p5_expected_results/huge_changed1.song'), {'tempo': 120, 'tuning': 883.0, 'notes': {'F#': {1: 14, 3: 3, 4: 6, 2: 8, 5: 3}, 'G': {2: 10, 4: 5, 1: 12, 5: 5, 3: 8}, 'D': {3: 5, 4: 8, 1: 8, 2: 11}, 'E': {2: 15, 1: 14, 3: 10, 4: 5, 5: 7}, 'G#': {5: 5, 4: 6, 1: 6, 2: 8, 3: 3}, 'A': {1: 18, 2: 15, 5: 6, 0: 4, 3: 6, 4: 9}, 'A#': {5: 7, 3: 6, 1: 13, 0: 6, 2: 6, 4: 7}, 'C': {1: 12, 5: 9, 3: 10, 8: 3, 2: 14}, 'D#': {2: 12, 1: 12, 4: 2, 5: 4, 3: 8}, 'C#': {1: 10, 4: 8, 2: 10, 3: 6, 5: 7}, 'B': {2: 7, 1: 6, 3: 2, 0: 10, 4: 5}, 'F': {4: 10, 5: 7, 1: 15, 3: 5, 2: 10}}, 'types': {'Half': 63, 'Quarter': 94, 'Whole': 17, 'Eighth': 130, 'Sixteenth': 188}})

    def test_song_as_dict_12(self):
        self.assertEqual(song_as_dict('p5_expected_results/biggest_changed1.song'), {'tempo': 200, 'tuning': 200.0, 'notes': {'F#': {1: 22, 5: 14, 6: 12, 4: 9, 3: 14, 2: 9}, 'G#': {3: 15, 5: 13, 1: 25, 2: 10, 6: 10, 4: 11}, 'G': {2: 11, 1: 17, 4: 7, 5: 12, 3: 9, 6: 6}, 'D#': {4: 9, 5: 12, 1: 19, 6: 9, 2: 9, 3: 16}, 'E': {1: 23, 5: 6, 2: 12, 3: 13, 6: 12, 4: 17}, 'A': {6: 13, 5: 11, 3: 10, 4: 7, 1: 15, 2: 11, 0: 11}, 'A#': {2: 14, 6: 12, 0: 13, 1: 9, 4: 10, 3: 10, 5: 15}, 'F': {3: 11, 4: 16, 5: 9, 1: 25, 6: 13, 2: 10}, 'B': {6: 15, 4: 13, 2: 8, 1: 8, 3: 15, 5: 13, 0: 5}, 'C#': {2: 9, 6: 10, 1: 12, 4: 21, 3: 19, 5: 6}, 'D': {1: 21, 2: 9, 5: 14, 3: 15, 4: 10, 6: 11}, 'C': {1: 25, 4: 13, 3: 13, 5: 7, 2: 12, 6: 12}}, 'types': {'Half': 121, 'Quarter': 181, 'Whole': 40, 'Eighth': 266, 'Sixteenth': 336}})

    def test_song_as_dict_13(self):
        self.assertEqual(song_as_dict('p5_expected_results/biggest_changed2.song'), {'tempo': 200, 'tuning': 200.0, 'notes': {'F#': {2: 12, 7: 26, 3: 10, 6: 9, 5: 14, 4: 9}, 'G#': {5: 15, 7: 23, 2: 13, 4: 10, 6: 11, 3: 12}, 'G': {4: 11, 2: 9, 6: 7, 3: 8, 7: 18, 5: 9}, 'D#': {6: 9, 7: 21, 3: 11, 2: 8, 4: 9, 5: 16}, 'E': {3: 10, 2: 13, 7: 18, 4: 12, 5: 13, 6: 17}, 'A': {7: 24, 5: 10, 6: 7, 3: 15, 4: 11, 2: 11}, 'A#': {4: 14, 7: 27, 2: 13, 3: 9, 6: 10, 5: 10}, 'F': {5: 11, 6: 16, 7: 22, 2: 14, 4: 10, 3: 11}, 'B': {7: 28, 6: 13, 4: 8, 3: 8, 5: 15, 2: 5}, 'C#': {4: 9, 7: 16, 2: 7, 6: 21, 5: 19, 3: 5}, 'D': {2: 8, 4: 9, 7: 25, 5: 15, 3: 13, 6: 10}, 'C': {2: 13, 6: 13, 5: 13, 7: 7, 4: 12, 8: 12, 3: 12}}, 'types': {'Half': 121, 'Quarter': 181, 'Whole': 40, 'Eighth': 266, 'Sixteenth': 336}})

    def test_song_as_dict_14(self):
        self.assertEqual(song_as_dict('p5_expected_results/biggest_changed3.song'), {'tempo': 200, 'tuning': 200.0, 'notes': {'F#': {1: 21, 4: 14, 5: 12, 7: 11, 2: 24, 3: 9}, 'D#': {2: 42, 3: 9, 4: 12, 1: 17, 5: 9}, 'G': {1: 20, 3: 7, 2: 17, 4: 12, 5: 6}, 'E': {2: 23, 1: 25, 4: 6, 5: 12, 3: 17}, 'A': {5: 13, 4: 11, 2: 10, 3: 7, 0: 15, 1: 22}, 'G#': {7: 13, 1: 23, 5: 10, 2: 12}, 'A#': {1: 27, 5: 12, 0: 9, 3: 10, 2: 10, 4: 15}, 'F': {2: 22, 3: 16, 4: 9, 1: 24, 5: 13}, 'B': {5: 15, 3: 13, 1: 13, 0: 8, 2: 15, 4: 13}, 'C#': {1: 16, 5: 10, 3: 21, 2: 24, 4: 6}, 'D': {1: 17, 4: 14, 2: 28, 3: 10, 5: 11}, 'C': {1: 25, 3: 13, 2: 25, 4: 7, 5: 12}}, 'types': {'Half': 121, 'Quarter': 181, 'Whole': 40, 'Eighth': 266, 'Sixteenth': 336}})

    def test_song_as_dict_15(self):
        self.assertEqual(song_as_dict('p5_expected_results/biggest_changed4.song'), {'tempo': 200, 'tuning': 200.0, 'notes': {'F#': {3: 12, 6: 28, 7: 21, 4: 10, 5: 9}, 'G#': {6: 28, 3: 13, 5: 10, 7: 21, 4: 12}, 'G': {5: 11, 3: 9, 7: 13, 4: 8, 6: 21}, 'D#': {7: 18, 6: 28, 4: 11, 3: 8, 5: 9}, 'E': {4: 10, 3: 13, 6: 19, 5: 12, 7: 29}, 'A': {7: 20, 6: 21, 4: 15, 5: 11, 3: 11}, 'A#': {5: 14, 7: 22, 3: 13, 4: 9, 6: 25}, 'F': {6: 20, 7: 29, 3: 14, 5: 10, 4: 11}, 'B': {7: 28, 5: 8, 4: 8, 6: 28, 3: 5}, 'C#': {5: 9, 7: 31, 3: 7, 6: 25, 4: 5}, 'D': {3: 8, 5: 9, 6: 29, 4: 13, 7: 21}, 'C': {3: 13, 7: 25, 6: 13, 8: 7, 5: 12, 4: 12}}, 'types': {'Half': 121, 'Quarter': 181, 'Whole': 40, 'Eighth': 266, 'Sixteenth': 336}})
     

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
    
        # set wants and extra_credits to either be the lists of s they want, or all of them when unspecified.
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
        print("\n%d/%d Required test cases passed (worth %d each)" % (passed1,tried1,weight_required) )
        print("\nScore based on test cases: %.2f/%d (%.2f*%d) " % (
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
        print("\nScore based on test cases: %.2f / %d ( %d * %.2f + %d * %.2f) " % (
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
