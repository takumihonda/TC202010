import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import read_Him8_obs, cmap_Him8, prep_proj_multi, plot_cbar, plot_or_save, read_LIDEN_all

quick = True
quick = False

lons = 120
lone = 155

lats = 15
late = 50


def main( time=datetime( 2020, 9, 5, 0, 0 ), band=13, liden_min=60 ):

    llons, llats, ltimes = read_LIDEN_all( )

    tbb, lon1d, lat1d = read_Him8_obs( time=time, band=band )
    lon2d, lat2d = np.meshgrid( lon1d, lat1d )
    
    fig, ax1 = plt.subplots( 1, 1, figsize=( 8, 6.5 ) )
    fig.subplots_adjust( left=0.02, bottom=0.03, right=0.98, top=0.95,
                         wspace=0.1, hspace=0.3)
    
    lons = 105 
    lone = 165 
    late = 50
    lats = 5
    
    ax_l = [ ax1] #
    m_l = prep_proj_multi( method='merc', ax_l=ax_l, ll_lon=lons, ur_lon=lone,
                           ll_lat=lats, ur_lat=late, fs=7, cc='lime', cw=0.3 )
    
    x2d, y2d = m_l[0](lon2d, lat2d)
    
    
    #tbb = tbb[ ( lon2d >= lons ) & (lon2d <= lone ) & ( lat2d >= lats ) & ( lat2d <= late ) ]
    #
    #print( tbb.shape )
    
    cmap, levs = cmap_Him8()
    
    shade = ax1.contourf( x2d, y2d, tbb, cmap=cmap,
                     levels=levs, extend='both' )
    
    plot_cbar( ax1, shade=shade, fig=fig )
    
    ptit = "Himawari-8 B{0:0=2}".format( band )
    
    ax1.text( 0.5, 1.01, ptit,
              fontsize=13, transform=ax1.transAxes,
              ha="center",
              va='bottom',
             )
    
    ctime = time.strftime('%H:%M UTC %m/%d/%Y')
    ax1.text( 1.0, 1.01, ctime,
              fontsize=10, transform=ax1.transAxes,
              ha="right",
              va='bottom',
             )
 
    lstime = time - timedelta( minutes=liden_min )

    lxs, lys = m_l[0](llons, llats)
    lxs[ ( ltimes < lstime ) | ( ltimes > time ) ] = np.nan
    ax1.scatter( lxs, lys, s=2, c='yellow', edgecolors='k',
                  linewidths=0.1, marker='o' )
   
    ofig = "Him8_B{0:0=2}_{1:}_LIDEN{2:0=3}min".format( band, time.strftime('%Y%m%d%H%M'), liden_min )
    plot_or_save( quick=quick, opath="png/Him8_LIDEN", ofig=ofig )   

###########

stime = datetime( 2020, 9, 3, 1, 0 )
etime = datetime( 2020, 9, 6, 12, 0 )

liden_min = 60

band = 8
#band = 9
band = 13

dh = 1
#etime = stime

time = stime
while time <= etime:
   main( time=time, band=band, liden_min=liden_min )
   time += timedelta( hours=dh )

