__author__ = 'Dazhong Li'
__version__ = '1.0'

import os
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt

#plaxis related module

import imp
path =
found_module = imp.find_module('plxscripting', [path])
plx = imp.load_module('plxscripting', *found_module)


class input:
    pass

class output:

    def __init__(self,path,port):
        '''
        This function initialize the plaxis remote with path and port
        Parameter:
            path - path to where plaxis is installed, e.g. 'C:\Program Files\Plaxis\PLAXIS 2D'
            port - port number to be fitt in
        return:
        '''
        found_module = imp.find_module('plxscripting', [path])
        plx = imp.load_module('plxscripting', *found_module)
        self.s_o = plx.easy.new_server('localhost', port)[0]
        self.g_o = plx.easy.new_server('localhost', port)[1]

    def get_result_epwp(self,Phase):
        '''
        This function return the excess pore water perssure at a certain phase
        Parameter:
        g_o: Plaxis output object
        Phase: Phase of interested,example 'g_o.Phase_6'
        '''
        g_o = self.g_o
        Phase = self._get_phase_by_name(Phase)
        x = np.array(g_o.getresults(Phase, g_o.ResultTypes.Soil.X, "node"))
        y = np.array(g_o.getresults(Phase, g_o.ResultTypes.Soil.Y, "node"))
        epwp =np.array(g_o.getresults(Phase, g_o.ResultTypes.Soil.PExcess, "node"))
        df = pd.DataFrame(dict(x=[],y=[],epwp=[]))
        df.x = x; df.y = y; df.epwp = epwp
        return df

    def _get_phase_by_name(self,phase_name):

        phase =  [x for x in self.g_o.Phases[:] if x.Name=='Phase_6']
        assert(len(phase) ==1)
        return phase[0]

