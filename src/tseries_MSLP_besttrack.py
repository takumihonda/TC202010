import numpy as np
import sys
import matplotlib.pyplot as plt

import matplotlib.dates as mdates

from datetime import datetime, timedelta

from tools_TC202010 import get_besttrack, plot_or_save, read_nc

quick = True
#quick = False

def main( stime=datetime( 2020, 8, 26, 0 ), etime=datetime( 2020, 9, 6, 0, ), exp='D1_20210629', name='maysak' ):

    tlons, tlats, tslps, ttimes = get_besttrack( name=name )

    dll = 5.0

    mslp_l = []
    time_l = []

    time_ = stime
    while time_ <= etime:
        print( time_ )
        fn = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/D1/{0:}/{1:}/hist_sno_np00001/mean/p_history.pe000000.nc".format( exp, time_.strftime('%Y%m%d%H%M%S') )
        try:
           mslp2d = read_nc( nvar="MSLP", fn=fn )[0,:,:]
           lon2d = read_nc( nvar="lon", fn=fn )[:,:]
           lat2d = read_nc( nvar="lat", fn=fn )[:,:]
           tclon = tlons[ ttimes==time_ ]
           tclat = tlats[ ttimes==time_ ]
           print( "check", ttimes[ ttimes==time_ ], np.min( mslp2d ) )
           mslp2d = np.where( ( np.abs( lon2d - tclon ) < dll ) |
                              ( np.abs( lat2d - tclat ) < dll ),
                               mslp2d, np.nan )
#           mslp2d[ ( np.abs( lon2d - tclon ) > dll ) | 
#                   ( np.abs( lat2d - tclat ) > dll ) ] = np.nan
           mslp_l.append( np.nanmin( mslp2d )*0.01 )
           time_l.append( time_ )
        except:
           print( "No data ", time_)
        time_ += timedelta( hours=6 )
 
    fig, ax1 = plt.subplots( 1, 1, figsize=( 8, 6.5 ) )   
    fig.subplots_adjust( left=0.1, bottom=0.07, right=0.96, top=0.95,
                         wspace=0.1, hspace=0.3)

    ymin = 910
    ymax = 1010

    yticks = np.arange( ymin, ymax+10, 10 )

    ax1.plot( ttimes, tslps, color='k', ls='solid', lw=2.0, label='Best track' )

    ax1.plot( time_l, mslp_l, color='b', ls='solid', lw=2.0, label=exp )

    ax1.xaxis.set_major_locator( mdates.HourLocator(interval=24) )
    ax1.xaxis.set_major_formatter( mdates.DateFormatter('%H%M\n%m/%d') )

    ax1.set_xlim( stime, etime )
    ax1.set_ylim( ymin, ymax )

    ax1.set_ylabel( 'MSLP (hPa)', fontsize=12 )

    time_l = []
    time_ = stime
    while time_ <= etime:
        time_l.append( time_ )

        time_ += timedelta( days=1 )

    ax1.vlines( x=time_l, ymin=ymin, ymax=ymax, 
                color='gray', lw=1.0, ls='dashed' )

    ax1.set_yticks( yticks, minor=False )
    ax1.hlines( y=yticks, xmin=stime, xmax=etime, 
                color='gray', lw=1.0, ls='dashed' )

    # SLP reduction per day
    rat_slp = 24

    s_slp = 1000.0
    sdate_slp = datetime( 2020, 8, 28, 0 )
    dday = 4

    edate_slp = sdate_slp + timedelta( days=dday )
    e_slp = s_slp - dday * rat_slp

    ax1.plot( [ sdate_slp, edate_slp ], [ s_slp, e_slp ], ls='dashed', lw=3.0,
              color='orange', label='RI')

    ax1.legend( loc='lower left')

    fig.suptitle( name.upper(), fontsize=13 )

    ofig = "1p_MSLP_tseries_{0:}_besttrac".format( exp )
    plot_or_save( quick=quick, opath="png/1p_MSLP_tseries", ofig=ofig )   

######
exp = "D1_20210629"
main( exp=exp)
