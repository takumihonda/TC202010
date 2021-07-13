import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import prep_proj_multi_cartopy, setup_grids_cartopy, plot_cbar, plot_or_save, read_nc, cmap_Him8

import cartopy.crs as ccrs
import cartopy.feature as cfeature

quick = True
quick = False



def main( stime=datetime( 2020, 9, 5, 0, 0 ), ftime=datetime( 2020, 9, 5, 0, 0 ), top="", exp="", exp_topo="D2/NOHIM8_4km_NP2304",
          ftint=timedelta( hours=6 ), band=9 ):


    ftlev = int( ( ftime - stime ).total_seconds() / ftint.total_seconds() )
    print( ftint.total_seconds(), ( ftime - stime ).total_seconds() )
    fn = '{0:}/{1:}/{2:}/fcst/mean/Him8_{2:}_mean_FT{3:0=4}.nc'.format( top, exp, stime.strftime('%Y%m%d%H%M%S'), ftlev )

    fn_topo = '{0:}/{1:}/{2:}/fcst_sno_np00001/mean/p_history.pe000000.nc'.format( top, exp, stime.strftime('%Y%m%d%H%M%S') )

    fsec = int( ( ftime - stime ).total_seconds() )

#    mslp_d1 = read_nc( nvar="MSLP", fn=fn )[:,:,:]
#    mslp_d1 = mslp_d1[ time_d1==fsec ]

    tbb_d1 = read_nc( nvar="tbb", fn=fn )[:,:,:]
    band_d1 = read_nc( nvar="band", fn=fn )[:]
    tbb_d1 = tbb_d1[ band_d1==band ]


#    mslp_min = np.min( mslp_d1 ) * 0.01

    lon2d_d1 = read_nc( nvar="lon", fn=fn_topo )
    lat2d_d1 = read_nc( nvar="lat", fn=fn_topo )
 
    tvar = r'BT (K)'

    fig = plt.figure( figsize=( 8,10 ) )

    fig.subplots_adjust( left=0.05, bottom=0.05, right=0.95, top=0.95,
                         wspace=0.1, hspace=0.3)
   
    lone = np.max( lon2d_d1 ) + 2
    lons = np.min( lon2d_d1 ) - 2 
   
    late = np.max( lat2d_d1 ) + 2
    lats = np.min( lat2d_d1 ) - 2

    central_longitude = 130.0
    ax_l = prep_proj_multi_cartopy( fig, xfig=1, yfig=1, proj="PlateCaree",
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


    lon2d_l = [ lon2d_d1, ]
    lat2d_l = [ lat2d_d1, ]
#    cvar_l = [ mslp_d1[0,:,:], ]    
    var_l = [ tbb_d1[0,:,:] ]    

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
    tit1 = "{0:}".format( tvar )
#    mslp_txt = "MSLP:{0:.1f} hPa".format( mslp_min )

    ft_info = "Forecast (FT={0:0=3}h)".format( fth, )

    tit_l = [
             tit1,
            ]

    bbox = { 'facecolor':'w', 'alpha':1.0, 'pad':2,
             'edgecolor':'w' }

    for i, ax in enumerate( ax_l ):

        setup_grids_cartopy( ax, xticks=xticks, yticks=yticks,
                                 fs=9, lw=0.25, color='k' )

        ax.set_extent([ lons, lone, lats, late ], crs=data_crs )
        ax.add_feature( coast, zorder=1 )
        ax.add_feature( land, zorder=0 )

        SHADE = ax.contourf( lon2d_l[i], lat2d_l[i], var_l[i]*fac, 
                         transform=data_crs,
                         levels=levs, cmap=cmap, extend='both' )

        plot_cbar( ax, shade=SHADE, fig=fig, levs=levs )
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

    
        ax.text( 0.5, 0.99, ft_info,
                 fontsize=11, transform=ax.transAxes,
                 ha="center",
                 va='top', bbox=bbox,
                 )
    

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
    
#        ax.text( 0.99, 0.99, mslp_txt,
#                  fontsize=11, transform=ax.transAxes,
#                  ha="right",
#                  va='top',
#                  bbox=bbox,
#                  zorder=5,
#                 )

#    fig.suptitle( "Analyzed MSLP (Pa)")

    ofig = "Fcst_s{0:}_{1:0=3}h_BT_B{2:0=2}".format( stime.strftime('%m%d%H'), fth, band )
    plot_or_save( quick=quick, opath="png/1p_fcst_tbb/{0:}".format( exp ), ofig=ofig )   

###########



#etime = stime 

top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020"
exp = "D2/NOHIM8_4km_NP2304"
exp = "D2/NOHIM8_4km_NP2304_alhpa_v_s_lb3000"
#exp = "D2/NOHIM8_4km_NP2304_cfill_s0.99"
stime0 = datetime( 2020, 8, 29, 6, 0 )
tint = timedelta( hours=12)
stime = datetime( 2020, 8, 30, 12, 0 )
#etime = datetime( 2020, 9, 4, 0, 0 )
etime = stime

#exp = "D1/D1_20210629"
#stime0 = datetime( 2020, 8, 29, 0, 0 )
#tint = timedelta( hours=24)
#stime = datetime( 2020, 8, 29, 0, 0 )
#etime = datetime( 2020, 9, 4, 0, 0 )

band = 13
band = 9

time = stime
while time <= etime:
   main( stime=stime0, ftime=time, top=top, exp=exp, band=band )
   time += tint

