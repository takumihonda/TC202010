import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import prep_proj_multi, plot_cbar, plot_or_save, get_gfs_grads_latlon, read_gfs_mslp_grads

quick = True
#quick = False

lons = 120
lone = 155

lats = 15
late = 50


def main( time=datetime( 2020, 9, 5, 0, 0 ), ):

    lon2d, lat2d = get_gfs_grads_latlon()

    mslp = read_gfs_mslp_grads( time=time )
    
    fig, ax1 = plt.subplots( 1, 1, figsize=( 8, 6.5 ) )
    fig.subplots_adjust( left=0.02, bottom=0.03, right=0.98, top=0.95,
                         wspace=0.1, hspace=0.3)
    
    lons = 105 
    lone = 165 
    late = 50
    lats = 5
    
    ax_l = [ ax1] #
    m_l = prep_proj_multi( method='merc', ax_l=ax_l, ll_lon=lons, ur_lon=lone,
                           ll_lat=lats, ur_lat=late, fs=7, cc='gray', cw=0.3 )
    
    x2d, y2d = m_l[0](lon2d, lat2d)
    
    
    #tbb = tbb[ ( lon2d >= lons ) & (lon2d <= lone ) & ( lat2d >= lats ) & ( lat2d <= late ) ]
    #
    #print( tbb.shape )
    levs = np.arange( 800, 1100, 4 )
    fac = 1.e-2    
    lw =0.5

    cont = ax1.contour( x2d, y2d, mslp*fac,
                     levels=levs, linewidths=lw, colors='k' )
    
    ax1.clabel( cont, fmt='%1.0f', fontsize=8, )

    ptit = "GFS Analysis: MSLP (hPa)"
    
    ax1.text( 0.5, 1.01, ptit,
              fontsize=13, transform=ax1.transAxes,
              ha="center",
              va='bottom',
             )
    
    ctime = time.strftime('%HUTC %m/%d/%Y')
    ax1.text( 1.0, 1.01, ctime,
              fontsize=10, transform=ax1.transAxes,
              ha="right",
              va='bottom',
             )
    
    ofig = "GFS_MSLP_{0:}".format( time.strftime('%Y%m%d%H%M'), )
    plot_or_save( quick=quick, opath="png/gfs_mslp", ofig=ofig )   

###########
time = datetime( 2020, 9, 5, 0, 0 )

stime = datetime( 2020, 9, 1, 0, 0 )
etime = datetime( 2020, 9, 7, 12, 0 )

stime = datetime( 2020, 9, 5, 18, 0 )
etime = stime

time = stime
while time <= etime:
   main( time=time, )
   time += timedelta( hours=6 )

