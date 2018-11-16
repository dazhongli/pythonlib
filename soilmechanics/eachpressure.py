from numpy import sin,cos

def ka_Coulomb(phi, c=0,alpha=90, beta=0,q=0,gamma=18,H=0):
    '''
    This function calculate the active earth pressure using the coulomb method
    '''
    if c !=0:
        kq = 1 + 2*q*sin(alpha)*cos(beta)/(gamma*H*sin(alpha+beta))
        eta = 2*c/(\gamma*H)
    else:
        kq = 1.0
        eta = 0
    ka = sin(alpha+beta)/(sin(alpha)**2 * sin(alpha + beta - phi - delta) *

