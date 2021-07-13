import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import read_nc, prep_proj_multi_cartopy, setup_grids_cartopy, draw_rec_4p, get_besttrack, read_obs_letkf

import cartopy.crs as ccrs
import cartopy.feature as cfeature

quick = True
#quick = False



def main( INFO={}, exp1="D1", exp2="NOHIM8_8km", otime=datetime( 2020, 9, 1, 0, 0 ) ):

    tlons, tlats, tslps, ttimes = get_besttrack()

    fn1 = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/{0:}/const/topo_sno_np00001/topo.pe000000.nc".format( exp1 )
    lon2d_d1 = read_nc( nvar="lon", fn=fn1 )
    lat2d_d1 = read_nc( nvar="lat", fn=fn1 )
    topo2d_d1 = read_nc( nvar="topo", fn=fn1 )
 
    print( "size:", topo2d_d1.shape )

    if exp2 != "":
       fn2 = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/{0:}/const/topo_sno_np00001/topo.pe000000.nc".format( exp2 )
       lon2d_d2 = read_nc( nvar="lon", fn=fn2 )
       lat2d_d2 = read_nc( nvar="lat", fn=fn2 )
       topo2d_d2 = read_nc( nvar="topo", fn=fn2 )

       lon_l = [ np.min( lon2d_d2 ), np.max( lon2d_d2) ]
       lat_l = [ np.min( lat2d_d2 ), np.max( lat2d_d2) ]

    lone = np.max( lon2d_d1 )
    lons = np.min( lon2d_d1 )
   
    late = np.max( lat2d_d1 )
    lats = np.min( lat2d_d1 )

    lons = 81
    lone = 179
    lats = 1
    late = 60

    print( "region", lons, lone, lats, late )
 
    # original data is lon/lat coordinate
    data_crs = ccrs.PlateCarree()


    fig = plt.figure( figsize=(7,4.5) )
    fig.subplots_adjust( left=0.09, bottom=0.06, right=0.96, top=0.96,
                         wspace=0.15, hspace=0.05)

    if INFO["proj"] == 'merc':
       ax_l = prep_proj_multi_cartopy( fig, xfig=1, yfig=1, proj=INFO["proj"],
                            latitude_true_scale=INFO['latitude_true_scale'] )

    elif INFO["proj"] == 'PlateCarree':
       ax_l = prep_proj_multi_cartopy( fig, xfig=1, yfig=1, proj=INFO["proj"],
                            central_longitude=INFO['central_longitude'] )
    elif INFO["proj"] == 'lcc':
       ax_l = prep_proj_multi_cartopy( fig, xfig=1, yfig=1, proj=INFO["proj"],
                            tlat1=INFO['tlat1'], tlat2=INFO['tlat2'],
                            central_longitude=INFO['central_longitude'],
                            central_latitude=INFO['central_latitude'],
                            latitude_true_scale=INFO['latitude_true_scale'] )

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

    ax = ax_l[0] 

    if INFO["proj"] == 'merc':
       setup_grids_cartopy( ax, xticks=xticks, yticks=yticks,
                                  fs=9, lw=0.25, color='k' )
    else:
       setup_grids_cartopy( ax, xticks=xticks, yticks=yticks,
                                  fs=9, lw=0.25, color='k' )

    ax.set_extent([ lons, lone, lats, late ], crs=data_crs )

    ax.add_feature( coast, zorder=1 )

    ax.add_feature( land  )
    ax.add_feature( ocean )

