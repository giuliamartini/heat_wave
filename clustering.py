import netCDF4 as nc
import numpy as np
import pandas as pd
import cftime
import csv
from geopotential import strtodate,get_hw_days, maxim_distance, get_anomalies_map,min_distance,HeatWave

#Inserire il path per il file netCDF4 con mappe di geopotenziale a 500 hPa
path_geop= '/home/giulia/geopotential_m.nc'

def algorithm(cluster_heat_waves):

    matrix_distances=np.array([])
    for i in range(0,len(cluster_heat_waves)):
        for j in range(0,len(cluster_heat_waves)):
            distance_each_hw= maxim_distance(cluster_heat_waves[i],cluster_heat_waves[j])
            matrix_distances=np.append(matrix_distances,distance_each_hw)

    matrix_distances=np.reshape(matrix_distances,(len(cluster_heat_waves),len(cluster_heat_waves)))
    #print(matrix_distances)
    np.fill_diagonal(matrix_distances,0)
    d_min=np.min(matrix_distances[np.nonzero(matrix_distances)])
    positions=np.where(matrix_distances==d_min)

    cluster_heat_waves[positions[0][0]].extend(cluster_heat_waves[positions[0][1]])

    cluster_heat_waves.remove(cluster_heat_waves[positions[0][1]])
    
    return cluster_heat_waves


fn = path_geop
ds = nc.Dataset(fn)
time = ds.variables['time']
dates = cftime.num2pydate(time[:], time.units, calendar='standard')
dates = pd.to_datetime(dates)
dates = np.array(list(map(lambda x: x.date(), dates)))
months = np.array(list(map(lambda x: x.month, dates)))
days = np.array(list(map(lambda x: x.day, dates)))
leap=[]
for i in range(0,len(months)):
    if months[i]==2 and days[i]==29:
        leap.append(int(i))

dates=np.delete(dates,leap)    

cluster_heat_waves=[]
cluster_heat_waves_anomalies=[]
heat_waves_days=[]
first_days=[]
durations=[]
magnitudos=[]
#ho cambiato il range
for i in range(0, 61):
    df = pd.read_csv('/home/giulia/tesipy2/JFM_90pct_'+str(i+1959)+'.csv')
    first_day = np.array(df['firstday'])
    first_day = np.array(list(map(strtodate, first_day)))
    first_day = np.array(list(map(lambda x: x.date(), first_day)))
    first_days.append(first_day)
    duration = np.array(df['duration'])
    durations.append(duration)
    magnitudo=np.array(df['magnitudo'])
    magnitudos.append(magnitudo)

    heat_waves_days.append(get_hw_days(dates, first_day, duration))

   # print(heat_waves_days)
cluster_rs_hw = []
cluster_anomalies_means_y = []
for h in range(0,len(heat_waves_days)):
    
    if len(heat_waves_days[h])!= 0:
        for hw in range(0,len(heat_waves_days[h])):
            anomalies_maps_hw = []
            for d in heat_waves_days[h][hw]:              
                anomalies_maps_hw.append(get_anomalies_map(dates,ds, d, int(d/90)) ) #divido per g dato da ECMWF
            anomalies_maps_hw_np = np.array(anomalies_maps_hw)
            anomalies_mean = np.mean(anomalies_maps_hw_np,axis=0)
            cluster_anomalies_means_y.append(anomalies_mean) 
            heat_wave_anomal=[HeatWave([first_days[h][hw]],[durations[h][hw]],[magnitudos[h][hw]],anomalies_mean)] #se considero le anomalie nella mappa
            cluster_heat_waves_anomalies.append(heat_wave_anomal)
print(cluster_heat_waves_anomalies)
print(len(cluster_heat_waves_anomalies))
#cambiato
while len(cluster_heat_waves_anomalies)>3:
    cluster_heat_waves_anomalies=algorithm(cluster_heat_waves_anomalies)
#print(len(cluster_heat_waves_anomalies[0]),len(cluster_heat_waves_anomalies[1]),len(cluster_heat_waves_anomalies[2]))
##print(cluster_heat_waves_anomalies)
#print(len(cluster_heat_waves_anomalies))
#
##numero opportuno di clusters
#d=np.array([])
#num_cl=np.array([])
#while len(cluster_heat_waves_anomalies)>=2:
#    dist=np.array([])
#    for i in range(0,len(cluster_heat_waves_anomalies)):
#        
#        for j in range(0,len(cluster_heat_waves_anomalies)):
#            if(j==i):
#                dist=np.append(dist,0) #modo rapido e brutto per non considerare interazioni con se stesso ma da eliminare
#            else:
#                distance_each_hw=[ maxim_distance(cluster_heat_waves_anomalies[i],cluster_heat_waves_anomalies[j])]
#                dist=np.append(dist,distance_each_hw)
#    min=np.min(dist[np.nonzero(dist)]) 
#    d=np.append(d,min)
#    num_cl=np.append(num_cl,len(cluster_heat_waves_anomalies))
#
#    cluster_heat_waves_anomalies=algorithm(cluster_heat_waves_anomalies)
#
#print('d: ',d)
#print('num_cl: ',num_cl)
#
#delta_d=np.array([])
#for i in range(0,len(d)-1):
#    delta_d=np.append(delta_d,d[i+1]-d[i])
#    print(str(i+1)+'-'+str(i))
#print('delta_d= ', delta_d)
#max_delta_d=np.max(delta_d)
#n=int(np.where(delta_d==max_delta_d)[0])
#5 e non 6 perchè i np.array partono da 0


for j in range(0,len(cluster_heat_waves_anomalies)):
    with open("JFM_90pct_fd"+str(j)+".csv", "w") as stream:
        writer = csv.writer(stream)
        writer.writerow(['firstday'])
        for hw in cluster_heat_waves_anomalies[j]:      
            writer.writerow(hw.first_day)
        stream.close()
    with open("JFM_90pct_dur"+str(j)+".csv", "w") as stream:
        writer = csv.writer(stream)
        writer.writerow(['duration'])
        for hw in cluster_heat_waves_anomalies[j]:        
            writer.writerow(hw.duration)
        stream.close()
    with open("JFM_90pct_mag"+str(j)+".csv", "w") as stream:
        writer = csv.writer(stream)
        writer.writerow(['magnitudo'])
        for hw in cluster_heat_waves_anomalies[j]:        
            writer.writerow(hw.magnitudo)
    stream.close()


