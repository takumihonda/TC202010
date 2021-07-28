import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import prep_proj_multi_cartopy, setup_grids_cartopy, plot_cbar, plot_or_save, read_nc, cmap_Him8, read_Him8_obs, band2wavelength

import cartopy.crs as ccrs
import cartopy.feature as cfeature

quick = True
#quick = False



def main( ftime=datetime( 2020, 9, 5, 0, 0 ), top="",
          band=9, ):


    tbb, lon1d, lat1d = read_Him8_obs( time=ftime, band=band )
    lon2d, lat2d = np.meshgrid( lon1d, lat1d )

 
    tvar = r'BT (K)'

    fig = plt.figure( figsize=( 8,10 ) )

    fig.subplots_adjust( left=0.05, bottom=0.05, right=0.95, top=0.95,
                         wspace=0.1, hspace=0.3)
   
   

    lone, lons = 150.0793914794922, 105.92059326171875
    late, lats = 51.614158630371094, 5.733283519744873


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


    lon2d_l = [ lon2d, ]
    lat2d_l = [ lat2d, ]
#    cvar_l = [ mslp_d1[0,:,:], ]    
    var_l = [ tbb[:,:] ]    

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

    tit1 = "{0:}".format( tvar )
#    mslp_txt = "MSLP:{0:.1f} hPa".format( mslp_min )

    ft_info = "Obs band {0:0=2} ({1:} µm)".format( band, band2wavelength( band=band ) )
    ofig = "Obs_{0:}_BT_B{1:0=2}".format( ftime.strftime('%m%d%H%M'), band )

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
    
        ctime = time.strftime('%H%M UTC %m/%d/%Y')
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

    plot_or_save( quick=quick, opath="png/1p_obs_tbb/", ofig=ofig )   

###########



#etime = stime 

top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020"
tint = timedelta( hours=12)


stime = datetime( 2020, 8, 29, 7, 0 )
#stime = datetime( 2020, 8, 30, 12, 0 )
etime = stime

band = 13
band = 10
#band = 8
#band = 9

time = stime
while time <= etime:
   main( ftime=time, band=band, )
   time += tint

