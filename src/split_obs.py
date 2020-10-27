import numpy as np
from datetime import datetime, timedelta


from tools_TC202010 import read_obs_letkf, write_obs_letkf



def main( time=datetime(2020, 9, 1, 0 ), dsec=600, OVERW=False):


    obs = read_obs_letkf( time=time )
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

time = stime

while time <= etime:

   main( time=time, dsec=dsec, OVERW=OVERW )
   time += timedelta( hours=6 )
