import netCDF4 as nc
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from read import warm_days_woy, warm_days_wod, get_heat_waves, values_hw, get_properties
#from hw import HeatWave
from utilities import mean_temp_wod, remove_leap_years, window_years_int, window_days, window_years, percentile, mean_temp, get_day, get_month, get_year, print_arr, get_wod

proj = ccrs.PlateCarree(central_longitude=180)
proj0 = ccrs.PlateCarree(0)
fn = '/home/giulia/Documents/Documenti/Tesi/pc_TAS_daymean_no29feb.nc'
ds = nc.Dataset(fn)
time = np.array(ds.variables['time'][:] - 438009.0)
temp = np.array(ds.variables['t2m'][:])

# tolgo ultimi 34 giorni
index1 = np.arange(len(time)-34, len(time), 1)

time = np.delete(time,  index1)
temp = np.delete(temp, index1)
dates = np.arange(dt.date(1950, 1, 1), dt.date(
    2022, 1, 1), dtype='datetime64[D]')


# rimuovo 29 febbraio da anni bisestili per semplificare matrice (72x365)
dates = remove_leap_years(dates)
temp = remove_leap_years(temp)
time = remove_leap_years(time)
date_matrix = np.reshape(dates, (int(len(dates)/365), 365))
time_matrix = np.reshape(time, (int(len(time)/365), 365))
temp_matrix = np.reshape(temp, (int(len(temp)/365), 365))

print(len(temp_matrix))
y=window_years(temp_matrix, 72)
#print(y)
print(y)
print(len(y))
#woy = warm_days_woy(temp_matrix, 60)
#print(woy)
#prov=get_heat_waves(woy)
#print(prov)

#prop=get_properties(temp_matrix,prov)
#print(prop)