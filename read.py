
import numpy as np
import math 
from utilities import mean_temp_wod, remove_leap_years, window_years_int, window_days, window_years, percentile, mean_temp, get_day, get_month, get_year, print_arr, get_wod



#def warm_days_woy(temp_matrix, year):
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
    percentiles = percentile(temp_matrix, year, 95)
    end = len(percentiles)
   

    wod = 0
    # per ogni finestra di giorni
    for wod in range(0, end):
        day_ = wod*20
        if (wod == end-1):
            for day_ in range(360, 364):
                if (temp_matrix[year, day_] > percentiles[wod]):
                    warm_days = np.append(warm_days, year)
                    warm_days = np.append(warm_days, day_)
        else:
            for day_ in range(wod*20, wod*20+20):
                # _year=years[year_]
                if (temp_matrix[year, day_] > percentiles[wod]):
                    warm_days = np.append(warm_days, year)
                    warm_days = np.append(warm_days, day_)

    warm_days = np.reshape(warm_days, (int(len(warm_days)/2), 2))
    return warm_days



# prova_woy = warm_days_woy(temp_matrix, date_matrix, 48)
#
# print(prova_woy)


def warm_days_wod(temp_matrix, year, wod):
    """ le finestre di giorni vanno da 1 a 19 e sono finestre di 20 giorni ciascuna tranne l'ultima che va dal giorno 360-365 """
    warm_days = np.array([])
    years = window_years_int(year)
    percentiles = percentile(temp_matrix, year, 95)
    year_ = 0
    window = len(years)
    # per ogni anno
    for year_ in range(0, window):
        # per ogni finestra di giorni
        day_ = wod*20
        for day_ in range(wod*20, wod*20+20):
            # _year=years[year_]
            if (temp_matrix[years[year_], day_] > percentiles[wod]):
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
    values = np.array([])
    i = 0
    for i in range(0, len(indexes)):

        values = np.append(values, date_matrix[int(
            indexes[i][0])][int(indexes[i][1])])

        values = np.append(values, date_matrix[int(
            indexes[i][0])][int(indexes[i][1])])

        values = np.append(values, date_matrix[int(
            indexes[i][0])][int(indexes[i][1])])

    values = np.reshape(values, (int(len(values)/3), 3))
    return values


#def get_heat_waves(events, date_matrix):
#    adjacent_days = []
#    heat_waves = []
#    i = 0
#    for i in range(0, len(events)-1):
#        next_date = date_matrix[int(events[i+1][0])][int(events[i+1][1])]
#        current_date = date_matrix[int(events[i][0])][int(events[i][1])]
#        previous_date = date_matrix[int(
#            events[i-1][0])][int(events[i-1][1])]
#        if(i == 0 and (next_date-current_date).astype(int) == 1):
#            adjacent_days.append(events[i][0])
#            adjacent_days.append(events[i][1])
#            adjacent_days.append(events[i+1][0])
#            adjacent_days.append(events[i+1][1])
#        if (i != 0 and get_year(next_date) == get_year((current_date)) and (next_date-current_date).astype(int) == 1):
#            if(get_year(current_date) == get_year((previous_date)) and (current_date-previous_date).astype(int) == 1):
#                if(i == len(events)-2):
#                    # altrimenti usciva dal loop senza aggiungere un'eventuale ultima ondata di calore
#                    adjacent_days.append(events[i+1][0])
#                    adjacent_days.append(events[i+1][1])
#                    heat_waves.append(np.reshape(
#                        adjacent_days, (int(len(adjacent_days)/2), 2)))
#                    adjacent_days = []
#                else:
#                    adjacent_days.append(events[i+1][0])
#                    adjacent_days.append(events[i+1][1])
#            else:
#                # aggiungo che se la data precedente non dista di un giorno allora svuoto gli adjacent days (anche se dovrebbe essere già stato fatto?)
#                if(len(adjacent_days) >= 6):
#                    heat_waves.append(np.reshape(
#                        adjacent_days, (int(len(adjacent_days)/2), 2)))
#                    adjacent_days = []
#
#                    adjacent_days.append(events[i][0])
#                    adjacent_days.append(events[i][1])
#                    adjacent_days.append(events[i+1][0])
#                    adjacent_days.append(events[i+1][1])
#                else:
#                    adjacent_days = []
#
#                    adjacent_days.append(events[i][0])
#                    adjacent_days.append(events[i][1])
#                    adjacent_days.append(events[i+1][0])
#                    adjacent_days.append(events[i+1][1])
#        else:
#            if(len(adjacent_days) >= 6):
#                heat_waves.append(np.reshape(
#                    adjacent_days, (int(len(adjacent_days)/2), 2)))
#                adjacent_days = []
#    heat_waves_arr = np.array(heat_waves, dtype=object)
#    return heat_waves_arr


