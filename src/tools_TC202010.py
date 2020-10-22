import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta

import os
import sys

from mpl_toolkits.basemap import Basemap
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

nx_gfs = 720
ny_gfs = 361

def read_nc( nvar="MSLP", fn="" ):

    nc = Dataset( fn, "r", format="NETCDF4" )
    var = nc.variables[nvar][:]
    nc.close()

    return( var )

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

def get_gfs_grads_latlon():
   lon = np.arange(   0.0, 360.0, 0.5 )
   lat = np.arange( -90.0,  90.5, 0.5 )
   lon2d, lat2d = np.meshgrid( lon,lat )

   if len( lon ) != nx_gfs or len( lat ) != ny_gfs:
      print( "Wrong GFS lat/lon")
      sys.exit()
  
   return( lon2d, lat2d )

def read_gfs_mslp_grads( time=datetime( 2020, 9, 5, 0, 0 ) ):
    top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/TC202010/ncepgfs"

    fn = top + time.strftime('/%Y%m%d%H/sfc_%Y%m%d%H%M%S.grd')

    try:
       infile = open( fn )
    except:
       print( fn )
       print("Failed to open")
       sys.exit()

    count = nx_gfs * ny_gfs

    rec = 0
    infile.seek( rec*4 )
    tmp2d = np.fromfile( infile, dtype=np.dtype('>f4'), count=count )
    input2d = np.reshape(tmp2d, (ny_gfs,nx_gfs) )
    input2d[ input2d == 9.999e20 ] = np.nan 
    infile.close

    return( input2d )

def read_LIDEN( time=datetime( 2020, 9, 5, 0, 0 ) ):


    top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/TC202010/LIDEN/raw_data" 
    fn_npz = os.path.join( top, time.strftime('liden%Y%m%d.npz') )
    
    try:
       data = np.load( fn_npz, allow_pickle=True )
       return( data["lons"], data["lats"], data["times"] )
    except:
       print( "make npz from csv")

       import csv
       fn = os.path.join( top, time.strftime('liden%Y%m%d.csv') )
   
       times = [] 
       lons = []
       lats = []
       print( fn )
       with open( fn ) as f:
           reader = csv.reader( f )
           for line in reader:
               d = int( line[0] ) 
               m = int( line[1] )
               y = int( line[2] )
               h = int( line[3] )
               n = int( line[4] )
               s = int( line[5] )
               lat = int( line[10] ) 
               lon = int( line[11] ) 
               times.append( datetime( year=y, month=m, day=d, hour=h, minute=n, second=s ) )
               lons.append( lon )
               lats.append( lat )
   
       lons = np.array( lons ) / 10000.0
       lats = np.array( lats ) / 10000.0
       times = np.array( times )
   
       np.savez( fn_npz, lons=lons, lats=lats, times=times )
   
       return( lons, lats, times )

def read_LIDEN_all( ):

    top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/TC202010/LIDEN/raw_data" 
    fn_npz = os.path.join( top, 'liden_all.npz' )

    try:
       data = np.load( fn_npz, allow_pickle=True )
       return( data["lons"], data["lats"], data["times"] )
    except:
       print( "make npz from csv")

       stime = datetime( 2020, 9, 3, 0 )
       etime = datetime( 2020, 9, 7, 0 )


       time = stime
       while time <= etime:
          lons_, lats_, times_ = read_LIDEN( time=time )

          if time > stime:
             lons = np.append( lons, lons_ )
             lats = np.append( lats, lats_ )
             times = np.append( times, times_ )
          else:
             lons = np.copy( lons_ )
             lats = np.copy( lats_ )
             times = np.copy( times_ )
          time += timedelta( days=1 )

       np.savez( fn_npz, lons=lons, lats=lats, times=times )
   
       return( lons, lats, times )
