import netCDF4 as nc
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from scipy import stats
import cftime
import csv

from utilities  import  mean_temp_day,window_years,percentile_d,get_wod

#from utils import mean_temp_wod, mean_temp_day, remove_leap_years, window_years, percentile_d, get_wod

#fn = '/home/giulia/Documents/Documenti/Tesi/pc_TAS_daymean.nc'
fn='/home/giulia/Documents/Documenti/Tesi/pc_TAS_daymean_no29feb.nc'
ds = nc.Dataset(fn)
time = ds.variables['time']
temp = np.array(ds.variables['t2m'][:])



dates = cftime.num2pydate(time[:], time.units, calendar='standard')
dates = pd.to_datetime(dates)
dates = np.array(list(map(lambda x: x.date(), dates)))

index=np.arange(0,12,1)
dates=np.delete(dates,index)
temp=np.delete(temp,index)
index1=np.arange(len(dates)-22,len(dates),1)
dates=np.delete(dates,index1)
temp=np.delete(temp,index1)
months = np.array(list(map(lambda x: x.month, dates)))
days = np.array(list(map(lambda x: x.day, dates)))
leap=[]
for i in range(0,len(months)):
    if months[i]==2 and days[i]==29:
        leap.append(int(i))

dates=np.delete(dates,leap)    
temp=np.delete(temp,leap) 


def warm_days_woy(temp_matrix, year):
    warm_days = np.array([])
    percentiles = percentile_d(temp_matrix, year, 90)
    # per ogni finestra di giorni
    for day_ in range(0, len(percentiles)):

        if (temp_matrix[year, day_] > percentiles[day_]):
            warm_days = np.append(warm_days, year)
            warm_days = np.append(warm_days, day_)

    warm_days = np.reshape(warm_days, (int(len(warm_days)/2), 2))
    return warm_days


def warm_days_wod_y(temp_matrix, year, day_begin, day_end):
   
    if day_begin < 0 or day_begin > 365:
        raise Exception("day_begin is out of range")
    if day_end < 0 or day_end > 365:
        raise Exception("day_end is out of range")

    warm_days = np.array([])
    percentiles = percentile_d(temp_matrix, year, 95)
    # per ogni finestra di giorni
    for day_ in range(day_begin, day_end):
        # _year=years[year_]
        if (temp_matrix[year, day_] > percentiles[day_]):
            warm_days = np.append(warm_days, year)
            warm_days = np.append(warm_days, day_)

    warm_days = np.reshape(warm_days, (int(len(warm_days)/2), 2))
    return warm_days



def get_values_matrix(matrix, indexes):
    values = np.array([])
    i = 0
    for i in range(0, len(indexes)):
        values = np.append(values, matrix[int(
            indexes[i][0])][int(indexes[i][1])])

    return values


def get_values_date_matrix_int(date_matrix, indexes):
    values = np.array([])
    i = 0
    for i in range(0, len(indexes)):

        values = np.append(values, date_matrix[int(
            indexes[i][0])][int(indexes[i][1])].year)

        values = np.append(values, date_matrix[int(
            indexes[i][0])][int(indexes[i][1])].month)

        values = np.append(values, date_matrix[int(
            indexes[i][0])][int(indexes[i][1])].day)

    values = np.reshape(values, (int(len(values)/3), 3))
    return values


def get_values_date_matrix(date_matrix, indexes):
    #values = np.array([])
    values = np.array([])
    i = 0
    for i in range(0, len(indexes)):

        values = np.append(values, date_matrix[int(
            indexes[i][0])][int(indexes[i][1])])

    return values


