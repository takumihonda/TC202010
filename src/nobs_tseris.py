import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

import matplotlib.pyplot as plt

import sys

from tools_TC202010 import read_score


def main( top='', stime=datetime(2020, 9, 1, 0 ), etime=datetime(2020, 9, 1, 0) ):

    time = stime
    while time < etime:
       data_ = read_score( top=top, time=time )
       if time == stime:
          # initiate a dictionary 
          data = dict( data_ )
          data.update( {'time': [ stime, stime ] } )
       else:
          for key in data.keys():
              if key == 'time':
                 data[key] = data[key] + [ time, time ]
              else:
                 data[key] = data[key] + data_[key] 

       time += timedelta( hours=6 )
 

    fig, ( ( ax1, ax2, ax3, ax4, ax5))  = plt.subplots( 5, 1, figsize=( 8, 9.5 ) )   
    ax_l = [ ax1, ax2, ax3, ax4, ax5] 

    tit_l = [ 'U', 'V', 'T', 'PS', 'Q' ]
    ymax_l = [ 50000, 50000, 5000, 1000, 5000 ]
    ymin_l = [ 0, 0, 0, 0, 0 ]

    for key in data.keys():
        if 'NOBS_U'    in key:
           ax = ax1
        elif 'NOBS_V'  in key:
           ax = ax2
        elif 'NOBS_T'  in key:
           ax = ax3
        elif 'NOBS_PS' in key:
           ax = ax4
        elif 'NOBS_Q'  in key:
           ax = ax5
        else:
           print( "skip ", key )
           continue

        ls = 'solid'
        c = 'k'

        ax.plot( data['time'], data[key], color=c, ls=ls )

    stime_ = stime - timedelta( hours=stime.hour )
    etime_ = etime - timedelta( hours=etime.hour )
 
    for i, ax in enumerate( ax_l ):

        ax.text( 0.5, 0.99, tit_l[i],
                 fontsize=13, transform=ax.transAxes,
                 ha="center",
                 va='top',
                 )
        
#        ax.hlines( y=0.0, xmin=stime_, xmax=etime_, ls='dotted', 
#                   color='k', lw=1.0 )

        ax.set_xlim( stime_, etime_ )
        ax.set_ylim( ymin_l[i], ymax_l[i] )

        if i == 4:
           ax.xaxis.set_major_locator( mdates.HourLocator(interval=24) )
           #ax.xaxis.set_major_formatter( mdates.DateFormatter('%d%H\n%m/%d') )
           ax.xaxis.set_major_formatter( mdates.DateFormatter('%d') )
           #ax.xaxis.set_major_formatter( mdates.DateFormatter('%m/%d') )
        else:
           ax.set_xticks([], [])

    plt.show()
    sys.exit()

#    time = stime



stime = datetime( 2020, 8, 16, 6, 0 )
etime = datetime( 2020, 9, 2, 0, 0 )

top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/TC2020/D1/D1_20210629"

#stime = datetime( 2017, 6, 16, 6, 0 )
#etime = datetime( 2017, 7, 5, 0, 0 )
#top = "/data_ballantine02/miyoshi-t/honda/SCALE-LETKF/scale-5.4.3/OUTPUT/KYUSHU2017_D1_20210629"

time = stime
main( top=top, stime=stime, etime=etime, )
