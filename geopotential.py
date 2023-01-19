import netCDF4 as nc
import numpy as np
import pandas as pd
from datetime import datetime
import math
import cftime


fn = '/home/giulia/geopotential_mean_no29feb.nc'
ds = nc.Dataset(fn, 'r')
lat = ds.variables['latitude']
lat = np.array(lat[:])
lon = np.array(ds.variables['longitude'][:])
time = ds.variables['time']
dates = cftime.num2pydate(time[:], time.units, calendar='standard')
dates = pd.to_datetime(dates)
dates = np.array(list(map(lambda x: x.date(), dates)))
# z=np.array(ds.variables['z'][:,:,:]) #z(time,lat,lon)


def strtodate(day_str):
    result = datetime.strptime(day_str, '%Y-%m-%d').date()
    return pd.to_datetime(result)


def get_hw_days(dates, first_day, duration):
    begin = np.array(list(map(lambda x: np.where(dates == x), first_day)))
    indexes = []
    for i in range(0, len(duration)):
        indexes.append(np.arange(begin[i], begin[i]+1+duration[i], 1))
    return indexes


def r(event1, event2):
    num = np.sum(np.multiply(event1, event2))
    den = math.sqrt(np.sum(np.multiply(event1, event1))) * \
        math.sqrt(np.sum(np.multiply(event2, event2)))
    return num/den


def distance(event_map1, event_map2):
    coeff_corr = r(event_map1, event_map2)
    return (1-coeff_corr)


def window_days_int(year, day):
    if (year*90+day) >= 440:
        return np.arange(year*90+day-10, 450, 1)
    if (year*90 + day) <= 10:
        return np.arange(0, day+11, 1)
    else:
        return np.arange(year*90+day-10, year*90+day+10, 1)


def woy_int(year):
    if(year <= 4):
        return np.arange(0, year+5, 1)
    if(year >= 58):
        return np.arange(year-5, 63, 1)  # controll range
    else:
        return np.arange(year-5, year+5, 1)


def wdy_int(years, day):
    days = np.array([])
    for year in years:
        days = np.append(days, window_days_int(year, day))
    #lambda x: np.append(days,window_days_int(x,day)),years
    return days


def day_mean(day_, year, ds):
    days = wdy_int(woy_int(year), day_)
    cluster_map = []
    for day in days:
        cluster_map.append(np.array(ds.variables['z'][day, :, :]))
    cluster_map_np = np.array(cluster_map)
    mean = np.mean(cluster_map_np, axis=0)
    return mean

def day_percentile(day_, year, ds, p_value):
    days = wdy_int(woy_int(year), day_)
    cluster_map = []
    for day in days:
        cluster_map.append(np.array(ds.variables['z'][day, :, :]))
    cluster_map_np = np.array(cluster_map)
    pct = np.percentile(cluster_map_np, p_value, axis=0)
    return pct


def get_anomalies(ds, day_, year, p_value):
    check_map = day_percentile(day_, year, ds, p_value) - \
        ds.variables['z'][day_, :, :]
    anomalies = np.where(check_map < 0)
    return anomalies


def get_anomalies_map(ds, day_, year):
    anomalies_map = day_mean(day_, year, ds)-ds.variables['z'][day_, :, :]
    return anomalies_map


class HeatWave:
    """contiente data del primo giorno di occorrenza della hw, durata, mappa di geopotenziale medio durante la hw/mappa delle anomalie"""

    def __init__(self, first_day, duration, geop_map):
        self.first_day = first_day
        self.duration = duration
        self.geop_map = geop_map

    def merge(self,other):
        self.geop_map=np.mean(np.array([self.geop_map,other.geop_map]),axis=0)
        self.first_day.append(other.first_day)
        self.duration.append(other.duration)
        return self


# sulle righe=long

cluster_heat_waves=np.array([])
cluster_heat_waves_anomalies=np.array([])

for i in range(0, 2):
    df = pd.read_csv('/home/giulia/tesipy/properties_'+str(i+2017)+'.csv')
    first_day = np.array(df['firstday'])
    first_day = np.array(list(map(strtodate, first_day)))
    first_day = np.array(list(map(lambda x: x.date(), first_day)))
    duration = df['duration']
    heat_waves_days = get_hw_days(dates, first_day, duration)
    cluster_rs_hw = []


    cluster_means_y = []
    cluster_anomalies_means_y = []

    for h in range(0,len(heat_waves_days)):
        geop_maps_hw=[]
        anomalies_maps_hw = []
        for d in heat_waves_days[h]:
            
            geop_maps_hw.append(ds.variables['z'][d,:,:])               
            anomalies_maps_hw.append(get_anomalies_map(ds, d, i))

         
        geop_maps_hw_np=np.array(geop_maps_hw)  
        mean_geop=np.mean(geop_maps_hw_np,axis=0)    
        cluster_means_y.append(mean_geop)
        anomalies_maps_hw_np = np.array(anomalies_maps_hw)
        anomalies_mean = np.mean(anomalies_maps_hw_np,axis=0)
        cluster_anomalies_means_y.append(anomalies_mean) 

        heat_wave_anomal=HeatWave([first_day[h]],[duration[h]],anomalies_mean) #se considero le anomalie nella mappa
        heat_wave=HeatWave([first_day[h]],[duration[h]],mean_geop)  #se considero geopotenziale medio
        
        cluster_heat_waves=np.append(cluster_heat_waves,heat_wave)
        cluster_heat_waves_anomalies=np.append(cluster_heat_waves_anomalies,heat_wave_anomal)



matrix_distances=np.array([])
for i in range(0,len(cluster_heat_waves)):
    states=map(lambda x: x.geop_map, cluster_heat_waves)
    distance_each_hw=[ distance(cluster_heat_waves[i].geop_map,x) for x in states]
    matrix_distances=np.append(matrix_distances,distance_each_hw)
    
matrix_distances=np.reshape(matrix_distances,(len(cluster_heat_waves),len(cluster_heat_waves)))
np.fill_diagonal(matrix_distances,0)# d<1 sempre
d_min=np.min(matrix_distances[np.nonzero(matrix_distances)])
positions=np.where(matrix_distances==d_min)

merged_hw=cluster_heat_waves[positions[0][0]].merge(cluster_heat_waves[positions[0][1]])

cluster_heat_waves=np.delete(cluster_heat_waves,(positions[0][0],positions[0][1]))
cluster_heat_waves=np.append(cluster_heat_waves,merged_hw)