def get_heat_waves_date(events, date_matrix):
    adjacent_days = []
    heat_waves = []
    for i in range(0, len(events)-1):
        next_date = date_matrix[int(events[i+1][0])][int(events[i+1][1])]
        current_date = date_matrix[int(events[i][0])][int(events[i][1])]
        previous_date = date_matrix[int(
            events[i-1][0])][int(events[i-1][1])]
        if(i == 0 and (next_date-current_date).days == 1):
            adjacent_days.append(int(events[i][0]))
            adjacent_days.append(int(events[i][1]))
            adjacent_days.append(int(events[i+1][0]))
            adjacent_days.append(int(events[i+1][1]))
        if (i != 0 and next_date.year == current_date.year and (next_date-current_date).days == 1):
            if(current_date.year == previous_date.year and (current_date-previous_date).days == 1):
                if(i == len(events)-2):
                    # altrimenti usciva dal loop senza aggiungere un'eventuale ultima ondata di calore
                    adjacent_days.append(int(events[i+1][0]))
                    adjacent_days.append(int(events[i+1][1]))
                    heat_waves.append(np.reshape(
                        adjacent_days, (int(len(adjacent_days)/2), 2)))
                    adjacent_days = []
                else:
                    adjacent_days.append(int(events[i+1][0]))
                    adjacent_days.append(int(events[i+1][1]))
            else:
                # aggiungo che se la data precedente non dista di un giorno allora svuoto gli adjacent days (anche se dovrebbe essere già stato fatto?)
                if(len(adjacent_days) >= 6):
                    heat_waves.append(np.reshape(
                        adjacent_days, (int(len(adjacent_days)/2), 2)))
                    adjacent_days = []

                    adjacent_days.append(int(events[i][0]))
                    adjacent_days.append(int(events[i][1]))
                    adjacent_days.append(int(events[i+1][0]))
                    adjacent_days.append(int(events[i+1][1]))
                else:
                    adjacent_days = []

                    adjacent_days.append(int(events[i][0]))
                    adjacent_days.append(int(events[i][1]))
                    adjacent_days.append(int(events[i+1][0]))
                    adjacent_days.append(int(events[i+1][1]))
        else:
            if(len(adjacent_days) >= 6):
                heat_waves.append(np.reshape(
                    adjacent_days, (int(len(adjacent_days)/2), 2)))
                adjacent_days = []
    heat_waves_arr = np.array(heat_waves, dtype=object)
    return heat_waves_arr


def get_heat_waves(events):
    adjacent_days = []
    heat_waves = []
    for i in range(0, len(events)-1):
        next_date_y = int(events[i+1][0])
        next_date_d = int(events[i+1][1])
        current_date_y = int(events[i][0])
        current_date_d = int(events[i][1])
        previous_date_y = int(events[i-1][0])
        previous_date_d = int(events[i-1][1])
        if(i == 0 and next_date_y == current_date_y and next_date_d-current_date_d == 1):
            adjacent_days.append(int(events[i][0]))
            adjacent_days.append(int(events[i][1]))
            adjacent_days.append(int(events[i+1][0]))
            adjacent_days.append(int(events[i+1][1]))
        if (i != 0 and next_date_y == current_date_y and next_date_d-current_date_d):
            if(current_date_y == previous_date_y and current_date_d-previous_date_d == 1):
                if(i == len(events)-2):
                    # altrimenti usciva dal loop senza aggiungere un'eventuale ultima ondata di calore
                    adjacent_days.append(int(events[i+1][0]))
                    adjacent_days.append(int(events[i+1][1]))
                    heat_waves.append(np.reshape(
                        adjacent_days, (int(len(adjacent_days)/2), 2)))
                    adjacent_days = []
                else:
                    adjacent_days.append(events[i+1][0])
                    adjacent_days.append(events[i+1][1])
            else:
                # aggiungo che se la data precedente non dista di un giorno allora svuoto gli adjacent days (anche se dovrebbe essere già stato fatto?)
                if(len(adjacent_days) >= 6):
                    heat_waves.append(np.reshape(
                        adjacent_days, (int(len(adjacent_days)/2), 2)))
                    adjacent_days = []

                    adjacent_days.append(int(events[i][0]))
                    adjacent_days.append(int(events[i][1]))
                    adjacent_days.append(int(events[i+1][0]))
                    adjacent_days.append(int(events[i+1][1]))
                else:
                    adjacent_days = []

                    adjacent_days.append(int(events[i][0]))
                    adjacent_days.append(int(events[i][1]))
                    adjacent_days.append(int(events[i+1][0]))
                    adjacent_days.append(int(events[i+1][1]))
        else:
            if(len(adjacent_days) >= 6):
                heat_waves.append(np.reshape(
                    adjacent_days, (int(len(adjacent_days)/2), 2)))
                adjacent_days = []
    heat_waves_arr = np.array(heat_waves, dtype=object)
    return heat_waves_arr


def values_hw(temp_matrix, heat_waves):
    temp_hw = []
    cluster_hw = []
    for i in range(0, len(heat_waves)):
        hw = heat_waves[i]
        for j in range(0, len(hw)):
            temp_hw.append(temp_matrix[int(hw[j][0])][int(hw[j][1])])

        cluster_hw.append(temp_hw)
        temp_hw = []
    return cluster_hw



class Properties:
    def __init__(self, first_day, T_max, duration, magnitudo, intensity):
        self.first_day = first_day
        self.T_max = T_max
        self.duration = duration
        self.magnitudo = magnitudo
        self.intensity = intensity
    
    def __repr__(self):
        return f"Properties({self.first_day!r}, {self.T_max!r},{self.duration!r},{self.magnitudo!r},{self.intensity!r})"

    def __iter__(self):
       return iter([self.first_day, self.T_max,self.duration,self.magnitudo,self.intensity])


