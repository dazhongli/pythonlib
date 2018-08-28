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

def Bouss_rect_average(length,width,depth):
    '''
    This function return the average stress coefficient under a rectangular loading
    '''
    l = length; b = width; Z = depth;
    X = sqrt(l**2+l**2+Z**2)
    Y = sqrt(b**2+l**2)
    C1 = l*log(((X-b)*(Y+b))/((X+b)*(Y-b)))
    C2 = b*log(((X-l)*(Y+l))/((X+l)*(Y-l)))
    C3 = Z*arctan((l*b)/(Z*X))
    alpha = 1/(2*pi*Z)*(C1+C2+C3)
    return alpha
class Consolidation
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

