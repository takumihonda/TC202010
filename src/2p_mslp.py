import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import plot_cbar, plot_or_save, get_gfs_grads_latlon, read_gfs_mslp_grads, read_nc, prep_proj_multi_cartopy, setup_grids_cartopy

import cartopy.crs as ccrs
import cartopy.feature as cfeature

quick = True
quick = False

lons = 120
lone = 155

lats = 15
late = 50


def main( time=datetime( 2020, 9, 5, 0, 0 ), exp="", ):

    lon2d_gfs, lat2d_gfs = get_gfs_grads_latlon()
    mslp_gfs = read_gfs_mslp_grads( time=time )

#    fn = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.1/OUTPUT/TC202010_D1/{0:}//fcst_sno_np00001/mean/p_history.pe000000.nc".format( time.strftime('%Y%m%d%H%M%S') )
    fn = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/D1/{0:}/{1:}/hist_sno_np00001/mean/p_history.pe000000.nc".format( exp, time.strftime('%Y%m%d%H%M%S') )
    mslp_d1 = read_nc( nvar="MSLP", fn=fn )[0,:,:]
    lon2d_d1 = read_nc( nvar="lon", fn=fn )
    lat2d_d1 = read_nc( nvar="lat", fn=fn )
   
    fig = plt.figure( figsize=( 10,3.9 ) )
    #fig, ( (ax1, ax2) ) = plt.subplots( 1, 2, figsize=( 10, 4.1 ) )
    fig.subplots_adjust( left=0.04, bottom=0.02, right=0.98, top=0.96,
                         wspace=0.1, hspace=0.3)
    
    lone = np.max( lon2d_d1 ) + 1
    lons = np.min( lon2d_d1 ) - 1
   
    late = np.max( lat2d_d1 ) + 1
    lats = np.min( lat2d_d1 ) - 1

#    m_l = prep_proj_multi( method='merc', ax_l=ax_l, ll_lon=lons, ur_lon=lone,
#                           ll_lat=lats, ur_lat=late, fs=7, cc='gray', cw=0.3 )

    central_longitude = 130.0
    ax_l = prep_proj_multi_cartopy( fig, xfig=2, yfig=1, proj="PlateCaree",
                         central_longitude=central_longitude )

    # original data is lon/lat coordinate
    data_crs = ccrs.PlateCarree()

    xticks = np.arange( 40, 205, 10 )
    yticks = np.arange( 0, 85, 10 )

    res = '50m'

    coast = cfeature.NaturalEarthFeature( 'physical', 'coastline', res,
                                         facecolor='none',
                                         edgecolor='k', )

    land = cfeature.NaturalEarthFeature( 'physical', 'land', res,
                                         edgecolor='face',
                                         facecolor=cfeature.COLORS['land'] )

    ocean = cfeature.NaturalEarthFeature( 'physical', 'ocean', res,
                                         edgecolor='face',
                                         facecolor=cfeature.COLORS['water'] )








    lon2d_l = [ lon2d_d1, lon2d_gfs]
    lat2d_l = [ lat2d_d1, lat2d_gfs]
    var_l = [ mslp_d1, mslp_gfs ]    

    levs = np.arange( 800, 1100, 4 )
    fac = 1.e-2    
    lw = 0.5

    lws = np.zeros( levs.shape )
    lws[:] = lw
    lws[ levs == 1000 ] = lw*4

    tit_l = [
             "SCALE-LETKF: D1",
             "GFS",
            ]

    for i, ax in enumerate( ax_l ):

        setup_grids_cartopy( ax, xticks=xticks, yticks=yticks,
                                 fs=9, lw=0.25, color='k' )
    
        ax.set_extent([ lons, lone, lats, late ], crs=data_crs )
    
        ax.add_feature( coast, zorder=1 )
    
        ax.add_feature( land  )
        ax.add_feature( ocean )

        #x2d, y2d = m_l[0]( lon2d_l[i], lat2d_l[i] )

        #cont = ax.contour( x2d, y2d, var_l[i]*fac,
        cont = ax.contour( lon2d_l[i], lat2d_l[i], var_l[i]*fac,
                         levels=levs, linewidths=lws, colors='k', transform=data_crs )
        
        ax.clabel( cont, fmt='%1.0f', fontsize=8, )

        if i == 0: 
           # draw domain
           lc = 'k'
           ax.plot( lon2d_l[i][0,:], lat2d_l[i][0,:], color=lc,
                    transform=data_crs )
           ax.plot( lon2d_l[i][-1,:], lat2d_l[i][-1,:], color=lc,
                    transform=data_crs )
           ax.plot( lon2d_l[i][:,0], lat2d_l[i][:,0], color=lc,
                    transform=data_crs )
           ax.plot( lon2d_l[i][:,-1], lat2d_l[i][:,-1], color=lc,
                    transform=data_crs )

   
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
    
    fig.suptitle( "Analyzed MSLP (Pa)", fontsize=14)

    ofig = "D1_GFS_MSLP_{0:}".format( time.strftime('%Y%m%d%H%M'), )
    plot_or_save( quick=quick, opath="png/2p_mslp", ofig=ofig )   

###########
time = datetime( 2020, 9, 5, 0, 0 )

stime = datetime( 2020, 9, 1, 0, 0 )
etime = datetime( 2020, 9, 7, 12, 0 )

stime = datetime( 2020, 8, 20, 0, 0 )
etime = datetime( 2020, 9,  5, 0, 0 )
#etime = stime

exp = "D1_20210629"

time = stime
while time <= etime:
   main( time=time, exp=exp )
   time += timedelta( hours=24 )