def get_heat_waves(events):
    adjacent_days = []
    heat_waves = []
    i = 0
    for i in range(0, len(events)-1):
        next_date_y = int(events[i+1][0])
        next_date_d=int(events[i+1][1])
        current_date_y = int(events[i][0])
        current_date_d=int(events[i][1])
        previous_date_y = int(events[i-1][0])
        previous_date_d=int(events[i-1][1])
        if(i == 0 and next_date_y==current_date_y and next_date_d-current_date_d==1):
            adjacent_days.append(events[i][0])
            adjacent_days.append(events[i][1])
            adjacent_days.append(events[i+1][0])
            adjacent_days.append(events[i+1][1])
        if (i != 0 and next_date_y == current_date_y and next_date_d-current_date_d):
            if(current_date_y == previous_date_y and current_date_d-previous_date_d == 1):
                if(i == len(events)-2):
                    # altrimenti usciva dal loop senza aggiungere un'eventuale ultima ondata di calore
                    adjacent_days.append(events[i+1][0])
                    adjacent_days.append(events[i+1][1])
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

                    adjacent_days.append(events[i][0])
                    adjacent_days.append(events[i][1])
                    adjacent_days.append(events[i+1][0])
                    adjacent_days.append(events[i+1][1])
                else:
                    adjacent_days = []

                    adjacent_days.append(events[i][0])
                    adjacent_days.append(events[i][1])
                    adjacent_days.append(events[i+1][0])
                    adjacent_days.append(events[i+1][1])
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
    i = 0
    for i in range(0, len(heat_waves)):
        j = 0
        hw = heat_waves[i]
        for j in range(0, len(hw)):
            temp_hw.append(temp_matrix[int(hw[j][0])][int(hw[j][1])])

        cluster_hw.append(temp_hw)
        temp_hw = []
    return cluster_hw


# manca funzione per la magnitude in cluster_hw ho solo i valori-> ho perso le posizioni in matrice
# trovare un modo di passare a get properties le posizioni ( posso sovrascrivere get_values all'interno della classe
# ho riarrangiare la classe in altro modo)
def get_properties(temp_matrix, heat_waves):
    """restituisce le proprietà delle ondate di calore in ordine: 
    temperatura massima
    durata
    magnitudo
    intensità"""
    #[T_max, length,magnitude,intensity]
    cluster_hw = values_hw(temp_matrix, heat_waves)
    cluster_properties = []
    properties = []
    #my_generic_iterable = map(str.upper, cluster_hw)
    i = 0
    for i in range(0, len(cluster_hw)):
       # for i in my_generic_iterable:
        T_max = max(cluster_hw[i])
        length = len(cluster_hw[i])

        cluster_anomalies = np.array([])
        mean_temp = mean_temp_wod(temp_matrix, int(heat_waves[i][int(len(
            heat_waves[i])/2)][0]), get_wod(int(heat_waves[i][int(len(heat_waves[i])/2)][1])))
        j = 0
        for j in range(0, len(cluster_hw[i])):
            # la temperatura su cui baso il calcolo è quella del giorno di mezzo della hw
            # l'[1] alla fine è il girono nel cluser di posizioni della matrice di temperature
            cluster_anomalies = np.append(
                cluster_anomalies, cluster_hw[i][j]-mean_temp)
        magnitude = np.mean(cluster_anomalies)
        intensity = magnitude*length
        properties.append(T_max)
        properties.append(length)
        properties.append(magnitude)
        properties.append(intensity)
        cluster_properties.append(properties)
        properties = []
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
    i = 0
    for i in range(0, len(cluster_hw)):

        mean_temp = mean_temp_wod(temp_matrix, int(heat_waves[i][int(len(
            heat_waves[i])/2)][0]), get_wod(int(heat_waves[i][int(len(heat_waves[i])/2)][1])))
        means.append(mean_temp)
    return means


#men = mean_temp_wod(temp_matrix, 56, 6)
#woy = warm_days_woy(temp_matrix, 60)
#prov = get_heat_waves(woy, date_matrix)
## mean=means(prov,temp_matrix)
##val = values_hw(temp_matrix, prov)
## anomal=anomalies(prov,temp_matrix)
#
#prop = get_properties(temp_matrix, prov)
#print(prop)


# DA VEDERE I RANGE DEI LOOP, TROVARE MODO PER ELIMINARE I LOOP