#    ax.contourf( lon2d_d1, lat2d_d1, topo2d_d1, 
#                 transform=data_crs ) 

    # draw domain
    lc = 'k'
    ax.plot( lon2d_d1[0,:], lat2d_d1[0,:], color=lc,
             transform=data_crs )
    ax.plot( lon2d_d1[-1,:], lat2d_d1[-1,:], color=lc,
             transform=data_crs )
    ax.plot( lon2d_d1[:,-1], lat2d_d1[:,-1], color=lc,
             transform=data_crs )
    ax.plot( lon2d_d1[:,0], lat2d_d1[:,0], color=lc,
             transform=data_crs )

    if exp2 != "":
       ax.plot( lon2d_d2[0,:], lat2d_d2[0,:], color=lc,
                transform=data_crs )
       ax.plot( lon2d_d2[-1,:], lat2d_d2[-1,:], color=lc,
                transform=data_crs )
       ax.plot( lon2d_d2[:,-1], lat2d_d2[:,-1], color=lc,
                transform=data_crs )
       ax.plot( lon2d_d2[:,0], lat2d_d2[:,0], color=lc,
                transform=data_crs )

       print( "check", np.max( lat2d_d2[0,:] ) )
       print( "check", np.max( lat2d_d1[0,:] ) )

    # draw typhoon
    ax.plot( tlons, tlats, transform=data_crs, color='k' )

    ms = 5
    for tidx in range( len(tlons) ):
        ttime_ = ttimes[tidx]
        if ttime_.day > 5 and ttime_.month == 9:
           break

        if ttime_.hour == 0:
           ax.plot( tlons[tidx], tlats[tidx], transform=data_crs,
                    marker='o', ms=ms, color='k' )

           if ttime_.day < 27:
              ax.text( tlons[tidx]-0.5, tlats[tidx], ttimes[tidx].strftime('%m/%d'),
                       fontsize=10, transform=data_crs,
                       ha="right",
                       va='top',
                       )

#    # plot obs
#    obs = read_obs_letkf( time=otime )
#    olons = obs[:,2]
#    olats = obs[:,3]
#    ms = 20
#    print( olons, olats )
#    ax.scatter( olons, olats, s=0.1, transform=data_crs, zorder=4,
#                 )
#    print( obs.shape )

    plt.show()
    sys.exit()
  




    fig, ( (ax1, ax2) ) = plt.subplots( 1, 2, figsize=( 10, 4.1 ) )
    fig.subplots_adjust( left=0.04, bottom=0.02, right=0.98, top=0.96,
                         wspace=0.1, hspace=0.3)
    


    ax_l = [ ax1, ax2 ] #
    m_l = prep_proj_multi( method='merc', ax_l=ax_l, ll_lon=lons, ur_lon=lone,
                           ll_lat=lats, ur_lat=late, fs=7, cc='gray', cw=0.3 )

    lon2d_l = [ lon2d_d1, lon2d_gfs]
    lat2d_l = [ lat2d_d1, lat2d_gfs]
    var_l = [ mslp_d1, mslp_gfs ]    

    levs = np.arange( 800, 1100, 4 )
    fac = 1.e-2    
    lw =0.5

    tit_l = [
             "SCALE-LETKF: D1",
             "GFS",
            ]

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
    
    fig.suptitle( "Analyzed MSLP (Pa)")

    ofig = "D1_GFS_MSLP_{0:}".format( time.strftime('%Y%m%d%H%M'), )
    plot_or_save( quick=quick, opath="png/2p_mslp", ofig=ofig )   

###########
time = datetime( 2020, 9, 5, 0, 0 )

stime = datetime( 2020, 9, 1, 0, 0 )
etime = datetime( 2020, 9, 7, 12, 0 )

#stime = datetime( 2020, 9, 2, 0, 0 )
stime = datetime( 2020, 9, 3, 0, 0 )
#etime = datetime( 2020, 8, 29, 0, 0 )
etime = datetime( 2020, 9, 5, 0, 0 )
#etime = stime

exp2 = ""
exp2 = "NOHIM8_8km_3"
exp2 = "NOHIM8_8km_4"
exp2 = "NOHIM8_8km_5"
exp2 = "NOHIM8_8km_6"
exp2 = "NOHIM8_8km_7"
exp2 = "NOHIM8_8km_8"
exp2 = "NOHIM8_8km_9"



exp1 = "D1/D1_20210629"
exp2 = "D2/NOHIM8_4km"
#proj = "lcc"
proj = 'PlateCarree'
INFO = { 'proj': proj,
         'latitude_true_scale': 30.0,
         'tlat1':20.0, 
         'tlat2':40.0,
         'central_longitude': 130.0, 
         'central_latitude': 30.0,
         }

main( INFO=INFO, exp1=exp1, exp2=exp2 )

