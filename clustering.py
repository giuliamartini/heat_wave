import netCDF4 as nc
import numpy as np
import pandas as pd
import cftime
from geopotential import strtodate,get_hw_days, distance, get_anomalies_map,HeatWave

fn = '/home/giulia/geopotential_mean_no29feb.nc'
ds = nc.Dataset(fn, 'r')
lat = ds.variables['latitude']
lat = np.array(lat[:])
lon = np.array(ds.variables['longitude'][:])
time = ds.variables['time']
dates = cftime.num2pydate(time[:], time.units, calendar='standard')
dates = pd.to_datetime(dates)
dates = np.array(list(map(lambda x: x.date(), dates)))



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
np.fill_diagonal(matrix_distances,0)
d_min=np.min(matrix_distances[np.nonzero(matrix_distances)])
positions=np.where(matrix_distances==d_min)

merged_hw=cluster_heat_waves[positions[0][0]].merge(cluster_heat_waves[positions[0][1]])

cluster_heat_waves=np.delete(cluster_heat_waves,(positions[0][0],positions[0][1]))
cluster_heat_waves=np.append(cluster_heat_waves,merged_hw)

print(len(cluster_heat_waves))
print(matrix_distances)
print(merged_hw.geop_map)


