'''
This Module facilitates the handling of the AGS Data Format commonly adopted for storing and
transferring geological/geoenvironmental data. Detailed descritpion of the data format
can be found https://www.ags.org.uk/data-format/

The module is designed to retrieve the data easily using Pandas.
'''

__author__ = 'Dazhong Li'
__version__ = '1.0.0'
__email__  ='dazhong.li@arup.com'


import pandas as pd
import numpy as np
import codecs

class ags:
    '''
    The class facilitates the handling of the ags files commonly adopted for storing
    GI data. The class is designed to
    '''
    def __init__(self):
        self.n_ags_files = 0
        self.file_key_map={}
        self.n_files = 0

    def read(self,filename):
        key_map ={}
        with open(filename, 'r') as f:
            count = 0
            start_line =0
            for line_number, line in enumerate(f):
                if '**' in line:
                    if count ==0:
                        start_line = line_number
                        key = line.strip()[3:-1] # key words are in a form of "**Key"
                    else:
                        key_map[key] = (start_line,line_number)
                        start_line = line_number
                        key = line.strip()[3:-1]
                    count = count + 1
        self.file_key_map[filename] = key_map
        self.n_files = self.n_files + 1

