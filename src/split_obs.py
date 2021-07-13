import numpy as np
from datetime import datetime, timedelta

import sys

from tools_TC202010 import read_obs_letkf, write_obs_letkf

DEBUG = True

def main( time=datetime(2020, 9, 1, 0 ), dsec=600, OVERW=False):


    obs = read_obs_letkf( time=time )
    if DEBUG:
       lons = obs[:,2]
       lats = obs[:,3]
       print( np.min( lons ), np.max( lons ) )
       print( np.min( lats ), np.max( lats ) )
       sys.exit()
    #head = [ "", "elm", "lon", "lat", "lev", "dat", "err", "typ", "dif", "" ]

    dif = obs[:,8]

    tmin = -3*3600
    tmax = 3*3600

    tot = 0
    t = tmin + dsec
    time0 = time - timedelta( seconds=tmin )
    while t <= tmax:
        tmin_ = t - dsec
        tmax_ = t 

        if t == tmin + dsec:
           cnt = len( dif[ (dif <= tmax_ ) ] )
           obs_ = obs[dif<=tmax_]
        else:
           cnt = len( dif[ ( dif > tmin_ ) & (dif <= tmax_ ) ] )
           obs_ = obs[ ( dif > tmin_ ) & (dif <= tmax_ ) ] 

        time_ = time0 + timedelta( seconds=tmax_ )
        obs_[:,8] = 0.0 # dif == 0.0
        write_obs_letkf( obs=obs_, time=time_, foot="10min", OVERW=OVERW )

#        ctime_ = time_.strftime('%Y%m%d%H%M%S.dat')

        t += dsec
        tot += cnt

    print( "tot", tot )

time = datetime( 2020, 9, 1, 0, 0 )
dsec = 600
OVERW = True


stime = datetime( 2020, 9, 1, 0, 0 )
etime = datetime( 2020, 9, 8, 0, 0 )

stime = datetime( 2020, 8, 29, 0, 0 )
etime = datetime( 2020, 8, 30, 0, 0 )

stime = datetime( 2020, 8, 28, 0, 0 )
etime = datetime( 2020, 8, 29, 0, 0 )

stime = datetime( 2020, 8, 27, 0, 0 )
etime = datetime( 2020, 8, 28, 0, 0 )

time = stime

while time <= etime:

   main( time=time, dsec=dsec, OVERW=OVERW )
   time += timedelta( hours=6 )
