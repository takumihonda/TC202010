import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import prep_proj_multi_cartopy, plot_cbar, plot_or_save, setup_grids_cartopy, read_nc, get_besttrack

import cartopy.crs as ccrs
import cartopy.feature as cfeature

quick = True
#quick = False

lons = 120
lone = 155

lats = 15
late = 50

def main( time=datetime( 2020, 9, 5, 0, 0 ), central_longitude=130,
          hpa=500, ftsec=86400 ):

    tit_l = [ "TOMITA08", "SN14", ]

    var_l = []
    var2_l = []

    tlons, tlats, tslps, ttimes = get_besttrack()

    for i, tit in enumerate( tit_l ): 
      fn = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/D1/D1_{0:}/{1:}/fcst_sno_np00001/mean/p_history.pe000000.nc".format( tit, time.strftime('%Y%m%d%H%M%S'), )
      print( fn )
      if i == 0:
         prs = read_nc( fn=fn, nvar='pressure' )[:] # hpa
         ftsecs = read_nc( fn=fn, nvar='time' )[:]
 
         lon2d = read_nc( fn=fn, nvar='lon' )[:]
         lat2d = read_nc( fn=fn, nvar='lat' )[:]

         lev = np.argmin( np.abs( prs - hpa ) )
         tlev = np.argmin( np.abs( ftsecs - ftsec ) )
      qhyd_ = read_nc( fn=fn, nvar='QHYDprs' )[tlev,lev,:,:] * 1.e3
      mslp_ = read_nc( fn=fn, nvar='MSLP' )[tlev,:,:] * 1.e-2 # hPa

      var_l.append( qhyd_ )
      var2_l.append( mslp_ )

    x2d_l = [ lon2d, lon2d,  ]
    y2d_l = [ lat2d, lat2d,  ]

    fig = plt.figure( figsize=( 14,5 ) )
    fig.subplots_adjust( left=0.05, bottom=0.05, right=0.95, top=0.95,
                         wspace=0.15, hspace=0.05)
 
    ax_l = prep_proj_multi_cartopy( fig, xfig=2, yfig=1, proj='PlateCarree',
                         central_longitude=central_longitude )
  
    xticks = np.arange( 40, 205, 10 )
    yticks = np.arange( 0, 85, 10 )

    res = '50m'

    fs = 8

    clw = 0.5
    cc = 'k'
    coast = cfeature.NaturalEarthFeature( 'physical', 'coastline', res,
                                         facecolor='none',
                                         edgecolor=cc, )

    land = cfeature.NaturalEarthFeature( 'physical', 'land', res,
                                         edgecolor='face',
                                         facecolor=cfeature.COLORS['land'] )

    ocean = cfeature.NaturalEarthFeature( 'physical', 'ocean', res,
                                         edgecolor='face',
                                         facecolor=cfeature.COLORS['water'] )

    # original data is lon/lat coordinate
    data_crs = ccrs.PlateCarree()

    lons = np.min( lon2d ) - 5
    lats = np.min( lat2d ) - 5

    lone = np.max( lon2d ) + 5
    late = np.max( lat2d ) + 5

#    lons = 105 
#    lone = 165 
#    late = 50
#    lats = 5
 
#    lons = 110 
#    lone = 150 
#    late = 49
#    lats = 8

    cmap = plt.cm.get_cmap("jet")
    cmap.set_under( 'w', alpha=0.0 )
    levs = np.array( [ 0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 5 ] )

    levs_mslp = np.arange( 800, 1200, 4 )

    for i, ax in enumerate( ax_l ):

        setup_grids_cartopy( ax, xticks=xticks, yticks=yticks,
                                 fs=fs, lw=0.25, color='k' )

        ax.set_extent([ lons, lone, lats, late ], crs=data_crs )
    
        ax.add_feature( coast, zorder=1, linewidth=clw )
    
#        ax.add_feature( land  )
#        ax.add_feature( ocean )

        SHADE = ax.contourf( x2d_l[i], y2d_l[i], var_l[i],
                       cmap=cmap, levels=levs, 
                       extend='both',
                       transform=data_crs )
 
        CONT = ax.contour( x2d_l[i], y2d_l[i], var2_l[i],
                       levels=levs_mslp, colors='k',
                       linewidths=1.0, 
                       transform=data_crs )
 

        ax.text( 0.5, 1.01, tit_l[i],
                  fontsize=10, transform=ax.transAxes,
                  ha="center",
                  va='bottom',
                 )
    
        lc = 'k'
        ax.plot( lon2d[0,:], lat2d[0,:], color=lc,
                 transform=data_crs )
        ax.plot( lon2d[-1,:], lat2d[-1,:], color=lc,
                 transform=data_crs )
        ax.plot( lon2d[:,-1], lat2d[:,-1], color=lc,
                 transform=data_crs )
        ax.plot( lon2d[:,0], lat2d[:,0], color=lc,
                 transform=data_crs )

        ax.text( 1.0, 0.99, 'MSLP: {0:.0f} hPa'.format( np.min( var2_l[i] ) ),
                 fontsize=10, transform=ax.transAxes,
                 ha="right",
                 va='top',
                )

        ax.plot( tlons, tlats, transform=data_crs, color='r' )

    ftime = ( time + timedelta( seconds=ftsec ) ).strftime('Valid: %H:%M UTC %m/%d/%Y')

    ax_l[-1].text( 1.0, 1.01, ftime,
              fontsize=10, transform=ax_l[-1].transAxes,
              ha="right",
              va='bottom',
             )
    
    ftday = ftsec / 86400

    print( ftime )
    tit = 'QHYD (g/kg) at {0:.0f}hPa (FT={1:.0f} days)'.format( prs[lev], ftday )
    fig.suptitle( tit, fontsize=13 )

    plot_cbar( ax_l[-1], shade=SHADE, fig=fig )
    plt.show()

#    sys.exit()   
   
    
#    ofig = "Him8_B{0:0=2}_{1:}".format( band, time.strftime('%Y%m%d%H%M'), )
#    plot_or_save( quick=quick, opath="png/Him8", ofig=ofig )   

###########
time = datetime( 2020, 8, 28, 0, 0 )

ftsec_max = 5*86400

ftsec = 86400
while ftsec <= ftsec_max:
   main( time=time, ftsec=ftsec )
   ftsec += 86400

