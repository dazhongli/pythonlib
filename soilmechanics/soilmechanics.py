from numpy import sqrt,pi,arctan
import numpy as np

def Ka(alpha, beta, theta, q, delta, c):
    pass


def Bouss_rect(width, length, depth):
    '''
    This function returns the load factor  at corner of the rectangular loading
    Input:
        width - width of loading
        length - length of loading
        depth - depth of point of interest at the corner
    return:
        I0
        P - I_0 * P_0
    '''
    pM = width / depth
    pN = length / depth
    pV = pM**2 + pN**2 +1
    pV1 = (pM * pN)**2

    c1 = 2 * pM * pN * sqrt(pV)/(pV + pV1)
    c2 = (pV + 1)/pV
    c3 = (2 * pN * pM *sqrt(pV))/(pV - pV1)
    return np.where(pV1>=pV, 1/(4*pi)*((c1*c2)+arctan(c3)+pi),1/(4*pi)*((c1*c2)+arctan(c3)))

class Consolidation:

    def __int__(self):
        self.Cc = 0
        self.Cr = 0
        self.e0 = 0
        self.initilized = False
        self.H = 0

    def plot_tv_doc():
        pass

class consolidation_Terzaghi (Consolidation):
    pass
