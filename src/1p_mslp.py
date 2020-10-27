import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import prep_proj_multi, plot_cbar, plot_or_save, get_gfs_grads_latlon, read_gfs_mslp_grads, read_nc

quick = True
quick = False

lons = 120
lone = 155

lats = 15
late = 50


def main( stime=datetime( 2020, 9, 5, 0, 0 ), ftime=datetime( 2020, 9, 5, 0, 0 ) ):


    fn = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.1/OUTPUT/TC202010_D1/{0:}/fcst_sno_np00001/mean/p_history.pe000000.nc".format( stime.strftime('%Y%m%d%H%M%S') )
    time_d1 = read_nc( nvar="time", fn=fn )[:]

    fsec = int( ( ftime - stime ).total_seconds() )

    mslp_d1 = read_nc( nvar="MSLP", fn=fn )[:,:,:]
    mslp_d1 = mslp_d1[ time_d1==fsec ]

    mslp_min = np.min( mslp_d1 ) * 0.01

    lon2d_d1 = read_nc( nvar="lon", fn=fn )
    lat2d_d1 = read_nc( nvar="lat", fn=fn )
 

    fig, ax1 = plt.subplots( 1, 1, figsize=( 8, 6.5 ) )
    fig.subplots_adjust( left=0.02, bottom=0.03, right=0.98, top=0.95,
                         wspace=0.1, hspace=0.3)

   
    lone = np.max( lon2d_d1 )
    lons = np.min( lon2d_d1 )
   
    late = np.max( lat2d_d1 )
    lats = np.min( lat2d_d1 )

    ax_l = [ ax1,  ] #
    m_l = prep_proj_multi( method='merc', ax_l=ax_l, ll_lon=lons, ur_lon=lone,
                           ll_lat=lats, ur_lat=late, fs=7, cc='gray', cw=0.3 )

    lon2d_l = [ lon2d_d1, ]
    lat2d_l = [ lat2d_d1, ]
    var_l = [ mslp_d1[0,:,:], ]    

    levs = np.arange( 800, 1100, 4 )
    fac = 1.e-2    
    lw =0.5

    fth = int( fsec / 3600 )
    tit1 = "Forecast (FT={0:0=3}h), MSLP:{1:.1f} hPa".format( fth, mslp_min )
    mslp_txt = "MSLP:{0:.1f} hPa".format( mslp_min )

    tit_l = [
             tit1,
            ]

    bbox = { 'facecolor':'w', 'alpha':1.0, 'pad':2,
             'edgecolor':'w' }

    for i, ax in enumerate( ax_l ):

        x2d, y2d = m_l[0]( lon2d_l[i], lat2d_l[i] )

        cont = ax.contour( x2d, y2d, var_l[i]*fac,
                         levels=levs, linewidths=lw, colors='k' )
        
        ax.clabel( cont, fmt='%1.0f', fontsize=8, )

    
        ax.text( 0.5, 1.01, tit_l[i],
                 fontsize=13, transform=ax.transAxes,
                 ha="center",
                 va='bottom',
                 )
    
        ctime = time.strftime('%HUTC %m/%d/%Y')
        ax.text( 1.0, 1.01, ctime,
                  fontsize=10, transform=ax.transAxes,
                  ha="right",
                  va='bottom',
                 )
    
        ax.text( 0.99, 0.99, mslp_txt,
                  fontsize=11, transform=ax.transAxes,
                  ha="right",
                  va='top',
                  bbox=bbox,
                  zorder=5,
                 )

#    fig.suptitle( "Analyzed MSLP (Pa)")

    ofig = "D1_fcst_s{0:}_{1:0=3}h_MSLP".format( stime.strftime('%m%d%H'), fth, )
    plot_or_save( quick=quick, opath="png/1p_mslp_fcst", ofig=ofig )   

###########
time = datetime( 2020, 9, 5, 0, 0 )

stime = datetime( 2020, 9, 1, 0, 0 )
etime = datetime( 2020, 9, 7, 12, 0 )

ftime = datetime( 2020, 9, 5, 0, 0 )


stime = datetime( 2020, 9, 3, 0, 0 )
#stime = datetime( 2020, 9, 4, 0, 0 )
etime = datetime( 2020, 9, 8, 0, 0 )


time = stime
while time <= etime:
   main( stime=stime, ftime=time )
   time += timedelta( hours=24 )

