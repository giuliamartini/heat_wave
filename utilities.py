
import numpy as np


def window_years_int(year,temp_matrix):

    if year in range(0, 4):
        result = np.arange(0, year+5)
        return result

    if year in range(len(temp_matrix)-4, len(temp_matrix)-1):
        result = np.arange(year-4, len(temp_matrix)-1)
        return result
    else:
        result = np.arange(year-4, year+5)
        return result


def window_days(temp_matrix, year, day):
  
    if day in range(0, 10) and year == 0:
        index = np.arange(0, 21-day)

        return temp_matrix[year, index]

    if day in range(0, 10) and year != 0:
        index = np.arange(0, 10-day)
        previous_year = np.array([])
        previous_year = np.append(
            previous_year, temp_matrix[year-1, len(temp_matrix[0])-10+day+index])
        index1 = np.arange(0, 11)
        previous_year = np.append(previous_year, temp_matrix[year, index1])
        return previous_year

    if day in range(len(temp_matrix[0])-10, len(temp_matrix[0])) and year == len(temp_matrix)-1:
        if(day > 366):
            raise Exception("day is out of range")
        index = np.arange(day-10, 365)
        return temp_matrix[year, index]
    if day in range(len(temp_matrix[0])-10, len(temp_matrix[0])) and year != len(temp_matrix)-1:
        index = np.arange(day-10, 365)
        next_year = np.array([])
        next_year = np.append(next_year, temp_matrix[year, index])
        index1 = np.arange(0, 10-(len(temp_matrix[0])-day))
        next_year = np.append(next_year, temp_matrix[year+1, index1])
        return next_year
    else:
        index = np.arange(day-10, day+10)

        return temp_matrix[year, index]

def window_years(temp_matrix, year):

    # temp_matrix = np.reshape(temp, (size/365, 365))
    if year in range(0, 4):
        return temp_matrix[0:year+4]

    if year in range(len(temp_matrix)-4, len(temp_matrix)-1):
        return temp_matrix[(year-4):len(temp_matrix)-1]

    if year > len(temp_matrix)-1:
        raise Exception("year is out of range")
    else:
        return temp_matrix[(year-4):(year+4)]


def percentile_d(temp_matrix, year, p_val):
    percentile_each_day = np.array([])

    years = window_years_int(year, temp_matrix)

    for i in range(0, len(temp_matrix[0])):
        temp_wod = np.array([])

        for j in range(0, len(years)):
            temps = window_days(temp_matrix, years[j], i)
            temp_wod = np.append(temp_wod, temps)

        perc = np.percentile(temp_wod, p_val)

        percentile_each_day = np.append(percentile_each_day, perc)
    return percentile_each_day


def mean_temp_day(temp_matrix, year, day):
    if year > len(temp_matrix)-1 or year < 0:
        raise Exception("year is out of range")
    if day > len(temp_matrix[0]) or day < 0:
        raise Exception("day is out of range")
    temps_each_year = np.array([])
    years = window_years_int(year, temp_matrix)
    for j in range(0, len(years)):
        temp = window_days(temp_matrix, years[j], day)
        temps_each_year = np.append(temps_each_year, temp)

    mean = np.mean(temps_each_year)

    return mean

