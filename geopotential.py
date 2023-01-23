
import numpy as np
import pandas as pd
from datetime import datetime
import math

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
    days = wdy_int(woy_int(year), day_%90)
    cluster_map = []
    for day in days:
        cluster_map.append(np.array(ds.variables['z'][day, :, :]))
    cluster_map_np = np.array(cluster_map)
    mean = np.mean(cluster_map_np, axis=0)
    return mean

def day_percentile(day_, year, ds, p_value):
    days = wdy_int(woy_int(year), day_%90)
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

def maxim_distance(cluster1,cluster2):
    arr_dist=np.array([])
    for x in cluster1:
        for y in cluster2:
            arr_dist=np.append(arr_dist,distance(x.geop_map,y.geop_map) ) 
    maximum=np.max(arr_dist)
    return maximum

def min_distance(cluster1,cluster2):
    arr_dist=np.array([])
    for x in cluster1:
        for y in cluster2:
            arr_dist=np.append(arr_dist,distance(x.geop_map,y.geop_map) ) 
    minimum=np.min(arr_dist)
    return minimum

 

# sulle righe=long













