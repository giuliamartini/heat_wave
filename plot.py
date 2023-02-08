import netCDF4 as nc
import numpy as np
import pandas as pd
import cftime
from geopotential import strtodate, get_hw_days,  get_anomalies_map, get_anomalies_temp_map
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import cartopy.crs as ccrs

def corr_plot_lines_temp(lon, lat, temp, geop, title, levels_t=None, levels_g=None):
    """Plot correlations
    """
    fig = plt.figure(figsize=[12, 5])
    ax = fig.add_subplot(
        1, 1, 1, projection=ccrs.NorthPolarStereo(central_longitude=0))
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)
    #cf = ax.contourf(lon,lat,var,levels=levels,cmap='bwr',transform=ccrs.PlateCarree(),extend='both')
    cf = ax.contourf(lon, lat, temp, levels=levels_t, cmap='coolwarm',
                     transform=ccrs.PlateCarree(), extend='both')
    cs = ax.contour(lon, lat, geop, levels=levels_g,
                    colors='black', transform=ccrs.PlateCarree())
    plt.clabel(cs, fmt='%d')
    cbar = plt.colorbar(cf, ax=ax)
    cbar.set_label('T [K]')
    ax.coastlines()

    ax.set_extent([-180, 180, 30, 90],
                  crs=ccrs.PlateCarree(central_longitude=0))
    #cbar = plt.colorbar(cf,ax=ax)
    # cbar.set_label('ACC')
    #ax.set_title(title, fontsize=20)
    #plt.show()
    plt.savefig(title+'.png')
    plt.close()


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
dates = np.array(list(map(lambda x: x.date(), dates)))


cluster_heat_waves = []
cluster_heat_waves_anomalies = []

for i in range(0, 3):

    df = pd.read_csv('/home/giulia/tesipy2/JFM_90pct_fd'+str(i)+'.csv')
    df2 = pd.read_csv(
        '/home/giulia/tesipy2/JFM_90pct_dur'+str(i)+'.csv')
    first_day = np.array(df['firstday'])
    first_day = np.array(list(map(strtodate, first_day)))
    first_day = np.array(list(map(lambda x: x.date(), first_day)))
    duration = df2['duration']
    heat_waves_days = get_hw_days(dates, first_day, duration)

    cluster_mean = []
    cluster_temp_mean = []
    for h in range(0, len(heat_waves_days)):
        anomalies_maps_hw = []
        anomalies_temp_maps_hw = []
        for d in heat_waves_days[h]:

            anomalies_maps_hw.append(
                get_anomalies_map(dates, ds, d, int(d/90)))
            anomalies_temp_maps_hw.append(
                get_anomalies_temp_map(dates, ds_temp, d, int(d/90)))

        anomalies_maps_hw_np = np.array(anomalies_maps_hw)
        anomalies_mean = np.mean(anomalies_maps_hw_np, axis=0)
        cluster_mean.append(anomalies_mean)

        anomalies_temp_maps_hw_np = np.array(anomalies_temp_maps_hw)
        anomalies_temp_mean = np.mean(anomalies_temp_maps_hw_np, axis=0)
        cluster_temp_mean.append(anomalies_temp_mean)
       #se si vuole stampare ogni mappa    
       # level = np.array([-12,-9, -6,-3, 0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12])
       # corr_plot_lines_temp(lon,lat,anomalies_temp_mean,anomalies_mean,title='ftgh7590_cl'+str(i)+'_hw_p'+ str(h),levels_t=None,levels_g=None)
        # np.array([-240, -200, -160, -120,  -80,  -40, 40,   80,  120,  160,  200,  240,  280,
        #                                     320]))
    cluster_mean_np = np.array(cluster_mean)
    cluster_temp_mean_np = np.array(cluster_temp_mean)
    

    mean = np.mean(cluster_mean_np, axis=0)
    mean_temp = np.mean(cluster_temp_mean_np, axis=0)
    corr_plot_lines_temp(lon, lat, mean_temp, mean,
                         title='JFM_90pct_imcl'+str(i), levels_t=np.array([-12,-9,-6,-3, 0 ,3,6,9,12]), levels_g=np.array([-160, -120,  -80,  -40, 40,  80,  120, 160]))
 

        
