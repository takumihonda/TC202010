import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import prep_proj_multi_cartopy, setup_grids_cartopy, plot_cbar, plot_or_save, read_nc, cmap_Him8, band2wavelength

import cartopy.crs as ccrs
import cartopy.feature as cfeature

quick = True
#quick = False



def main( stime=datetime( 2020, 9, 5, 0, 0 ), ftime=datetime( 2020, 9, 5, 0, 0 ), top="", exp="", exp_topo="D2/NOHIM8_4km_NP2304",
          ftint=timedelta( hours=6 ), dir='fcst', fhead='' ):

    fsec = int( ( ftime - stime ).total_seconds() )

    ftlev = int( ( ftime - stime ).total_seconds() / ftint.total_seconds() )
    print( ftint.total_seconds(), ( ftime - stime ).total_seconds() )
    fn = '{0:}/{1:}/{2:}/{4:}/mean/{5:}Him8_{2:}_mean_FTSEC{3:0=7}.nc'.format( top, exp, stime.strftime('%Y%m%d%H%M%S'), fsec, dir, fhead )

    print( fn )

    ofn = '{0:}/{1:}/Him8_{2:}_sobs.nc'.format( top, 'D2/Him8', ftime.strftime('%Y%m%d%H%M%S') )

    otbb = read_nc( nvar="tbb", fn=ofn )[:,:,:]
    oband = read_nc( nvar="band", fn=ofn )

    tbb_d1 = read_nc( nvar="tbb", fn=fn )[:,:,:]
    band_d1 = read_nc( nvar="band", fn=fn )[:]
