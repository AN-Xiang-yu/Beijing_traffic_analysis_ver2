# density.py

import tools as t
import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from math import ceil

# contant variable
# number of taxis in the sample data at Beijing at 2008
NUMBER_TAXI_SAMPLE = 10134
# total number of taxis in the data at Beijing at 2008
NUMBER_TAXI_TOTAL = 66000
# total number of cars in the data at Beijing at 2008
NUMBER_CAR_TOTAL = 3181000
# ratio of the total number of the taxis divided by number of taxis in samble in the data at Beijing at 2008
RATIO_TAXI_TOTAL_SAMPLE = NUMBER_TAXI_TOTAL/NUMBER_TAXI_SAMPLE
# ratio of the number of the cars divided by total number of taxis in the data at Beijing at 2008
RATIO_CAR_TAXI = NUMBER_CAR_TOTAL/NUMBER_TAXI_TOTAL
# area of Beijing / km^2
AREA_BEIJIGN = 1381


def charge_data(path):
    """charge and process the data

    Args:
        path (str): the path of the data

    Returns:
        pandas.DataFrame: the dataframe of the data charged
    """
    # charge the data
    data = pd.read_csv(path)
    # change the type of column time into datetime
    data['time'] = pd.to_datetime(data['time'], format='%Y/%m/%d %H:%M:%S')
    # take the column time as the index
    data = data.set_index('time')
    return data


def density_taxi_period_hour(time_start_selected, time_end_selected, data):
    """ get the density of the taxis of a selected time in Beijing

    Args:
        time_start_selected (str):
            the start of the selected time 
        time_end_selected (str):
            the end of the selected time 
        data (pandas.DataFrame):
            the data of the Beijing taxis trafic data 

    Returns:
        float: the density of the taxis of a selected time in Beijing
    """

    # declare the total number of the cars of the selected time
    num_car_total = 0
    # total number of days
    num_day = len(data.day.unique())

    # convert the type of selected time into datatime
    time_start_selected_to_datetime = datetime.strptime(
        time_start_selected, '%H:%M:%S')
    time_end_selected_to_datetime = datetime.strptime(time_end_selected,
                                                      '%H:%M:%S')
    # get the hour, minute and second of the the selected time
    hour_start = time_start_selected_to_datetime.hour
    minute_start = time_start_selected_to_datetime.minute
    second_start = time_start_selected_to_datetime.second
    hour_end = time_end_selected_to_datetime.hour
    minute_end = time_end_selected_to_datetime.minute
    second_end = time_end_selected_to_datetime.second

    # total number of the cars of the selected time
    for day in data.day.unique():
        # calculate the number of the cars of each day of the selected time
        num_car_day = len(
            data[(data.index.day == day) & (data.index.hour >= hour_start)
                 & (data.index.minute >= minute_start) &
                 (data.index.second >= second_start) & (
                     data.index.hour <= hour_end)
                 & (data.index.minute <= minute_end) &
                 (data.index.second <= second_end)].groupby(["taxi_id"]))
        # accumulated the number of the cars
        num_car_total = num_car_total + num_car_day

    # calculate the density of the cars of the selected time
    # area of Beijing / km^2
    density = num_car_total / (num_day * AREA_BEIJIGN)
    return density


def density_car_period_hour(time_start_selected, time_end_selected, data):
    """ get the density of the taxis and cars of a selected time in Beijing

    Args:
        time_start_selected (str):
            the start of the selected time 
        time_end_selected (str):
            the end of the selected time 
        data (pandas.DataFrame):
            the data of the Beijing taxis trafic data 

    Returns:
        int, int: the density of the taxis and cars of a selected time in Beijing
    """
    # density of the taxis of a selected time in Beijing
    density_taxi = density_taxi_period_hour(
        time_start_selected, time_end_selected,
        data)
    # density of the taxis of a selected time in Beijing
    density_car = density_taxi * RATIO_CAR_TAXI * RATIO_TAXI_TOTAL_SAMPLE
    return ceil(density_taxi), ceil(density_car)