def get_properties(date_matrix, temp_matrix, heat_waves):
    """restituisce le proprietà delle ondate di calore in ordine: 
    temperatura massima
    durata
    magnitudo
    intensità"""
    #[T_max, length,magnitude,intensity]
    cluster_hw = values_hw(temp_matrix, heat_waves)
    cluster_properties = []
    #my_generic_iterable = map(str.upper, cluster_hw)
    i = 0
    for i in range(0, len(cluster_hw)):
       # for i in my_generic_iterable:
        first_date = date_matrix[int(
            heat_waves[i][0][0])][int(heat_waves[i][0][1])]
        T_max = max(cluster_hw[i])
        length = len(cluster_hw[i])

        cluster_anomalies = np.array([])

        for j in range(0, len(cluster_hw[i])):
            mean_temp = mean_temp_day(temp_matrix, int(
                heat_waves[i][j][0]), int(heat_waves[i][j][1]))
            cluster_anomalies = np.append(
                cluster_anomalies, cluster_hw[i][j]-mean_temp)
        magnitude = np.mean(cluster_anomalies)
        intensity = magnitude*length
        properties = Properties(
            first_date, T_max, length, magnitude, intensity)

        cluster_properties.append(properties)

    # ritorna il cluster di array contenenti le proprietà delle ondate di calore avveute nella finestra di tempo
    return cluster_properties



def properties_csv(prop):    
    
    with open("properties_90pct_"+str(1950+k)+".csv", "w") as stream:
        #writer = csv.DictWriter(stream, delimiter=',',fieldnames=headerList)     
        writer = csv.writer(stream)
        writer.writerow(['firstday','Tmax','duration','magnitudo','intensity'])
        writer.writerows(prop)
    stream.close()
        
   


#date_matrix = np.reshape(dates, (int(len(dates)/365), 365))
#temp_matrix = np.reshape(temp, (int(len(temp)/365), 365))

date_matrix = np.reshape(dates, (int(len(dates)/365), 365))
temp_matrix = np.reshape(temp, (int(len(temp)/365), 365))

cluster_intensities=np.array([])
cluster_duration=np.array([])
w=np.array([])
for k in range(0,71):
    woy = warm_days_wod_y(temp_matrix, k,180,270)
    w=np.append(w,len(woy))
    #print(woy)


    #hw = get_heat_waves_date(woy, date_matrix)
    #prop = get_properties(date_matrix, temp_matrix, hw)
    #properties_csv(prop)
#print(np.sum(w))
#warm_days=np.array([])
#number_event=np.array([])
#number_days=np.array([])
#min=np.array([])
#year=np.array([])

#woy = warm_days_wod_y(temp_matrix, 70,0,365)
#hw = get_heat_waves_date(woy, date_matrix)
#print(hw)
#means=np.array([])
#perc=percentile_d(temp_matrix,70,95)
#for i in range(0, len(temp_matrix[70])):
#    means=np.append(means,mean_temp_day(temp_matrix,70,i))
#
#print(len(perc))
#print(len(means))
#
#
#plt.scatter(date_matrix[70],temp_matrix[70],c='tab:blue',s=10,marker ='o')
#plt.plot(date_matrix[70],means,c='tab:orange')
#plt.plot(date_matrix[70],perc,c='tab:green')
#for h in hw:
#    for i in range(0,len(h)):
#        plt.scatter(date_matrix[70][int(h[i][1])],temp_matrix[70][int(h[i][1])],c='r',s=10,marker='o')
#plt.legend(['T ','media ','95° percentile','heatwaves'])
#plt.xlabel('Date ')
#plt.ylabel('Temperatura media giornaliera [K]')
#plt.show()
#
#for k in range(9,71):
#    woy = warm_days_wod_y(temp_matrix, k,0,365)
#    hw = get_heat_waves_date(woy, date_matrix)
#    #min=np.append(min,np.min(temp_matrix[k]))
#    year=np.append(year,k+1950)
#    #max=np.max(temp_matrix[k])
    
#a, b = np.polyfit(year, min, 1)
#plt.scatter(year,min,c='tab:orange',s=20)
#plt.plot(year, a*year+b)
#plt.legend('TF')
#plt.bar_label('slope='+str(a))
#plt.xlabel('Anno')
#plt.ylabel('Temperatura minima annua [K]')
#plt.show()

    #plt.scatter(k+1950,max,c='tab:orange',s=20)
    #number_event=np.append(number_event,len(hw))
    #for h in hw:
    #    number_days=np.append(number_days,len(h))
    
    #prop = get_properties(date_matrix, temp_matrix, hw)
    #properties_csv(prop)
#plt.show()
#ev=np.sum(number_event)
#day=np.sum(number_days)
#print(ev)
#print(day)
#print(len(warm_days))
#print(np.sum(warm_days))


