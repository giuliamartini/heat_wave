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

def strtodate(day_str):
    result= datetime.strptime(day_str, '%Y-%m-%d').date()
    return pd.to_datetime(result)

#primo giorno e durata delle hw
df = pd.read_csv('/home/giulia/tesipy/properties_2018.csv')
first_day = np.array(df['firstday'])
first_day = np.array(list(map(strtodate, first_day)))
first_day=np.array(list(map(lambda x: x.date(), first_day)))
duration = df['duration']

class Event:
    def __init__(self,first_day,duration):
        self.first_day=first_day
        self.duration=duration


def get_hw_days(dates,first_day,duration):
    begin=np.array(list(map(lambda x: np.where(dates==x),first_day)))
    indexes=[]
    for i in range(0,len(duration)):
        indexes.append(np.arange(begin[i],begin[i]+1+duration[i],1))
    return indexes


print(get_hw_days(dates,first_day,duration))



def r(event1,event2):
    num=np.sum(np.multiply(event1,event2))
    den=math.sqrt(np.sum(np.multiply(event1,event1)))*math.sqrt(np.sum(np.multiply(event2,event2)))
    return num/den

def distance(event_map1,event_map2):
    coeff_corr=r(event_map1,event_map2)
    return (1-coeff_corr)

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
    #lambda x: np.append(days,window_days_int(x,day)),years
    return days

def day_mean(day_, ds):
    days=wdy_int(np.array([0,1,2,3,4]),day_)
    cluster_map=[]
    for day in days:
        cluster_map.append(np.array(ds.variables['z'][day,:,:]))
    cluster_map=np.array(cluster_map)
    mean=np.mean(cluster_map, axis=0) 
    return mean

def day_percentile(day_,ds,p_value):
    days=wdy_int(np.array([0,1,2,3,4]),day_)
    cluster_map=[]
    for day in days:
        cluster_map.append(np.array(ds.variables['z'][day,:,:]))
    cluster_map=np.array(cluster_map)
    pct=np.percentile(cluster_map,p_value, axis=0) 
    return pct

def get_anomalies(ds,day_,p_value):
    check_map=day_percentile(day_,ds,p_value)-ds.variables['z'][day_,:,:]
    anomalies= np.where(check_map<0)
    return anomalies

b=get_anomalies(ds,5,40)
print(b)


#sulle righe=long
#sulle colonne=lat
a=day_percentile(5,ds,90)
print(a[b])
#print(len(a[:,0]))
#print(len(lat))

#hw=get_hw_days(dates,first_day,duration)
#print(hw)
#cluster_rs=[]
#for h in hw:
#    
#    for d in h:
#        cluster_rs.append(r(np.array(ds.variables['z'][d,:,:]),day_mean(d,ds)))
#    
#
#print(cluster_rs)
#print(r(np.array(ds.variables['z'][5,:,:]),np.array(ds.variables['z'][6,:,:])))
#print(distance(np.array(ds.variables['z'][5,:,:]),np.array(ds.variables['z'][250,:,:])))
#print(first_day)
