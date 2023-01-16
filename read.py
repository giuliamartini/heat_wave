
import netCDF4 as nc
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from scipy import stats
import csv
from read import warm_days_woy, warm_days_wod, get_heat_waves, values_hw, get_properties
#from hw import HeatWave
from utilities import mean_temp_wod, mean_temp_day, remove_leap_years, window_years_int, window_days, window_years, percentile, percentile_d, mean_temp, get_day, get_month, get_year, print_arr, get_wod

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


# def warm_days_woy(temp_matrix, year):
#    warm_days = np.array([])
#    years = window_years_int(year)
#    percentiles = percentile(temp_matrix, year, 95)
#    year_ = 0
#    end = len(percentiles)
#    window = len(years)
#    # per ogni anno
#    for year_ in range(0, window):
#
#        wod = 0
#        # per ogni finestra di giorni
#        for wod in range(0, end):
#            day_ = wod*20
#            if (wod == end-1):
#
#                for day_ in range(360, 364):
#                    if (temp_matrix[years[year_], day_] > percentiles[wod]):
#                        warm_days = np.append(warm_days, years[year_])
#                        warm_days = np.append(warm_days, day_)
#
#            else:
#                for day_ in range(wod*20, wod*20+20):
#                    # _year=years[year_]
#
#                    if (temp_matrix[years[year_], day_] > percentiles[wod]):
#                        warm_days = np.append(warm_days, years[year_])
#                        warm_days = np.append(warm_days, day_)
#
#    warm_days = np.reshape(warm_days, (int(len(warm_days)/2), 2))
#    return warm_days

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


# prova_woy = warm_days_woy(temp_matrix, date_matrix, 48)
#
# print(prova_woy)


def warm_days_wod_y(temp_matrix, year, day_begin, day_end):
   
    if day_begin < 0 or day_begin > 365:
        raise Exception("day_begin is out of range")
    if day_end < 0 or day_end > 365:
        raise Exception("day_end is out of range")

    warm_days = np.array([])
    percentiles = percentile_d(temp_matrix, year, 90)
    # per ogni finestra di giorni
    for day_ in range(day_begin, day_end):
        # _year=years[year_]
        if (temp_matrix[year, day_] > percentiles[day_]):
            warm_days = np.append(warm_days, year)
            warm_days = np.append(warm_days, day_)

    warm_days = np.reshape(warm_days, (int(len(warm_days)/2), 2))
    return warm_days


def warm_days_wod(temp_matrix, year, wod):
    """ le finestre di giorni vanno da 1 a 19 e sono finestre di 20 giorni ciascuna tranne l'ultima che va dal giorno 360-365 """
    warm_days = np.array([])
    years = window_years(year)
    window = len(years)
    percentiles = percentile_d(temp_matrix, year, 90)
    end = len(percentiles)
    # per ogni anno
    for year_ in range(0, window):
        # per ogni finestra di giorni
        day_ = wod*20
        for day_ in range(wod*20, wod*20+20):
            # _year=years[year_]
            if (temp_matrix[years[year_], day_] > percentiles[day_]):
                warm_days = np.append(warm_days, years[year_])
                warm_days = np.append(warm_days, day_)

    warm_days = np.reshape(warm_days, (int(len(warm_days)/2), 2))
    return warm_days


def get_values_matrix(matrix, indexes):
    values = np.array([])
    i = 0
    for i in range(0, len(indexes)):
        # j=0
        # for j in range(0,len(indexes[i])-1):
        values = np.append(values, matrix[int(
            indexes[i][0])][int(indexes[i][1])])

    return values


