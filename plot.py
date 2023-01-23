import netCDF4 as nc
import numpy as np
import pandas as pd
import cftime
from geop import strtodate ,get_hw_days,  get_anomalies_map, day_mean



import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
#from numba import jit

def corr_plot(lon, lat, var, title, levels=None):
    """Plot correlations
    """
    fig = plt.figure(figsize=[12,5])
    ax = fig.add_subplot(111, projection=ccrs.NorthPolarStereo())
 
    cf = ax.contourf(lon,lat,var,levels=levels,cmap='bwr',transform=ccrs.NorthPolarStereo(),extend='both')
 
    ax.coastlines()
    ax.set_extent([-180, 180, 90, 60], crs=ccrs.NorthPolarStereo())
    cbar = plt.colorbar(cf,ax=ax)
    cbar.set_label('ACC')
    ax.set_title(title, fontsize=20)
    plt.show()

fn = '/home/giulia/geopotential_no29feb_f.nc'
ds = nc.Dataset(fn)
lat = ds.variables['latitude']
lat = np.array(lat[:])
lon = np.array(ds.variables['longitude'][:])
time = ds.variables['time']
dates = cftime.num2pydate(time[:], time.units, calendar='standard')
dates = pd.to_datetime(dates)
dates = np.array(list(map(lambda x: x.date(), dates)))
index=np.arange(0,14,1)
dates=np.delete(dates,index)

cluster_heat_waves=[]
cluster_heat_waves_anomalies=[]
 
#plot=corr_plot(lon,lat,np.array(ds.variables['z'][5,:,:]),title='mappa di anomalia di altezza geopotenziale 500hPa cluster:')
 
for i in range(0,2):
  
   df = pd.read_csv('/home/giulia/tesipy/cluster_geop_fd'+str(i)+'.csv')
   df2= pd.read_csv('/home/giulia/tesipy/cluster_geop_dur'+str(i)+'.csv')
   first_day = np.array(df['firstday'])
   first_day = np.array(list(map(strtodate, first_day)))
   first_day = np.array(list(map(lambda x: x.date(), first_day)))
   duration = df2['duration']
   heat_waves_days = get_hw_days(dates, first_day, duration)


   for h in range(0,len(heat_waves_days)):
      anomalies_maps_hw=[]
      for d in heat_waves_days[h]:          
         anomalies_maps_hw.append(get_anomalies_map(dates,ds,d,int(d/90)))  
   anomalies_maps_hw_np = np.array(anomalies_maps_hw)
   anomalies_mean = np.mean(anomalies_maps_hw_np,axis=0)
   plot=corr_plot(lon,lat,anomalies_mean,title='mappa di anomalia di altezza geopotenziale 500hPa cluster: '+str(i))
   


        
