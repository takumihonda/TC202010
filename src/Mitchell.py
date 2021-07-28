import numpy as np
import sys

import matplotlib.pyplot as plt

def X2ab( X=np.array([]) ):
    a_l = np.zeros( X.shape )
    b_l = np.zeros( X.shape )

    a_l = np.where( ( 0.01 < X ) & ( X <= 10.0       ), 0.04394, a_l )
    a_l = np.where( ( 10.0 < X ) & ( X <= 585        ), 0.06049, a_l )
    a_l = np.where( ( 585  < X ) & ( X <= 1.56*1.e5  ), 0.02072, a_l )
    a_l = np.where( ( 1.56*1.e5  < X ) & ( X <= 1.e8 ), 1.0865 , a_l )
    
    b_l = np.where( ( 0.01 < X ) & ( X <= 10.0       ), 0.970, b_l )
    b_l = np.where( ( 10.0 < X ) & ( X <= 585        ), 0.831, b_l )
    b_l = np.where( ( 585  < X ) & ( X <= 1.56*1.e5  ), 0.638, b_l )
    b_l = np.where( ( 1.56*1.e5  < X ) & ( X <= 1.e8 ), 0.499, b_l )

    return( a_l, b_l )

def get_Re( X=np.array([]), a=np.array([]), b=np.array([]) ):
    return( a*np.power( X, b) )

def get_X( alpha=1.0, rho_a=1.0, d=np.array([]), beta=1.0, sigma=1.0, gamma=1.0, nu=1.0, 
           g=9.81):

    # Eq. 17 in Mitchell (1993)
    eta = 1.4086*1.e-5 # Seifert and Beheng (2006)
    X = 2*alpha*g*rho_a*np.power( d, beta+2-sigma ) / ( gamma*eta**2 )
    return( X )

def Mitchell1993( d=np.array([]), dfac=1.e-6 ):
    g = 9.81
    rho_a = 1.0

    nu = 1.0

    # snow
    alpha = 0.00739
    beta = 2.45
    gamma = 0.2285
    sigma = 1.88

    X = get_X( d=d*dfac, alpha=alpha, beta=beta, gamma=gamma, sigma=sigma, nu=nu, rho_a=rho_a, g=g )
    a_l, b_l = X2ab( X=X )

#    X = np.arange( 1, 1.e8, 10 )
#    a_l, b_l = X2ab( X=X )
#    Re = get_Re( X=X, a=a_l, b=b_l )
    
    # Eq. 22 in Mitchell (1993)
    vt = a_l * nu * np.power( 2*alpha*g / ( rho_a*nu**2*gamma ), b_l ) * np.power( d*dfac, b_l*(beta+2-sigma)-1 )
    return( vt )


def main( INFO={}):
    print( INFO['alpha'] )

    d_l = np.arange( INFO["dmin"], INFO["dmax"]+INFO["dinc"], INFO["dinc"] )

    dfac = 1.e-6
    d_l = np.arange( 10, 450, 10 )
    vt_l = Mitchell1993( d=d_l, dfac=dfac )
  
    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots( 1, 1, figsize=( 8, 6.5 ) )   
    ax1.plot( d_l, vt_l )
    ax1.set_xlabel( "Dimension (µm)")
    plt.show() 
#    a, nu, alpha, g, rho_a, gamma, D, b, beta, sigma, 

########
alpha = 0.1
beta = 0.1
gamma = 0.1
sigma = 0.1

dmin = 0.1
dmax = 1.0
dinc = 0.1

INFO = { 'alpha': alpha, 'beta': beta, 'gamma': gamma, 'sigma': sigma,
         'dmin': dmin, 'dmax':dmax, 'dinc': dinc }
main( INFO=INFO )