# [i][0]: anno
# [i][1]:mese
# [i][20]:giorno
def get_values_date_matrix_int(date_matrix, indexes):
    values = np.array([])
    i = 0
    for i in range(0, len(indexes)):

        values = np.append(values, get_year(date_matrix[int(
            indexes[i][0])][int(indexes[i][1])]))

        values = np.append(values, get_month(date_matrix[int(
            indexes[i][0])][int(indexes[i][1])]))

        values = np.append(values, get_day(date_matrix[int(
            indexes[i][0])][int(indexes[i][1])]))

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
    i = 0
    for i in range(0, len(events)-1):
        next_date = date_matrix[int(events[i+1][0])][int(events[i+1][1])]
        current_date = date_matrix[int(events[i][0])][int(events[i][1])]
        previous_date = date_matrix[int(
            events[i-1][0])][int(events[i-1][1])]
        if(i == 0 and (next_date-current_date).astype(int) == 1):
            adjacent_days.append(int(events[i][0]))
            adjacent_days.append(int(events[i][1]))
            adjacent_days.append(int(events[i+1][0]))
            adjacent_days.append(int(events[i+1][1]))
        if (i != 0 and get_year(next_date) == get_year((current_date)) and (next_date-current_date).astype(int) == 1):
            if(get_year(current_date) == get_year((previous_date)) and (current_date-previous_date).astype(int) == 1):
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


# manca funzione per la magnitude in cluster_hw ho solo i valori-> ho perso le posizioni in matrice
# trovare un modo di passare a get properties le posizioni ( posso sovrascrivere get_values all'interno della classe
# ho riarrangiare la classe in altro modo)

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


def anomalies(heat_waves, temp_matrix):
    cluster_hw = values_hw(temp_matrix, heat_waves)
    anomal = []
    i = 0
    for i in range(0, len(cluster_hw)):

        cluster_anomalies = []
        mean_temp = mean_temp_wod(temp_matrix, int(heat_waves[i][int(len(
            heat_waves[i])/2)][0]), get_wod(int(heat_waves[i][int(len(heat_waves[i])/2)][1])))
        j = 0
        for j in range(0, len(cluster_hw[i])):
            # la temperatura su cui baso il calcolo è quella del giorno di mezzo della hw
            # l'[1] alla fine è il girono nel cluser di posizioni della matrice di temperature
            cluster_anomalies = np.append(
                cluster_anomalies, cluster_hw[i][j]-mean_temp)
        anomal.append(cluster_anomalies)
    return anomal


def means(heat_waves, temp_matrix):
    cluster_hw = values_hw(temp_matrix, heat_waves)
    means = []
    for i in range(0, len(cluster_hw)):

        mean_temp = mean_temp_wod(temp_matrix, int(heat_waves[i][int(len(
            heat_waves[i])/2)][0]), get_wod(int(heat_waves[i][int(len(heat_waves[i])/2)][1])))
        means.append(mean_temp)
    return means


dates = remove_leap_years(dates)
temp = remove_leap_years(temp)
time = remove_leap_years(time)
date_matrix = np.reshape(dates, (int(len(dates)/365), 365))
time_matrix = np.reshape(time, (int(len(time)/365), 365))
temp_matrix = np.reshape(temp, (int(len(temp)/365), 365))

cluster_intensities=np.array([])
cluster_duration=np.array([])
for k in range(0,71):
    woy = warm_days_wod_y(temp_matrix, k,274,365)
    #print(woy)
    hw = get_heat_waves_date(woy, date_matrix)
    prop = get_properties(date_matrix, temp_matrix, hw)
    durations=map(lambda dur: dur.duration, prop)
    intensities=map(lambda inte: inte.intensity, prop)
    for inte in intensities:
        cluster_intensities=np.append(cluster_intensities,inte) 
    for dur in durations:
        cluster_duration=np.append(cluster_duration,dur ) 
bins=np.arange(0,int(max(cluster_intensities))+1,1)
histo=plt.hist(cluster_intensities,bins=bins,range=(0,int(max(cluster_intensities))+1))
plt.xticks(np.arange(len(bins)),bins)
plt.legend("durata")
plt.title('occorrenze di intensità delle hw periodo OND da 1950-2021')
plt.xlabel('intensità [K*day] ')
plt.ylabel('occorrenze')
plt.show()
 #Plot KDE




#plt.figure(figsize=(8,6))
#density = stats.gaussian_kde(cluster_intensities)
#xs = np.linspace(0,max(cluster_intensities)+1,200)
#density.covariance_factor = lambda : .25
#density._compute_covariance()
#pdf=plt.plot(xs,density(xs), color='b')
#plt.title('distribuzione di probabilità di intensità delle hw periodo JFM da 1950-2021')
#plt.xlabel('intensità [K*day] ')
#plt.ylabel('distribuzione di probabilità')
#plt.show()



