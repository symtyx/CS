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

############################################################################
############################################################################
# BEGIN SPECIALIZATION SECTION (the only part you need to modify beyond 
# adding new test cases).

# name all expected definitions; if present, their definition (with correct
# number of arguments) will be used; if not, a decoy complainer function
# will be used, and all tests on that function should fail.
    
REQUIRED_DEFNS = [  "extract_title",
                    "extract_organism",
                    "extract_sequences"
                 ]

# for method names in classes that will be tested. They have to be here
# so that we don't complain about missing global function definitions.
# Really, any chosen name for test batches can go here regardless of actual
# method names in the code.
SUB_DEFNS = []

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = []

# how many points are test cases worth?
weight_required     = 4
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
        
    ############################################################################
    
    def test_extract_title_1(self):
        self.assertEqual(extract_title('test_inputs/GenBank1.gb'),"Subtractive library of chicken spleen 36h post-infected NDV")
    def test_extract_title_2(self):
        self.assertEqual(extract_title('test_inputs/GenBank2.gb'),"Selection method for dogs suitable to guide dogs")
    def test_extract_title_3(self):
        self.assertEqual(extract_title('test_inputs/GenBank3.gb'),"Inference of the protokaryotypes of amniotes and tetrapods and the evolutionary processes of microchromosomes from comparative gene mapping")
    def test_extract_title_4(self):
        self.assertEqual(extract_title('test_inputs/GenBank4.gb'),"The long terminal repeat of feline endogenous RD-114 retroviral DNAs: analysis of transcription regulatory activity and nucleotide sequence")
    def test_extract_title_5(self):
        self.assertEqual(extract_title('test_inputs/GenBank5.gb'),"Small molecule inhibition of cGAS reduces interferon expression in primary macrophages from autoimmune mice")
    def test_extract_title_6(self):
        self.assertEqual(extract_title('test_inputs/GenBank6.gb'),"Expansion pattern of the evolutionary neocentromere of macaque chromosome 6")
    def test_extract_title_7(self):
        self.assertEqual(extract_title('test_inputs/GenBank7.gb'),"A whole-genome assembly of the domestic cow, Bos taurus")
    def test_extract_title_8(self):
        self.assertEqual(extract_title('test_inputs/GenBank8.gb'),"Anterior localization of maternal mRNAs preceded the evolution of bicoid")

    ############################################################################
    
    def test_extract_organism_1(self):
        self.assertEqual(extract_organism('test_inputs/GenBank1.gb'),['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Archelosauria', 'Archosauria', 'Dinosauria', 'Saurischia', 'Theropoda', 'Coelurosauria', 'Aves', 'Neognathae', 'Galloanserae', 'Galliformes', 'Phasianidae', 'Phasianinae', 'Gallus'])
    def test_extract_organism_2(self):
        self.assertEqual(extract_organism('test_inputs/GenBank2.gb'),['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Mammalia', 'Eutheria', 'Laurasiatheria', 'Carnivora', 'Caniformia', 'Canidae'])
    def test_extract_organism_3(self):
        self.assertEqual(extract_organism('test_inputs/GenBank3.gb'),['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Archelosauria', 'Archosauria', 'Crocodylia', 'Longirostres', 'Crocodylidae', 'Crocodylus'])
    def test_extract_organism_4(self):
        self.assertEqual(extract_organism('test_inputs/GenBank4.gb'),['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Mammalia', 'Eutheria', 'Laurasiatheria', 'Carnivora', 'Feliformia', 'Felidae', 'Felinae', 'Felis'])
    def test_extract_organism_5(self):
        self.assertEqual(extract_organism('test_inputs/GenBank5.gb'),['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Mammalia', 'Eutheria', 'Euarchontoglires', 'Glires', 'Rodentia', 'Myomorpha', 'Muroidea', 'Muridae', 'Murinae', 'Mus', 'Mus'])
    def test_extract_organism_6(self):
        self.assertEqual(extract_organism('test_inputs/GenBank6.gb'),['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Mammalia', 'Eutheria', 'Euarchontoglires', 'Primates', 'Haplorrhini', 'Catarrhini', 'Cercopithecidae', 'Cercopithecinae', 'Macaca'])
    def test_extract_organism_7(self):
        self.assertEqual(extract_organism('test_inputs/GenBank7.gb'),['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Mammalia', 'Eutheria', 'Laurasiatheria', 'Cetartiodactyla', 'Ruminantia', 'Pecora', 'Bovidae', 'Bovinae', 'Bos'])
    def test_extract_organism_8(self):
        self.assertEqual(extract_organism('test_inputs/GenBank8.gb'),['Eukaryota', 'Metazoa', 'Ecdysozoa', 'Arthropoda', 'Hexapoda', 'Insecta', 'Pterygota', 'Neoptera', 'Holometabola', 'Coleoptera', 'Polyphaga', 'Cucujiformia', 'Tenebrionidae', 'Tenebrionidae incertae sedis', 'Tribolium'])

    ############################################################################
    
    def test_extract_sequences_1(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank1.gb'),{1: ['acatccacgg', 'atgaaggaga', 'ggagaaatgt', 'ttcaaatcag', 'ttctaacacg', 'aaaaccaatt'], 61: ['ccaagaccaa', 'gttatgaaat', 'taccactaag', 'cagcagtgaa', 'agaactacat', 'attgaagtca'], 121: ['gataagaaag', 'caagctgaag', 'agcaagcact', 'gggcatcttt', 'cttgaaaaaa', 'gtaaggccca'], 181: ['agtaacagac', 'tatcagattt', 'ttttgcagtc', 'tttgcattcc', 'tactagatga', 'ttcacagaga'], 241: ['agatagtcac', 'atttatcatt', 'cgaaaacatg', 'aaagaattcc', 'agtcagaact', 'tgcatttggg'], 301: ['ggcatgtaag', 'tctcaaggtt', 'gtctttttgc', 'caatgtgctg', 'taacattatt', 'gcactcagag'], 361: ['tgtactgctg', 'acagccactg', 'ttctgccgaa', 'atgacagaaa', 'atagggaaca', 'agagtaagca'], 421: ['gtttcacttc', 'ttgtgcacaa', 'aatgtcaact', 'tagccgttat', 'cttatggcct', 'aagtgattag'], 481: ['cagaaataca', 'caatcatttc', 'tgagctgttt', 'actgtatctg', 'ccacagaggc', 'agctaaattc'], 541: ['ccaagctatc', 'tgaaatcatc', 'ctctgcttcc', 'gattctcagg', 'gttgcctgct', 'tatgctagaa'], 601: ['aggatgtttc', 'agtctctcac', 'agtgattttg', 'ctgccaattt', 'tttgttttat', 'cttctaactc'], 661: ['acttcccttt', 'aagtaatgtt', 'ctcttttacc', 'aggggggatg', 'aagtgatcag', 'gcacttttca'], 721: ['gtatgaagaa', 'accaccaatc', 'aaatatatgt', 'tgcataattt', 'aaacttgtgg', 'caagggagag'], 781: ['actaccagta', 'taattccatc', 'gtgttgttta', 'cccagtgt']})
    def test_extract_sequences_2(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank2.gb'),{1: ['atgcccaagc', 'aggtggaagt', 'acgaatgcac', 'gacagccatc', 'tcagctcaga', 'ggagccgaag'], 61: ['caccgacatc', 'taggcctgcg', 'tctgtgtgac', 'aagctgggga', 'agaacctcct', 'gctcacattg'], 121: ['actgtgttcg', 'gtgtcatcct', 'gggggcagta', 'tgtggagggc', 'ttcttcgctt', 'ggcatctcct'], 181: ['ctccaccccg', 'atgtggtcat', 'gttgatagcc', 'ttcccagggg', 'atatactcat', 'gaggatgcta'], 241: ['aaaatgctca', 'ttctccctct', 'catcatctcc', 'agcttaatca', 'cagggttgtc', 'gggcctggat'], 301: ['gctaaagcca', 'gtgggcgctt', 'aggcacaaga', 'gccatggtgt', 'attacatgtc', 'cacaaccata'], 361: ['attgccgcgg', 'tgttgggggt', 'catcctggtc', 'ttggctatcc', 'acccagggaa', 'ccccaaactc'], 421: ['aagaagcagc', 'tgggacctgg', 'gaagaagaat', 'gatgaagtgt', 'ccagcctgga', 'ygccttcctg'], 481: ['gatcttattc', 'gaaatctctt', 'tcctgaaaac', 'ctggtccaag', 'cctgttttca', 'acagattcaa'], 541: ['acggtgacca', 'agaaagtcct', 'ggtggctcct', 'ccatcagatg', 'aggacagcaa', 'tgccaccaat'], 601: ['gctgtcatct', 'ccttattgaa', 'cgagactgtg', 'acggaggccc', 'ctgaagaagt', 'gaaggtggtt'], 661: ['atcaagaagg', 'gcctggagtt', 'caaggatggc', 'atgaatgtct', 'taggtctgat', 'agggtttttc'], 721: ['attgcttttg', 'gcatcgccat', 'ggggaagatg', 'ggagagcagg', 'ccaagctgat', 'ggtggagttc'], 781: ['ttcaacattt', 'tgaatgagat', 'tgtaatgaag', 'ttagtgatca', 'tgatcatgtg', 'gtactctccc'], 841: ['ctgggtattg', 'cctgcctaat', 'ttgtggaaag', 'atcattgcaa', 'tcaaggactt', 'agaagtggtt'], 901: ['gctaggcaac', 'tggggatgta', 'catgatcacg', 'gtgattgtgg', 'gcctcatcat', 'ccatgggggc'], 961: ['atctttctcc', 'ccttgattta', 'ctttctagtc', 'accaggaaaa', 'accctttctc', 'ctttttcgct'], 1021: ['ggcattttcc', 'aagcttggat', 'cactgccctg', 'ggtaccgctt', 'ccagtgccgg', 'aactttgcct'], 1081: ['gtcactttcc', 'gttgcctgga', 'agaaaatctg', 'gggattgata', 'agcgcgtgac', 'cagatttgtc'], 1141: ['ctcccagtgg', 'gagcaaccat', 'caacatggac', 'ggcacagccc', 'tttatgaagc', 'agtggccgcc'], 1201: ['atctttattg', 'cccaaatgaa', 'cggtgttatc', 'ctggacggag', 'gccagattgt', 'gactgtgagc'], 1261: ['ctcacggcca', 'cgctggcgag', 'cgtcggtgcg', 'gccagtatcc', 'ccagcgcagg', 'cctcgtcacc'], 1321: ['atgctcctca', 'tcctgacggc', 'tgtgggcctg', 'ccaacggagg', 'acatcagcct', 'gctggtggct'], 1381: ['gtggactggc', 'tgctggacag', 'gatgagaact', 'tcagtcaatg', 'tggtggggga', 'ctcatttggg'], 1441: ['gctgggattg', 'tctatcacct', 'ctccaagtct', 'gagctggata', 'ctattgactc', 'ccagcatcga'], 1501: ['gtgcatgaag', 'atattgaaat', 'gaccaagact', 'cagtccattt', 'atgatgtgaa', 'gaaccttagg'], 1561: ['gaaagcaact', 'ctaatcaatg', 'tgtctatgcc', 'gcacacaact', 'ctgtcatagt', 'agatgagtgc'], 1621: ['aaggtaactc', 'tggcagccaa', 'cggaaagtca', 'gccgactgtg', 'gtgttgaaga', 'agaaccttgg'], 1681: ['aaacgtgaaa', 'aataa']})
    def test_extract_sequences_3(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank3.gb'),{1: ['tattttattc', 'tgataatcgg', 'ctgaatgtaa', 'cagaggaact', 'aacatctaat', 'aacaggacaa'], 61: ['gaattctgaa', 'tgtccagtcc', 'aggcttacag', 'atgccaaaca', 'cattagttgg', 'agagcagtgt'], 121: ['tgaacaacaa', 'caacctctat', 'attgaaattc', 'ccagtggtgc', 'tctgcctgaa', 'gggagcaaag'], 181: ['acagttttgc', 'agttctttta', 'gaatttgctg', 'aagaacagct', 'tcaagttgat', 'catgtcttca'], 241: ['tatgtttcca', 'caagaataga', 'gatgacagag', 'ctgcattact', 'ccgaactttc', 'agctttttgg'], 301: ['gctttgagat', 'tgtgagacca', 'gggcatcccc', 'ttgtccccaa', 'gagaccagat', 'gcttgcttca'], 361: ['tggcctacac', 'gtttgagaga', 'gactcttctg', 'aagaagaata', 'gattgcaatg', 'tttgcctctt'], 421: ['tagagctttc', 'ctgttgttta', 'tgaagatgaa', 'tatgtagaaa', 'ttttgtcaac', 'atcttttaca'], 481: ['atgcatagaa', 'ttgtttgtac', 'aaaatgttgt', 'gaccaactgc', 'ttgggcgggg', 'agatgttgaa'], 541: ['aatttcagac', 'ttcatcatct', 'tttctggatt', 'tgtgcgcatg', 'ttgtgattgt', 'gcaaataaat'], 601: ['gctcactcc']})
    def test_extract_sequences_4(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank4.gb'),{1: ['catgttatta', 'catggggcct', 'gccagtgaga', 'agtcagaacc', 'ccccaacctt', 'tgctaacata'], 61: ['aataaccgct', 'ttcatttcgc', 'ttctgtaaaa', 'ccgcttatgc', 'gccccaccct', 'aaccgctttc'], 121: ['atttcgcttc', 'tgtaaaaccg', 'cttatgcgcc', 'ccaccctagc', 'cggaaagtcc', 'ccagccgtac'], 181: ['gcaacccggg', 'ccccgagttg', 'catcagccgc', 'ttcgcaaccc', 'gggctccgag', 'ttgcatcagc'], 241: ['cgaaagaaac', 'ttcatttccc', 'aagcttcccc', 'gggacgaaat', 'tacccacaac', 'cccaaccacc'], 301: ['accgagcaga', 'gagcctatcg', 'ccagcctgta', 'tgcaaatgta', 'actcaaaatg', 'gtataaaaga'], 361: ['cctgtaaccc', 'cgtttatcgg', 'ggctctcccg', 'ctttctaaca', 'ctggggagcc', 'ctggtgcacc'], 421: ['agtaaagact', 'ctctgccgac', 'gtcggagtgc', 'cgcgtggttc', 'tttgcgccaa', 'ctctcattcc'], 481: ['atagggccta', 'ggagtttggc', 'tcctaacatt', 'tggtgcattg', 'gccgggaaac', 'cgagggaagg'], 541: ['caa']})
    def test_extract_sequences_5(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank5.gb'),{1: ['ngtcttcggc', 'aatt']})
    def test_extract_sequences_6(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank6.gb'),{1: ['tctccacgtg', 'atttttacat', 'gcataaaagg', 'acagtagttt', 'agaatagaaa', 'aggaatattt'], 61: ['ttatgcacct', 'tcagttgttt', 'tagtctaact', 'ccccttaaaa', 'tttccaacat', 'aattcacctt'], 121: ['cacatgaaac', 'tggataagat', 'gaaaatctga', 'attcacttta', 'aaagaaaaga', 'gtcaaaaagg'], 181: ['catttatgta', 'tttgattatt', 'aaattgaaaa', 'catcaaattc', 'tatctgtttg', 'ccatgttcat'], 241: ['ctg']})
    def test_extract_sequences_7(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank7.gb'),{1: ['atggctggag', 'gaaggaacag', 'tacgacaatc', 'acagagttta', 'tcctcttggg', 'gttctctgag'], 61: ['tttccacagc', 'tcaccgctgt', 'cctcttttca', 'atattcctag', 'ggatctacct', 'ggtgacagtg'], 121: ['tcttggaacc', 'tgggactcat', 'cgccgtcatc', 'aggatggact', 'cccgtttgca', 'cacgcctatg'], 181: ['tacttcttcc', 'tcagtaacct', 'gtccttgctg', 'gacacttgct', 'atatatccat', 'catagctcct'], 241: ['agaatgctct', 'cagacttctt', 'caggaagcat', 'aaactcatct', 'cctttacggg', 'gtgcatcatg'], 301: ['cagtacttct', 'tgttctctag', 'cctgggcctg', 'actgagtgca', 'gtctgctggc', 'ggccatggct'], 361: ['tatgatcgct', 'acgtcgccat', 'ttgcagtcct', 'ctgctctaca', 'cagccaccat', 'gtgcccctct'], 421: ['ctctgcgtgc', 'agatggtggc', 'aggatcttgt', 'gtaactggat', 'tccttggctc', 'gttcattcag'], 481: ['ttgtgtgcct', 'tacttcagct', 'ccacttctgt', 'ggaccaaaca', 'tcatcaacca', 'tttcttctgt'], 541: ['gacctgcccc', 'aactgctaac', 'cctatcctgc', 'tcggacacct', 'tgttctttca', 'agtcatgaca'], 601: ['tctgtgctca', 'cagtcatctt', 'tgggctcatg', 'tctgtcttgg', 'ttatcatgat', 'atcctatggt'], 661: ['tacattgtcg', 'ccaccattgt', 'gaagatcact', 'tcagctgaag', 'gccggtccaa', 'agccttcaac'], 721: ['acttgtgctt', 'ctcacctgac', 'agcagtgacc', 'ctcttctttg', 'gctcgggtat', 'ctttgtttat'], 781: ['atgtatccta', 'attctggcgg', 'ttcctcgagc', 'caaagcaagc', 'tggcatctgt', 'cttgtacact'], 841: ['gttataatcc', 'ccatgctaaa', 'tccattgatc', 'tatagcttga', 'ggaacaaaga', 'aatcaaagat'], 901: ['gccctaagca', 'tacggaagaa', 'gaaactcttt', 'tcctggtgtt']})
    def test_extract_sequences_8(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank8.gb'),{1: ['ggtgtagaga', 'agctgatcag', 'tacctgtgtg', 'tgcgacttac', 'ctactgctcg', 'ctgatgagat'], 61: ['gaatcgcgat', 'ctgtgaagtt', 'cggaatgttg', 'cgctgcccga', 'gccacatatc', 'cttacagaaa'], 121: ['gatgaaccag', 'ctgtgcaagg', 'tctgcggaga', 'gccagcggcc', 'ggattccact', 'ttggagcttt'], 181: ['tacctgcgag', 'ggatgcaagt', 'ccttcttcgg', 'tcgaacgtac', 'aacaatatca', 'gctcaatatc'], 241: ['ggaatgcaaa', 'aacaacggcg', 'aatgtgtgat', 'caacaaaaaa', 'aatcggacag', 'cttgcaaagc'], 301: ['atgccgctta', 'agaaagtgcc', 'ttttggtcgg', 'tatgtcgaaa', 'agtgggtctc', 'gttacggccg'], 361: ['ccgctccaac', 'tggttcaaga', 'tccactgcct', 'cctgcaggag', 'cagcagcagg', 'ccggcgccaa'], 421: ['catggcggcg', 'gcggctaacc', 'tcctgcgccc', 'gcacccctac', 'ctgtcgccgc', 'tcttccacag'], 481: ['cgccgccccc', 'aggacggcct', 'cccgcgagac', 'caagagctcg', 'gagtcggaca', 'gcggcgcctc'], 541: ['ctcggccgac', 'cccgacgacg', 'agctgcgctc', 'ctccagcgcc', 'ttcagctaca', 'tcaagccctc'], 601: ['cagcgagcgc', 'gactacttct', 'ccgtgaaaaa', 'actgccgtct', 'ccggcgagtg', 'atagtgagtg'], 661: ['cttcgataga', 'cggaaattta', 'ttagtgcatt', 'agtcaacgct', 'ccttccgtgt', 'ctccggcctc'], 721: ['tctgccctcg', 'atctccccca', 'gcggcggctt', 'cctgcccaag', 'tggctgccgc', 'cgctgcaggg'], 781: ['cttcagcgac', 'ccctcggcct', 'g']})
    def test_extract_sequences_9(self):
        self.assertEqual(extract_sequences('test_inputs/GenBank9.gb'),{1: ['ttaatttgca', 'tgttaacaaa', 'aaaaaaatgt', 'aactgacaaa', 'gaaaataaaa', 'agcaaaatat'], 61: ['tgaagtggac', 'aaaggtttaa', 'tatgttttat', 'gttagatata', 'gtacataaaa', 'ataagatttg'], 121: ['gcttatatca', 'tatgaataaa', 'tctgaacaaa', 'atttctagat', 'aaccgtacat', 'taacacgcta'], 181: ['aaaccatatc', 'ctaaaacttt', 'tgtttatttg', 'aaaacactaa', 'tttggttttt', 'ctataataat'], 241: ['tcttttgttt', 'tgtttttttc', 'ttgttcatct', 'cctttctctt', 'tcaattaccg', 'ttggaacaag'], 301: ['acgaagtttc', 'agagacaaca', 'ctacccaatc', 'tctctctcta', 'accttaagtg', 'ttgtctttct'], 361: ['ctctataagc', 'cagagaccag', 'acagtgatga', 'cgatatagta', 'tatgagacca', 'gagggaggat'], 421: ['taaccaccat', 'ttcccgtcat', 'gaatccagct', 'actgacccag', 'tctccgccgc', 'cgcagctgct'], 481: ['cttgctccgc', 'ctccacaacc', 'tccgcagcct', 'caccgtctct', 'ctacctcttg', 'caaccgtcac'], 541: ['ccagaagagc', 'ggttcaccgg', 'tttttgccct', 'tcttgtctct', 'gtgaacgtct', 'ctcagtctta'], 601: ['gatcagacca', 'acaatggcgg', 'ttcctcttct', 'tcctctaaaa', 'agcctccgac', 'catctctgct'], 661: ['gcggctctca', 'aggctctctt', 'taagccttcc', 'ggaaacaacg', 'gagtgggcgg', 'tgtaaataca'], 721: ['aacggaaacg', 'gccgggttaa', 'acccggattc', 'ttcccggagc', 'tccgtcgtac', 'gaaatctttc'], 781: ['tcagcatcca', 'agaacaacga', 'aggattctcc', 'ggcgtgtttg', 'agccacaacg', 'taggtcttgt'], 841: ['gacgtcaggc', 'ttcgaagctc', 'tctttggaac', 'ttgtttagcc', 'aagatgagca', 'acgaaacctt'], 901: ['ccaagcaatg', 'tcaccggcgg', 'tgagattgat', 'gtcgagccga', 'ggaaatcaag', 'cgttgcggag'], 961: ['cctgttctag', 'aggtaaacga', 'tgaaggagaa', 'gctgaaagtg', 'acgacgaaga', 'acttgaagag'], 1021: ['gaggaggagg', 'aagactacgt', 'tgaagctggc', 'gactttgaga', 'ttctcaatga', 'ttccggcgaa'], 1081: ['ctaatgaggg', 'aaaaaagcga', 'cgagattgtt', 'gaagttagag', 'aggagattga', 'agaagcggtg'], 1141: ['aaaccaacaa', 'agggtttaag', 'cgaagaggag', 'ttaaagccaa', 'taaaggatta', 'catagatctt'], 1201: ['gattctcaaa', 'ccaagaagcc', 'atcggtacga', 'cggagttttt', 'ggtcggcggc', 'ctctgttttc'], 1261: ['agcaagaagc', 'ttcagaaatg', 'gaggcagaat', 'caaaagatga', 'agaagcggcg', 'taacggcggc'], 1321: ['gaccatcggc', 'caggatcagc', 'tagattaccg', 'gtggagaaac', 'cgattgggag', 'acagctccgg'], 1381: ['gatactcaat', 'cggagattgc', 'tgattacgga', 'tatggtcgga', 'ggtcgtgcga', 'taccgaccct'], 1441: ['cgattctctc', 'tagacgccgg', 'aagattctct', 'cttgacgccg', 'gtagattctc', 'cgttgacatc'], 1501: ['ggtaggatct', 'cgcttgatga', 'tcctcgttat', 'tcgtttgacg', 'agccgagagc', 'ttcttgggac'], 1561: ['gggtctttga', 'ttggacggac', 'aatgtttcct', 'cccgccgcga', 'gagctcctcc', 'gccgccgtca'], 1621: ['atgctctcgg', 'tggtggagga', 'tgcgccgccg', 'ccggtgcacc', 'gtcacgtaac', 'ccgagcggat'], 1681: ['atgcagtttc', 'cggtggaaga', 'accggcgcca', 'ccaccaccgg', 'tggttaacca', 'aaccaacggt'], 1741: ['gtgtcagacc', 'cggttatcat', 'acccggcgga', 'tcaatccaaa', 'cccgagacta', 'ctatactgac'], 1801: ['tcatcgtcaa', 'ggaggcggaa', 'aagtctcgac', 'aggtctagta', 'gctccatgag', 'gaaaacggct'], 1861: ['gcagccgttg', 'tggcggatat', 'ggacgagcca', 'aagctttcag', 'tgtcgtcggc', 'tatatcaatt'], 1921: ['gacgcttact', 'caggatcact', 'gagagataac', 'aacaactacg', 'ccgtggagac', 'ggcagataac'], 1981: ['ggatctttcc', 'gggaaccggc', 'gatgatgatc', 'ggcgatagga', 'aagtgaatag', 'taacgataat'], 2041: ['aacaagaagt', 'cgagacggtg', 'ggggaagtgg', 'agcattttag', 'gacttattta', 'caggaagagt'], 2101: ['gttaacaagt', 'atgaggaaga', 'ggaggaggag', 'gaagaggata', 'ggtataggag', 'attaaacggt'], 2161: ['ggaatggtgg', 'agagatcgtt', 'atcggagtca', 'tggccggagc', 'tgaggaatgg', 'aggaggagga'], 2221: ['ggaggagggc', 'cgaggatggt', 'gaggagtaat', 'agcaatgtga', 'gctggaggag', 'ttccggaggt'], 2281: ['ggatcagcga', 'ggaaagtcaa', 'cggattggat', 'aggaggaata', 'agagttcaag', 'gtactcacct'], 2341: ['aagaatgggg', 'aaaacggaat', 'gttgaagttt', 'tacttgccac', 'atatgaaagc', 'tagtcggaga'], 2401: ['atgagcggta', 'caggaggagc', 'aggaggtggc', 'ggcggcggag', 'ggtgggcgaa', 'tagtcacggg'], 2461: ['cattctatag', 'cgaggagtgt', 'aatgaggctg', 'tattgatcaa', 'caaaattgtt', 'cattggatgg'], 2521: ['tttaattagc', 'tctatgaagc', 'tgaacctttg', 'tttttagtat', 'ttcgttggtt', 'taggtttaat'], 2581: ['ttcggttcaa', 'ttggtttact', 'ttgtaatgtt', 'aaggagggga', 'tgcattctca', 'aacgaatcac'], 2641: ['ttgttgtcgt', 'tgtctatttt', 'aaccggaata', 'aaccgccatt', 'cgaccagcta', 'tatttttggt'], 2701: ['tccaggcttc', 'ccaatcaaca', 'cctaaatttt', 'ttcca']})

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
