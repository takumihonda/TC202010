import numpy as np
from netCDF4 import Dataset
from datetime import datetime

import os

from mpl_toolkits.basemap import Basemap
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def prep_proj_multi( method="merc", ax_l=[], res="c", ll_lon=120, ur_lon=155, ll_lat=15, ur_lat=50,
                     blon=135, blat=35, lat2=40,
                     fs=10, zorder=2, contc='burlywood', cont_alp=0.2,
                     cc='k', lw=0.1, cw=0.2, lc='k' ):

    ddeg = 0.2 # deg

    m_l = []
    contc = contc

    pdlat = 5.0
    pdlon = 5.0
    #pdlat = 1.0
    #pdlon = 2.0

    for ax in ax_l:
      m = Basemap( projection=method,resolution = res,
                   llcrnrlon = ll_lon,llcrnrlat = ll_lat,
                   urcrnrlon = ur_lon,urcrnrlat = ur_lat,
                   lat_0 = blat, lat_1 = lat2,
                   lat_2 = lat2, lon_0 = blon,
                   ax = ax )
      m_l.append(m)

      m.drawcoastlines( linewidth=cw, color=cc, zorder=zorder)
      m.fillcontinents( color=contc, lake_color='w', zorder=0, alpha=cont_alp)
      m.drawparallels( np.arange(0,70,pdlat),labels=[1,0,0,0],fontsize=fs,color=lc,linewidth=lw)
      m.drawmeridians( np.arange(0,180,pdlon),labels=[0,0,0,1],fontsize=fs,color=lc,linewidth=lw)


    return( m_l )

def read_Him8_obs( time=datetime( 2020, 9, 10, 0), band=13 ):

    top = "/data9/honda/himawari_real/HIMAWARI-8/HISD/Hsfd"

    idir = top + time.strftime('/%Y%m/%d/%Y%m%d%H00/%M/')
    fn = 'B{0:0=2}/DLON0.02_DLAT0.02_HS_H08_{1:}_{2:}_B{3:0=2}_FLDK.nc'.format( band, time.strftime('%Y%m%d'), time.strftime('%H%M'), band  )

    print( idir + fn )

    nc = Dataset( idir + fn, "r", format="NETCDF4" )
    lon1d = nc.variables['longitude'][:]
    lat1d = nc.variables['latitude'][:]
    tbb = nc.variables['tbb'][:]
    nc.close()


    return( tbb, lon1d, lat1d )

def cmap_Him8():

    colors1 = plt.cm.jet_r(np.linspace(0, 1, 128 ))
    colors2 = plt.cm.binary(np.linspace(0., 1, 128 )) # w/k
    colors = np.vstack((colors1, colors2))
    cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
    levs = np.arange( 200, 304, 4 )    

    return( cmap, levs )

def plot_cbar( ax=None, shade=None, fig=None, ori='vertical', fs=7 ):

    if fig is None:
       ax_cb=None
    else:
       pos = ax.get_position()
       cb_width = 0.01
       cb_height = pos.height*0.9
       ax_cb = fig.add_axes( [pos.x1+0.005, pos.y1-cb_height, cb_width, cb_height] )
    cb = plt.colorbar( shade, cax=ax_cb,
                       orientation=ori, ) #ticks=levs[::2] )
    cb.ax.tick_params( labelsize=fs )

def plot_or_save( quick=True, opath="png", ofig="fig" ):

    if not quick:
       os.makedirs(opath, exist_ok=True)

       ofig = os.path.join(opath, ofig + ".png")
       plt.savefig(ofig,bbox_inches="tight", pad_inches = 0.1)
       print(ofig)
       plt.clf()
    else:
       print(ofig)
       plt.show()

