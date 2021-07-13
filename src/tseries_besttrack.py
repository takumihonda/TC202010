import numpy as np
import matplotlib.pyplot as plt

import matplotlib.dates as mdates

from datetime import datetime, timedelta

from tools_TC202010 import get_besttrack, plot_or_save

quick = False

def main( stime=datetime( 2020, 8, 26, 0 ), etime=datetime( 2020, 9, 6, 0, )):
    tlons, tlats, tslps, ttimes = get_besttrack()

    fig, ax1 = plt.subplots( 1, 1, figsize=( 8, 6.5 ) )   

    ymin = 900
    ymax = 1010

    yticks = np.arange( ymin, ymax+10, 10 )

    ax1.plot( ttimes, tslps, )

    ax1.xaxis.set_major_locator( mdates.HourLocator(interval=24) )
    ax1.xaxis.set_major_formatter( mdates.DateFormatter('%H%M\n%m/%d') )

    ax1.set_xlim( stime, etime )
    ax1.set_ylim( ymin, ymax )

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

    ax1.plot( [ sdate_slp, edate_slp ], [ s_slp, e_slp ] )

    ofig = "1p_MSLP_tseries_besttrac"
    plot_or_save( quick=quick, opath="png/1p_MSLP_tseries", ofig=ofig )   

main()
