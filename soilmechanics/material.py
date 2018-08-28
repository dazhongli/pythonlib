import numpy as np

class Material:
    def __init__(self):
       self.gamma = np.nan() # unit weight
       self.E = np.nan() #Young Modulus
       self.name = 'None' #name of material
       self.poisson_ratio = 0.25


class SoilMC(Material):
    '''
    Mohr Coulum Material, i.e., elasticity-perfect-plasticity material defined by E, c, and phi
    '''
    def __init__(self):
        self.C = np.nan()
        self.phi = np.nan()
        self.cu = np.nan()