def display_density_hour(data):
    """show the density of cars and taxis according to the period choosed

        Args:
            data (pandas.DataFrame):
                the data of the Beijing taxis trafic data 

        Returns:
            int, int: the density of the taxis and cars of a selected time in Beijing
    """
    # select the time
    time_selected = st.slider('Please select the time for which you want to check the density:',
                              value=(time(00, 00, 00),
                                     time(23, 59, 59)),
                              step=timedelta(minutes=1),
                              format='H:mm')
    # get the time start and the time end
    time_start_selected, time_end_selected = time_selected
    # get the density of cars and taxis according to the period choosed
    density_taxi_hour, density_car_hour = density_car_period_hour(
        str(time_start_selected), str(time_end_selected), data)
    # show the result
    st.write('Taxis density between',
             time_start_selected, 'and', time_end_selected, 'is', density_taxi_hour, 'per km².')
    st.write('Cars density between',
             time_start_selected, 'and', time_end_selected, 'is', density_car_hour, 'per km².')

    return density_taxi_hour, density_car_hour


def density_taxi_period_weekday(weekday_selected, data):
    """ get the density of the taxis of a selected day in Beijing 

    Args:
    day_selected (int):
        the start of the selected time 

    data (pandas.DataFrame):
        the data of the Beijing taxis trafic data 

    Returns:
        int: the density of the taxis of a selected time in Beijing
    """

    # declare the total number of the taxis of the selected day
    num_taxi_total = len(data[data['weekday'] == weekday_selected].groupby(
        ["taxi_id"]))

    # calculate the density of the taxis of the selected day
    # area of Beijing / km^2
    density = num_taxi_total / (AREA_BEIJIGN)
    return density


def density_car_period_weekday(weekday_selected, data):
    """ get the density of the taxis and cars of a selected day in Beijing 

    Args:
    day_selected (int):
        the start of the selected time 

    data (pandas.DataFrame):
        the data of the Beijing cars trafic data 

    Returns: 
        int, int: the density of the taxis and cars of a selected weekday in Beijing
    """
    # he density of the cars of a selected day in Beijing
    density_taxi = density_taxi_period_weekday(
        weekday_selected,
        data)
    density_car = density_taxi * RATIO_CAR_TAXI * RATIO_TAXI_TOTAL_SAMPLE
    return ceil(density_taxi), ceil(density_car)


def display_density_weekday(data):
    """show the density of cars and taxis according to the period choosed


    Args:
        data (pandas.DataFrame): 
            the data of the Beijing taxis trafic data 

    Returns:
        int, int: the density of the taxis and cars of a selected day in Beijing
    """
    # initialize the corresponding weekday and his number
    weekday = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6,
    }
    # display the selectbox
    weekday_selected = st.selectbox(
        'Please select a weekday for which you want to check the density', list(
            weekday.keys()))
    # get the get the density of the taxis and cars of a selected day in Beijing
    density_taxi_weekday, density_car_weekday = density_car_period_weekday(
        weekday[weekday_selected], data)
    # show the result
    st.write('Taxis density of ',
             weekday_selected, 'is', density_taxi_weekday, 'per km²')
    st.write('Cars density of ',
             weekday_selected, 'is', density_car_weekday, 'per km²')
    return density_taxi_weekday, density_car_weekday


def main():
    """the main part of the page
    """

    # create the container blocks
    dataset = st.container()
    density_hour = st.container()
    density_weekday = st.container()

    with dataset:
        path = "https://media.githubusercontent.com/media/AN-Xiang-yu/Beijing_traffic_analysis_ver2/main/csv/taxi_data.csv?token=AO23ECKDKJGEQIFDOXFJHIDDKZNAQ"
    #     data = charge_data(path)

    # with density_hour:
    #     display_density_hour(data)

    # with density_weekday:
    #     display_density_weekday(data)
