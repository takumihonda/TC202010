import numpy as np
import matplotlib.pyplot as plt

def m2d( m=1.0, a=1.0, b=1.0 ):
    return( a * np.power( m, b ) )

def get_v( mmin=0.0, mmax=0.1, minc=0.1, 
           alpha=40.0, beta=0.230, gamma=1/2, 
           rho_0=1.0, rho=1.0 ):

    m_l = np.arange( mmin, mmax+minc, minc )

    v_l = np.zeros( m_l.shape )

    for i, m_ in enumerate( m_l ):
      v_ = alpha * np.power( m_, beta ) * np.power( rho_0 / rho, gamma )
      v_l[i] = v_

    return( v_l, m_l )


########
alpha_def = 27.70
beta_def  = 0.216
gamma = 1/2

rho_0 = 1.0
rho = 1.0

# [kg]
mmin = 0.0
mmax = 5.0e-5
minc = 1.e-8

alpha_snow_s = 29257.1601562500
alpha_snow_l = 305.678619384766
beta_snow_s  = 0.528109610080719
beta_snow_l  = 0.329863965511322

v_snow_def, m_l = get_v( alpha=alpha_def, beta=beta_def, 
                   mmin=mmin, mmax=mmax, minc=minc )
v_snow_s, _ = get_v( alpha=alpha_snow_s, beta=beta_snow_s, 
                   mmin=mmin, mmax=mmax, minc=minc )
v_snow_l, _ = get_v( alpha=alpha_snow_l, beta=beta_snow_l, 
                   mmin=mmin, mmax=mmax, minc=minc )


ymin = 0.0
ymax = 10.0
fig, ax1 = plt.subplots( 1, 1, figsize=( 8, 6.5 ) )   

dmin = 0.0
dmax = 1.e-5

ax1.set_xlim( dmin*1.e3, dmax*1.e3 )
ax1.set_ylim( ymin, ymax )

data_l = [ v_snow_def, v_snow_s, v_snow_l ]
lab_l = ["default", "small", "large" ]
c_l = [ 'k', 'b', 'r' ]

d_l = m2d( m_l )

for i, data, in enumerate( data_l ):
   ax1.plot( d_l*1.e3, data, label=lab_l[i], color=c_l[i] )

ax1.legend( loc='upper left', fontsize=12, )
#ax1.set_xlabel( 'Mass (g)')
ax1.set_xlabel( 'Maximum dimension (mm)')
ax1.set_ylabel( 'Terminal velocity (m/s)')
plt.show()

