import numpy as np
import sys
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

from tools_TC202010 import read_Him8_obs, cmap_Him8, prep_proj_multi_cartopy, plot_cbar, plot_or_save, setup_grids_cartopy, read_nc

import cartopy.crs as ccrs
import cartopy.feature as cfeature

quick = True
#quick = False

lons = 120
lone = 155

lats = 15
late = 50

def main( time=datetime( 2020, 9, 5, 0, 0 ), central_longitude=130 ):

    tit_l = [ "QI", "QS", "QG"]

    exp = 'NOHIM8_4km'
#    exp = 'NOHIM8_4km_param1'

    fn1 = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/D2/{0:}/20200827120000/fcst_sno_np00001/0001/QI.nc".format( exp )
    fn2 = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/D2/{0:}/20200827120000/fcst_sno_np00001/0001/QS.nc".format( exp )
    fn3 = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/D2/{0:}/20200827120000/fcst_sno_np00001/0001/QG.nc".format( exp )

    zlev = 40
    tlev = 1
    qhyd1 = read_nc( fn=fn1, nvar='QI' )[tlev,:,:,:]
    qhyd2 = read_nc( fn=fn2, nvar='QS' )[tlev,:,:,:]
    qhyd3 = read_nc( fn=fn3, nvar='QG' )[tlev,:,:,:]

    lon2d = read_nc( fn=fn1, nvar='lon' )[:]
    lat2d = read_nc( fn=fn1, nvar='lat' )[:]
    cz = read_nc( fn=fn1, nvar='CZ' )[2:-2]

    print( cz.shape, cz[zlev])

#    qhyd1 = np.sum( qhyd1, axis=0 ) * 1.e3
#    qhyd2 = np.sum( qhyd2, axis=0 ) * 1.e3
    qhyd1 = qhyd1[zlev,:,:] * 1.e3
    qhyd2 = qhyd2[zlev,:,:] * 1.e3
    qhyd3 = qhyd3[zlev,:,:] * 1.e3


    data_l = [ qhyd1, qhyd2, qhyd3 ]
    x2d_l = [ lon2d, lon2d, lon2d ]
    y2d_l = [ lat2d, lat2d, lat2d ]

    fig = plt.figure( figsize=( 10,4 ) )
    fig.subplots_adjust( left=0.05, bottom=0.05, right=0.95, top=0.9,
                         wspace=0.15, hspace=0.05)
 
    ax_l = prep_proj_multi_cartopy( fig, xfig=3, yfig=1, proj='PlateCarree',
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

    lons = 105 
    lone = 165 
    late = 50
    lats = 5
 
    lons = 110 
    lone = 150 
    late = 49
    lats = 8

    cmap = plt.cm.get_cmap("jet")
    cmap.set_under( 'w', alpha=0.0 )
    levs = np.array( [ 0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 5 ] )

    for i, ax in enumerate( ax_l ):

        setup_grids_cartopy( ax, xticks=xticks, yticks=yticks,
                                 fs=fs, lw=0.25, color='k' )

        ax.set_extent([ lons, lone, lats, late ], crs=data_crs )
    
        ax.add_feature( coast, zorder=1, linewidth=clw )
    
#        ax.add_feature( land  )
#        ax.add_feature( ocean )

        print( i, np.max( data_l[i]) )

        SHADE = ax.contourf( x2d_l[i], y2d_l[i], data_l[i],
                       cmap=cmap, levels=levs, 
                       extend='both',
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


    tit = 'Hydrometeors (g/kg) at Z={0:.1f}km'.format( cz[zlev]*0.001 )
    fig.suptitle( tit, fontsize=13 )

    plot_cbar( ax_l[-1], shade=SHADE, fig=fig )
    plt.show()
    sys.exit()   
   
    

###########
time = datetime( 2020, 9, 5, 0, 0 )

stime = datetime( 2020, 9, 1, 0, 0 )
stime = datetime( 2020, 8, 27, 12, 0 )
stime = datetime( 2020, 8, 27, 18, 0 )
etime = datetime( 2020, 9, 6, 12, 0 )


dh = 1
etime = stime

time = stime
while time <= etime:
   main( time=time, )
   time += timedelta( hours=dh )