def properties_csv(prop):    
    with open("properties_"+str(1950+k)+".csv", "w") as stream:
        writer = csv.writer(stream)
        writer.writerows(prop)
    stream.close()




#perc = percentile_d(temp_matrix, k, 90)

    #line1 = plt.scatter(date_matrix[k], temp_matrix[k],
    #                    s=5, c='b', marker='o'),  # serie temporale
    #for j in range(0, len(woy)):
    #    line4 = plt.scatter(date_matrix[k][int(
    #        woy[j][1])], temp_matrix[k][int(woy[j][1])], s=5, c='r', marker='x')
    #    #mean_temp = mean_temp_day(temp_matrix, int(woy[j][0]), int(woy[j][1]))
    #    #plt.scatter(date_matrix[50][int(woy[j][1])],mean_temp,s=5, c='g', marker='x' )
#
    #mean_temp = []
    #for j in range(0, len(date_matrix[k])):
    #    mean_temp.append(mean_temp_day(temp_matrix, k, j))
#
    #line2 = plt.plot(date_matrix[55], mean_temp, color='green')
    #line3 = plt.plot(date_matrix[55], perc, color="orange")
#
    #plt.title(str(k+1950)+': arancione: 90-th percentile, verde: media delle temperature')
    #plt.xlabel('data ')
    #plt.legend([line1, line4], ['temperatura media giornaliera', 'anomalie'])
    #plt.show()
  
# for i in range(28,34):
#    wod_y=warm_days_wod_y(temp_matrix,i,0,90)
#
#    hw=get_heat_waves(wod_y)

# values=values_hw(temp_matrix,hw)
#    prop=get_properties(temp_matrix,hw)
#    print(wod_y)
#    print(prop)
#    #df=pd.DataFrame(prop)
# print(df)
# print(values)
# print(hw)
# for i in range(0,len(hw)):
#    values =get_values_matrix(temp_matrix, hw[i])
#    date=get_values_date_matrix_int(date_matrix,hw[i])
#    prop=get_properties(temp_matrix,hw)[i]
#np.savetxt('data.csv', values, delimiter=',')
#np.savetxt('data.csv', date, delimiter=',')
#np.savetxt('data.csv', prop, delimiter=',')
# for i in range(0, len())
#dates =  get_values_date_matrix(date_matrix,hw[i])
#plt.scatter(date_matrix[40],temp_matrix[40],s=5, c='b', marker='o')
# for i in range(0,len(hw)):
#    for j in range(0,len(hw[i])):
#        plt.scatter(date_matrix[40][int(hw[i][j][1])],temp_matrix[40][int(hw[i][j][1])],s=5, c='r', marker='x')
#
#
# plt.show()
#fig, axs = plt.subplots(36, 2)
# for k in range(0,35):
#    woy=warm_days_woy(temp_matrix,k)
#    hw=get_heat_waves(woy)
#    axs[k,0].scatter(date_matrix[k],temp_matrix[k],s=5, c='b', marker='o')
#    for i in range(0,len(hw)):
#        for j in range(0,len(hw[i])):
#            axs[k,0].scatter(date_matrix[k][int(hw[i][j][1])],temp_matrix[k][int(hw[i][j][1])],s=5, c='r', marker='x')
# for k in range(36,71):
#    woy=warm_days_woy(temp_matrix,k)
#    hw=get_heat_waves(woy)
#    axs[k-36,1].scatter(date_matrix[k],temp_matrix[k],s=5, c='b', marker='o')
#    for i in range(0,len(hw)):
#        for j in range(0,len(hw[i])):
#            axs[k-36,1].scatter(date_matrix[k][int(hw[i][j][1])],temp_matrix[k][int(hw[i][j][1])],s=5, c='r', marker='x')
# for i in range(28,34):
#    woy= warm_days_woy(temp_matrix,i)
#    hw=get_heat_waves_date(woy,date_matrix)
#    print(hw)
#    print(woy)


# DA VEDERE I RANGE DEI LOOP, TROVARE MODO PER ELIMINARE I LOOP
