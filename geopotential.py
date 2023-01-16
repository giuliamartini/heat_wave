import netCDF4 as nc
import numpy as np
import pandas as pd
from datetime import datetime
import math
import cftime 
fn = '/home/giulia/geopotential_mean_no29feb.nc'
ds = nc.Dataset(fn,'r')
lat=ds.variables['latitude']
lat=np.array(lat[:])
lon = np.array(ds.variables['longitude'][:] )
time=ds.variables['time']
dates=cftime.num2pydate(time[:], time.units, calendar='standard')
dates = pd.to_datetime(dates)
dates=np.array(list(map(lambda x: x.date(), dates)))
#z=np.array(ds.variables['z'][:,:,:]) #z(time,lat,lon)

#print(geo[0][0][0])
#res=np.reshape(geop[0],(len(lat),len(lon)))
#print(res)

def strtodate(day_str):
    result= datetime.strptime(day_str, '%Y-%m-%d').date()
    return pd.to_datetime(result)

#primo giorno e durata delle hw
df = pd.read_csv('/home/giulia/tesipy/properties_2019.csv')
first_day = np.array(df['firstday'])
first_day = np.array(list(map(strtodate, first_day)))
first_day=np.array(list(map(lambda x: x.date(), first_day)))
duration = df['duration']

def find_date(dates,first_day):
    indexes=np.array(list(map(lambda x: np.where(dates==x),first_day)))
    return indexes

class Event:
    def __init__(self,first_day,duration):
        self.first_day=first_day
        self.duration=duration


def r(event1,event2):
    num=np.sum(np.multiply(event1,event2))
    den=math.sqrt(np.sum(np.multiply(event1,event1)))*math.sqrt(np.sum(np.multiply(event2,event2)))
    return num/den

def distance(event_map1,event_map2):
    r=r(event_map1,event_map2)
    return (1-r)

#print(r(np.array(ds.variables['z'][0,:,:]),np.array(ds.variables['z'][1,:,:])))

def window_days_int(year,day):
    if (year*90+day)>=440:
        return np.arange(year*90+day-10,450,1)
    if (year*90 +day)<=10:
        return np.arange(0,day+11,1)
    else:
        return np.arange(year*90+day-10,year*90+day+10,1)

def wdy_int(years,day):
    days=np.array([])
    for year in years:
        days=np.append(days,window_days_int(year,day))
    return days

def day_mean(days, ds):
    cluster_map=[]
    for day in days:
        cluster_map.append(np.array(ds.variables['z'][day,:,:]))
    cluster_map=np.array(cluster_map)
    mean=np.mean(cluster_map, axis=0) 
    return mean


years=np.array([0,1,2,3,4])
days=wdy_int(years,7)
print(day_mean(days,ds))
#print(first_day)
