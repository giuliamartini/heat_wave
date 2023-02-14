import netCDF4 as nc
import numpy as np
import pandas as pd
import cftime
from geopotential import strtodate, get_hw_days,  get_anomalies_map, get_anomalies_temp_map, HeatWave, maxim_distance, min_corr, max_corr
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import cartopy.crs as ccrs
from plot import corr_plot_lines_temp

fn = '/home/giulia/geopotential_m.nc'
fn_temp = '/home/giulia/temp2m_m.nc'
ds = nc.Dataset(fn)
ds_temp = nc.Dataset(fn_temp)
lat = ds.variables['latitude']
lat = np.array(lat[:])
lon = np.array(ds.variables['longitude'][:])
time = ds.variables['time']
dates = cftime.num2pydate(time[:], time.units, calendar='standard')
dates = pd.to_datetime(dates)
datess=dates
dates = np.array(list(map(lambda x: x.date(), dates)))
#al posto di i mettere numero del cluster
for ii in range(0,3):
    cluster_heat_waves=[]
    cluster_heat_waves_anomalies=[]
    heat_waves_days=[]
    first_days=[]
    durations=[]
    magnitudos=[]
    df = pd.read_csv('/home/giulia/tesipy2/JFMn_90pct_fd'+str(ii)+'.csv')
    df2 = pd.read_csv(
        '/home/giulia/tesipy2/JFMn_90pct_dur'+str(ii)+'.csv')
    df3= pd.read_csv(
        '/home/giulia/tesipy2/JFMn_90pct_mag'+str(ii)+'.csv')
    first_day = np.array(df['firstday'])
    first_day = np.array(list(map(strtodate, first_day)))
    first_day = np.array(list(map(lambda x: x.date(), first_day)))
    first_days.append(first_day)
    duration = np.array(df2['duration'])
    durations.append(duration)
    magnitudo=np.array(df3['magnitudo'])
    magnitudos.append(magnitudo)

    heat_waves_days.append(get_hw_days(dates, first_day, duration))
    #print(first_days)
    cluster_rs_hw = []
    cluster_anomalies_means_y = []
    for h in range(0,len(heat_waves_days)):    
        for hw in range(0,len(heat_waves_days[h])):
            anomalies_maps_hw = []
            for d in heat_waves_days[h][hw]:              
                anomalies_maps_hw.append(get_anomalies_map(dates,ds, int(d), int(d/90)) ) #divido per g dato da ECMWF
            anomalies_maps_hw_np = np.array(anomalies_maps_hw)
            anomalies_mean = np.mean(anomalies_maps_hw_np,axis=0)
            cluster_anomalies_means_y.append(anomalies_mean) 
            heat_wave_anomal=[HeatWave([first_days[h][hw]],[durations[h][hw]],[magnitudos[h][hw]],anomalies_mean)] #se considero le anomalie nella mappa
            cluster_heat_waves_anomalies.extend(heat_wave_anomal)


#print(cluster_heat_waves_anomalies)
    fd=[]
    day=[]
    hw_non_corr=[]
    hw_max_corr=[]
    n=len(cluster_heat_waves_anomalies)
    rmax=0
    map_max_corr=[cluster_heat_waves_anomalies[0]]
    for i in range(0,n):
        hw_check=[cluster_heat_waves_anomalies[0]]
        cluster_heat_waves_anomalies.remove(cluster_heat_waves_anomalies[0])
        r =max_corr(hw_check,cluster_heat_waves_anomalies)
        #print(hw_check[0].first_day)
        #print(r)
        if r>rmax:
            rmax=r
            map_max_corr.remove(map_max_corr[0])
            map_max_corr.extend(hw_check)
        if r<0.4:
            fd.append(np.where(first_day==hw_check[0].first_day))
            day.append(np.where(dates==hw_check[0].first_day))
            hw_non_corr.extend(hw_check)
        cluster_heat_waves_anomalies.extend(hw_check)


    print(fd)
    print(day)

    hwd=get_hw_days(dates,np.array([map_max_corr[0].first_day]),np.array([map_max_corr[0].duration]))
    anomalies_r=[]
    anomalies_temp_r=[]
    for g in hwd[0]:
        anomalies_r.append(get_anomalies_map(dates, ds, int(g), int(g/90)))
        anomalies_temp_r.append(
                get_anomalies_temp_map(dates, ds_temp, int(g), int(g/90)))
        anomalies_r_np = np.array(anomalies_r)
        anomalies_r_mean = np.mean(anomalies_r_np, axis=0)
        anomalies_temp_r_np = np.array(anomalies_temp_r)
        anomalies_temp_r_mean = np.mean(anomalies_temp_r_np, axis=0)
        mask = (anomalies_temp_r_mean > -1.5) & (anomalies_temp_r_mean < 1.5)
        anomalies_temp_r_mean[mask] = np.nan
    
        corr_plot_lines_temp(lon, lat,anomalies_temp_r_mean, anomalies_r_mean,
                             title=' $r_{max}$ cluster '+str(ii)+' '+str(datess[int(hwd[0][0])].year)+'-'+str(datess[int(hwd[0][0])].month)+'-'+str(datess[int(hwd[0][0])].day), levels_t=np.array([-12,-9,-6,-3,0,3,6,9,12]), levels_g=np.array([-160, -120,  -80,  -40, 40,  80,  120, 160]))
   


    for h in hw_non_corr:
        print(h.first_day)
    cluster_mean = []
    cluster_temp_mean = []
    for h in range(0, len(hw_non_corr)):
        anomalies_maps_hw = []
        anomalies_temp_maps_hw = []
        heat_waves_days=get_hw_days(dates,np.array([hw_non_corr[h].first_day]),np.array([hw_non_corr[h].duration]))
        for d in heat_waves_days[0]:
            print(dates[int(d)])
            anomalies_maps_hw.append(
                get_anomalies_map(dates, ds, int(d), int(d/90)))
            anomalies_temp_maps_hw.append(
                get_anomalies_temp_map(dates, ds_temp, int(d), int(d/90)))
        anomalies_maps_hw_np = np.array(anomalies_maps_hw)
        anomalies_mean = np.mean(anomalies_maps_hw_np, axis=0)
        anomalies_temp_maps_hw_np = np.array(anomalies_temp_maps_hw)
        anomalies_temp_mean = np.mean(anomalies_temp_maps_hw_np, axis=0)
        mask = (anomalies_temp_mean > -1.5) & (anomalies_temp_mean < 1.5)
        anomalies_temp_mean[mask] = np.nan
    
        corr_plot_lines_temp(lon, lat,anomalies_temp_mean, anomalies_mean,
                             title=' $r_{cl}$<0.4 cluster '+str(ii)+' '+str(datess[int(heat_waves_days[0][0])].year)+'-'+str(datess[int(heat_waves_days[0][0])].month)+'-'+str(datess[int(heat_waves_days[0][0])].day), levels_t=np.array([-12,-9,-6,-3,0,3,6,9,12]), levels_g=np.array([-160, -120,  -80,  -40, 40,  80,  120, 160]))
  
