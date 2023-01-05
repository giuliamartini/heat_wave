
import pandas as pd
import numpy as np


def remove_leap_years(temp):

    date = pd.Series(

        pd.date_range("1950-01-01", periods=len(temp)-1, freq="D")

    )
    date_df = {'date': date, 'year': date.dt.year,
               'month': date.dt.month, 'day': date.dt.day}
    dates_arr = date_df['date']
    i = 0
    years = np.array
    months = np.array
    days = np.array
    dates = np.array
    for i in range(0, len(temp)-1):
        dates = np.append(dates, dates_arr[i].date())
        years = np.append(years, dates_arr[i].year)
        months = np.append(months, dates_arr[i].month)
        days = np.append(days, dates_arr[i].day)

        i += 1

    j = 0

    for j in range(0, 26280):
        if (months[j] == 2 and days[j] == 29):
            months = np.delete(months, j)
            days = np.delete(days, j)
            years = np.delete(years, j)
            temp = np.delete(temp, j)
            dates = np.delete(dates, j)
            j += 1

    return temp


def get_year(date):

    year = date.astype('datetime64[Y]').astype(int) + 1970
    return year.astype(int)


def get_month(date):
    month = date.astype('datetime64[M]').astype(int) % 12 + 1
    return month.astype(int)


def get_day(date):
    day = date - date.astype('datetime64[M]') + 1
    return day.astype(int)


def window_years_int(year):

    if year in range(0, 4):
        result = np.arange(0, year+5)
        return result

    if year in range(71-4, 71):
        result = np.arange(year-4, 71)
        return result
    else:
        result = np.arange(year-4, year+5)
        return result


def window_days(temp_matrix, year, day):
    # temp_matrix = window_years(temp, year)

    if day in range(0, 10) and year == 0:
        index = np.arange(0, 21-day)

        return temp_matrix[year, index]

    # fai che per gli anni non di confine per il cluster di dati generali
    # ma di confine per i 9 anni posso guardare 5 giorni indietro, usa ravel
    # tanto ritorna un vettore
    if day in range(0, 10) and year != 0:
        index = np.arange(0, 10-day)
        previous_year = np.array([])
        previous_year = np.append(
            previous_year, temp_matrix[year-1, 355+day+index])
        index1 = np.arange(0, 11)
        previous_year = np.append(previous_year, temp_matrix[year, index1])
        return previous_year

    if day in range(355, 365) and year == 71:
        if(day>366):
            raise Exception("day is out of range")
        index = np.arange(day-10, 365)
        return temp_matrix[year, index]
    if day in range(355, 365) and year != 71:
        index = np.arange(day-10, 365)
        next_year = np.array([])
        next_year = np.append(next_year, temp_matrix[year, index])
        index1 = np.arange(0, 10-(365-day))
        next_year = np.append(next_year, temp_matrix[year+1, index1])
        return next_year
    else:
        index = np.arange(day-10, day+10)

        return temp_matrix[year, index]

# se serve fornisce la parte di matrice per 9 anni ma di base si può usare l'insieme di indici con window_days


def window_years(temp_matrix, year):

    # temp_matrix = np.reshape(temp, (size/365, 365))
    if year in range(0, 4):
        return temp_matrix[0:year+4]

    if year in range(72-4, 72):
        return temp_matrix[(year-4):71]
 
    if year>72:
        raise Exception("year is out of range") 
    else:
        return temp_matrix[(year-4):(year+4)]

#percentile calcolato per ogni finestra di 20 giorni in un anno sulla finestra di 9 anni centrata sull'anno voluto
def percentile(temp_matrix, year, p_val):
    percentile_each_wod = np.array([])

    years = window_years_int(year)
   
    i = 0
    for i in range(0, 19):
        temp_wod=np.array([])
        # nel caso voglia la finestra di tutti i giorni(cambia i*20 con i)
        # for i in range(0, 365):
        # divido in 18 finestre di 20 giorni
        # fare la finestra finale di 5 giorni (sfrutta window days)
        if(i == 19):
            
            j = 0

            for j in range(0, len(years)):
               # ogni giorni risente della media dei 10 giorni prima e dopo
                temps = window_days(temp_matrix, years[j], 360)
               
                temp_wod = np.append(temp_wod, temps)
                

            perc = np.percentile(temp_wod, p_val)
    
            percentile_each_wod = np.append(percentile_each_wod, perc)
           
            

        else:

            j = 0

            for j in range(0, len(years)):
               # ogni giorni risente della media dei 10 giorni prima e dopo
                temps = window_days(temp_matrix, years[j], i*20)
                
                temp_wod = np.append(temp_wod, temps)
                

            perc = np.percentile(temp_wod, p_val)
            percentile_each_wod = np.append(percentile_each_wod, perc)
            
    return percentile_each_wod


def mean_temp(temp_matrix, year):
    mean_each_year = np.array([])
    years = window_years_int(year)
    size = len(years)
    j = 0
    for j in range(0, size):
        i = 0
        # divido in 18 finestre di 20 giorni e 1 da 5
        for i in range(0, 19):
           # ogni giorni risente della media dei 10 giorni prima e dopo
            if(i == 19):
                temp2 = window_days(temp_matrix, years[j], 360)
                mean = np.mean(temp2)
                mean_each_year = np.append(mean_each_year, mean)
                i += 1
            else:
                temp2 = window_days(temp_matrix, years[j], i*20)
                mean = np.mean(temp2)
                mean_each_year = np.append(mean_each_year, mean)
                i += 1

    mean_each_year = np.reshape(mean_each_year, (len(years), 19))

    return mean_each_year


def mean_temp_wod(temp_matrix, year, wod):
    years = window_years_int(year)
    j = 0
    for j in range(0, len(years)):

        # divido in 18 finestre:17 di 20 giorni e 1 da 5
        if(wod==19):
            temp2 = window_days(temp_matrix, years[j], 360)
            mean=np.mean(temp2)
        # ogni giorni risente della media dei 10 giorni prima e dopo
        
        else:
            temp2 = window_days(temp_matrix, years[j], wod*20)
            
            mean = np.mean(temp2)
       
    return mean


def print_arr(arr):
    i = 0
    for i in range(0, len(arr)):
        print(arr[i])


def get_wod(day):
    return int(day/20)