#    tbb_d1 = tbb_d1[ band_d1==band ]


    lon2d_d1 = read_nc( nvar="lon", fn=fn )
    lat2d_d1 = read_nc( nvar="lat", fn=fn )
 
    tvar = r'BT (K)'

    fig = plt.figure( figsize=( 14,10 ) )

    fig.subplots_adjust( left=0.05, bottom=0.05, right=0.92, top=0.9,
                         wspace=0.05, hspace=0.2)
   
    lone = np.max( lon2d_d1 ) + 2
    lons = np.min( lon2d_d1 ) - 2 
   
    late = np.max( lat2d_d1 ) + 2
    lats = np.min( lat2d_d1 ) - 2

    central_longitude = 130.0
    ax_l = prep_proj_multi_cartopy( fig, xfig=4, yfig=2, proj="PlateCaree",
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


    lon2d_l = [ lon2d_d1, lon2d_d1, lon2d_d1, lon2d_d1,
                lon2d_d1, lon2d_d1, lon2d_d1, lon2d_d1, ]
    lat2d_l = [ lat2d_d1, lat2d_d1, lat2d_d1, lat2d_d1, 
                lat2d_d1, lat2d_d1, lat2d_d1, lat2d_d1, ]
#    cvar_l = [ mslp_d1[0,:,:], ]    
    band1 = 8
    band2 = 9
    band3 = 10
    band4 = 13

    band_l = [ band1, band2, band3, band4,
               band1, band2, band3, band4,  ]

    var_l = [ tbb_d1[ band_d1==band1][0,:,:],
              tbb_d1[ band_d1==band2][0,:,:],
              tbb_d1[ band_d1==band3][0,:,:],
              tbb_d1[ band_d1==band4][0,:,:],
              otbb[ oband==band1][0,:,:],
              otbb[ oband==band2][0,:,:],
              otbb[ oband==band3][0,:,:],
              otbb[ oband==band4][0,:,:],
             ]    

    clevs = np.arange( 800, 1100, 4 )
    cfac = 1.e-2    
    lw = 1.0

    levs = np.arange( 0.5, 6.5, 0.5  )
    fac = 1.e-3
    cmap = plt.cm.get_cmap("jet")

    cmap, levs = cmap_Him8( vmin=190, vmax=300, dv=4 )
    fac = 1.e0

    cmap.set_under( 'gray', alpha=1.0 )
    cmap.set_over( 'k', alpha=1.0 )

    fth = int( fsec / 3600 )

    tit1 = 'SCALE'
    tit2 = 'Obs'

    ft_info = "FT={0:0=4} s".format( fsec, )
    ofig = "8p_{0:}Fcst_s{1:}_{2:0=4}s_sobs".format( fhead, stime.strftime('%m%d%H'), fsec,)

    tit_l = [
             tit1,
             tit1,
             tit1,
             tit1,
             tit2,
             tit2,
             tit2,
             tit2,
            ]

    bbox = { 'facecolor':'w', 'alpha':1.0, 'pad':2,
             'edgecolor':'w' }

    for i, ax in enumerate( ax_l ):

        xfs = 8
        yfs = 8
        if ( i >= 1 and i <= 3 ) or ( i >= 5 and i <= 7 ):
           yfs = 0.0
      
        setup_grids_cartopy( ax, xticks=xticks, yticks=yticks,
                             xfs=xfs, yfs=yfs, lw=0.25, color='k' )

        ax.set_extent([ lons, lone, lats, late ], crs=data_crs )
        ax.add_feature( coast, zorder=1 )
        ax.add_feature( land, zorder=0 )

        SHADE = ax.contourf( lon2d_l[i], lat2d_l[i], var_l[i]*fac, 
                         transform=data_crs,
                         levels=levs, cmap=cmap, extend='both' )

        if i <= 3:
           ax.text( 0.5, 0.99, ft_info,
                    fontsize=11, transform=ax.transAxes,
                    ha="center",
                    va='top', bbox=bbox,
                    )

        if i == 3:
           plot_cbar( ax, shade=SHADE, fig=fig, levs=levs, cb_height_rat=1.8,
                      dx=0.01 )

           ctime = time.strftime('%H%M UTC\n%m/%d/%Y')
           ax.text( 1.0, 1.01, ctime,
                     fontsize=10, transform=ax.transAxes,
                     ha="left",
                     va='bottom',
                    )

#        ax.text( 0.99, 1.01, tvar,
#                 fontsize=13, transform=ax.transAxes,
#                 ha="right",
#                 va='bottom',
#                 )

#        cont = ax.contour( lon2d_l[i], lat2d_l[i], cvar_l[i]*cfac,
#                         transform=data_crs,
#                         levels=clevs, linewidths=lw, colors='k' )
#        
#        ax.clabel( cont, fmt='%1.0f', fontsize=8, )


        ax.text( 0.5, 1.01, '{0:} (Band {1:})'.format( tit_l[i], band_l[i] ),
                 fontsize=13, transform=ax.transAxes,
                 ha="center",
                 va='bottom',
                 )
    
    
#        ax.text( 0.99, 0.99, mslp_txt,
#                  fontsize=11, transform=ax.transAxes,
#                  ha="right",
#                  va='top',
#                  bbox=bbox,
#                  zorder=5,
#                 )

    fig.suptitle( "AHI brightness temperature (K)", fontsize=14 )

    plot_or_save( quick=quick, opath="png/8p_fcst_sobs_tbb/{0:}".format( exp ), ofig=ofig )   

###########



#etime = stime 

top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020"
exp = "D2/NOHIM8_4km_NP2304"
#exp = "D2/NOHIM8_4km_NP2304_alhpa_v_s_lb3000"
#exp = "D2/NOHIM8_4km_NP2304_cfill_s0.99"
stime0 = datetime( 2020, 8, 29, 6, 0 )
tint = timedelta( hours=12)
#etime = datetime( 2020, 9, 4, 0, 0 )

#exp = "D1/D1_20210629"
#stime0 = datetime( 2020, 8, 29, 0, 0 )
#tint = timedelta( hours=24)
#stime = datetime( 2020, 8, 29, 0, 0 )
#etime = datetime( 2020, 9, 4, 0, 0 )

dir = 'fcst_short'
stime = datetime( 2020, 8, 29, 7, 0 )
#stime = datetime( 2020, 8, 29, 6, 10 )

#dir = 'fcst_long'
#stime = datetime( 2020, 8, 30, 12, 0 )


etime = stime


band = 13
band = 8
band = 10
#band = 9

fhead = ""
#fhead = "clr_"
#fhead = "cfrac2018_"
#fhead = "nokadd_clr_"
#fhead = "t5_clr_"
#fhead = "t25_clr_"
#fhead = "ppmv_clr_"
#fhead = "debug_clr_"
#fhead = "debug_qmin_clr_"
#fhead = "q0_clr_"
#fhead = "noq_above_clr_"
#fhead = "zenith0_clr_"
#fhead = "zenith65_clr_"
#fhead = "zenith_"

time = stime
while time <= etime:
   main( stime=stime0, ftime=time, top=top, exp=exp, dir=dir, 
         fhead=fhead )
   time += tint

