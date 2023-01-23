import netCDF4 as nc
import numpy as np
import pandas as pd
import cftime
import csv
from datetime import datetime
import datetime as dt
from geop import strtodate,get_hw_days, maxim_distance, get_anomalies_map,min_distance,HeatWave


def algorithm(cluster_heat_waves):

    matrix_distances=np.array([])
    for i in range(0,len(cluster_heat_waves)):
        for hw in cluster_heat_waves:
            distance_each_hw=[ maxim_distance(cluster_heat_waves[i],hw)]
            matrix_distances=np.append(matrix_distances,distance_each_hw)

    matrix_distances=np.reshape(matrix_distances,(len(cluster_heat_waves),len(cluster_heat_waves)))
    np.fill_diagonal(matrix_distances,0)
    d_min=np.min(matrix_distances[np.nonzero(matrix_distances)])
    positions=np.where(matrix_distances==d_min)

    cluster_heat_waves[positions[0][0]].extend(cluster_heat_waves[positions[0][1]])

    cluster_heat_waves.remove(cluster_heat_waves[positions[0][1]])
    
    return cluster_heat_waves


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

for i in range(0, 60):
    df = pd.read_csv('/home/giulia/tesipy/properties_'+str(i+1959)+'.csv')
    first_day = np.array(df['firstday'])
    first_day = np.array(list(map(strtodate, first_day)))
    first_day = np.array(list(map(lambda x: x.date(), first_day)))
    duration = df['duration']
    heat_waves_days = get_hw_days(dates, first_day, duration)
    cluster_rs_hw = []


    cluster_anomalies_means_y = []
    for h in range(0,len(heat_waves_days)):
        anomalies_maps_hw = []
        for d in heat_waves_days[h]:              
            anomalies_maps_hw.append(get_anomalies_map(dates,ds, d, i))  
        anomalies_maps_hw_np = np.array(anomalies_maps_hw)
        anomalies_mean = np.mean(anomalies_maps_hw_np,axis=0)
        cluster_anomalies_means_y.append(anomalies_mean) 
        heat_wave_anomal=[HeatWave([first_day[h]],[duration[h]],anomalies_mean)] #se considero le anomalie nella mappa
        cluster_heat_waves_anomalies.append(heat_wave_anomal)


while len(cluster_heat_waves_anomalies)>6:
    cluster_heat_waves_anomalies=algorithm(cluster_heat_waves_anomalies)



        


##numero opportuno di cluster
cluster_check=cluster_heat_waves_anomalies.copy()
d=np.array([])

while len(cluster_check)>=2:
    dist=np.array([])
    for i in range(0,len(cluster_check)):
        
        for j in range(0,len(cluster_check)):
            if(j==i):
                dist=np.append(dist,10) #modo rapido e brutto per non considerare interazioni con se stesso ma da eliminare
            else:
                distance_each_hw=[ maxim_distance(cluster_check[i],cluster_check[j])]
                dist=np.append(dist,distance_each_hw)
    min=np.min(dist[np.nonzero(dist)]) 
    d=np.append(d,min)
    cluster_check=algorithm(cluster_check)


delta_d=np.array([])
for i in range(0,len(d)-1):
    delta_d=np.append(delta_d,d[i+1]-d[i])
print(delta_d)
max_delta_d=np.max(delta_d)
n=int(np.where(delta_d==max_delta_d)[0])

i=5-n #5 e non 6 perchè i np.array partono da 0
for i in range(5-n,6):
    cluster_heat_waves_anomalies=algorithm(cluster_heat_waves_anomalies)


for j in range(0,len(cluster_heat_waves)):
    with open("cluster_geop_fd"+str(j)+".csv", "w") as stream:
        writer = csv.writer(stream)
        writer.writerow(['firstday'])
        for hw in cluster_heat_waves[j]:    
            
            writer.writerow(hw.first_day)
        stream.close()
    with open("cluster_geop_dur"+str(j)+".csv", "w") as stream:
        writer = csv.writer(stream)
        writer.writerow(['duration'])
        for hw in cluster_heat_waves[j]:    
            
            writer.writerow(hw.duration)
        stream.close()


