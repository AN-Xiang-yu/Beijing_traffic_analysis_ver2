# density.py

import page.tools as t
import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from math import ceil

# contant variable
# number of taxis in the sample data at Beijing at 2008
NUMBER_TAXI_SAMPLE = 1000

# total number of taxis in the data at Beijing at 2008
NUMBER_TAXI_TOTAL_BEIJING = 66000
# total number of cars in the data at Beijing at 2008
NUMBER_CAR_TOTAL_BEIJING = 3181000
# ratio of the total number of the taxis divided by number of taxis in samble in the data at Beijing at 2008
RATIO_TAXI_TOTAL_SAMPLE_BEIJING = NUMBER_TAXI_TOTAL_BEIJING/NUMBER_TAXI_SAMPLE
# ratio of the number of the cars divided by total number of taxis in the data at Beijing at 2008
RATIO_CAR_TAXI_BEIJING = NUMBER_CAR_TOTAL_BEIJING/NUMBER_TAXI_TOTAL_BEIJING
# area of Beijing / km^2
AREA_BEIJIGN_BEIJING = 1381

# total number of taxis in the data at Paris at 2008
NUMBER_TAXI_TOTAL_PARIS = 15000
# total number of cars in the data at Paris at 2008
NUMBER_CAR_TOTAL_PARIS = 2600000
# ratio of the total number of the taxis divided by number of taxis in samble in the data at Paris at 2008
RATIO_TAXI_TOTAL_SAMPLE_PARIS = NUMBER_TAXI_TOTAL_PARIS/NUMBER_TAXI_SAMPLE
# ratio of the number of the cars divided by total number of taxis in the data at Paris at 2008
RATIO_CAR_TAXI_PARIS = NUMBER_CAR_TOTAL_PARIS/NUMBER_TAXI_TOTAL_PARIS
# area of Paris / km^2
AREA_BEIJIGN_PARIS = 105.4

# total number of taxis in the data at Paris at 2008
NUMBER_TAXI_TOTAL_NEWYORK = 13605
# population of New York in 2006
POPULATION_NEWYORK = 8214426
# population having a car of New York in 2010
POPULATION_RATIO_CAR_NEWYORK = 0.23
# total number of cars in the data at New York at 2008
NUMBER_CAR_TOTAL_NEWYORK = POPULATION_NEWYORK * POPULATION_RATIO_CAR_NEWYORK
# ratio of the total number of the taxis divided by number of taxis in samble in the data at New York at 2008
RATIO_TAXI_TOTAL_SAMPLE_NEWYORK = NUMBER_TAXI_TOTAL_NEWYORK/NUMBER_TAXI_SAMPLE
# ratio of the number of the cars divided by total number of taxis in the data at New York at 2008
RATIO_CAR_TAXI_NEWYORK = NUMBER_CAR_TOTAL_NEWYORK/NUMBER_TAXI_TOTAL_NEWYORK
# area of New York / km^2
AREA_BEIJIGN_NEWYORK = 783.8


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

    # declare the total number of the taxis of the selected time
    num_taxi_total = 0
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

    # total number of the taxis of the selected time
    for day in data.day.unique():
        # calculate the number of the cars of each day of the selected time
        num_car_day = len(
            data[(data.index.day == day) & (data.index.hour >= hour_start)
                 & (data.index.minute >= minute_start) &
                 (data.index.second >= second_start) & (
                     data.index.hour <= hour_end)
                 & (data.index.minute <= minute_end) &
                 (data.index.second <= second_end)].groupby(["taxi_id"]))
        # accumulated the number of the taxis
        num_taxi_total = num_taxi_total + num_car_day

    # calculate the density of the taxis of the selected time
    # area of Beijing / km^2
    density_Beijing = num_taxi_total / (num_day * AREA_BEIJIGN_BEIJING)
    density_Paris = num_taxi_total / (num_day * AREA_BEIJIGN_PARIS)
    density_NewYork = num_taxi_total / (num_day * AREA_BEIJIGN_NEWYORK)
    return density_Beijing, density_Paris, density_NewYork


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
    # density of the taxis of a selected time
    density_Beijing, density_Paris, density_NewYork = density_taxi_period_hour(
        time_start_selected, time_end_selected,
        data)
    density_taxi_Beijing = density_Beijing * RATIO_TAXI_TOTAL_SAMPLE_BEIJING
    density_taxi_Paris = density_Paris * RATIO_TAXI_TOTAL_SAMPLE_PARIS
    density_taxi_NewYork = density_NewYork * RATIO_TAXI_TOTAL_SAMPLE_NEWYORK
    # density of the taxis of a selected time in Beijing
    density_car_Beijing = density_taxi_Beijing * RATIO_CAR_TAXI_BEIJING
    density_car_Paris = density_taxi_Paris * RATIO_CAR_TAXI_PARIS
    density_car_NewYork = density_taxi_NewYork * RATIO_CAR_TAXI_NEWYORK
    return ceil(density_taxi_Beijing), ceil(density_taxi_Paris), ceil(density_taxi_NewYork), ceil(density_car_Beijing), ceil(density_car_Paris), ceil(density_car_NewYork)


def display_density_hour(data):
    """show the density of cars and taxis according to the period choosed

        Args:
            data (pandas.DataFrame):
                the data of the Beijing taxis trafic data 
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
    density_taxi_hour_Beijing, density_taxi_hour_Paris, density_taxi_hour_NewYrok, density_car_Beijing, density_car_Paris, density_car_NewYork = density_car_period_hour(
        str(time_start_selected), str(time_end_selected), data)
    # show the result
    st.write('Taxis density between',
             time_start_selected, 'and', time_end_selected, 'in Beijing is', density_taxi_hour_Beijing, 'per km².')
    st.write('Taxis density between',
             time_start_selected, 'and', time_end_selected, 'in Paris is', density_taxi_hour_Paris, 'per km².')
    st.write('Taxis density between',
             time_start_selected, 'and', time_end_selected, 'in NewYork is', density_taxi_hour_NewYrok, 'per km².')
    st.write('Cars density between',
             time_start_selected, 'and', time_end_selected, 'in Beijing is', density_car_Beijing, 'per km².')
    st.write('Cars density between',
             time_start_selected, 'and', time_end_selected, 'in Paris is', density_car_Paris, 'per km².')
    st.write('Cars density between',
             time_start_selected, 'and', time_end_selected, 'in NewYork is', density_car_NewYork, 'per km².')


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
    density_Beijing = num_taxi_total / (AREA_BEIJIGN_BEIJING)
    density_Paris = num_taxi_total / (AREA_BEIJIGN_PARIS)
    density_NewYork = num_taxi_total / (AREA_BEIJIGN_NEWYORK)
    return density_Beijing, density_Paris, density_NewYork


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
    # the density of the cars of a selected day in Beijing
    density_Beijing, density_Paris, density_NewYork = density_taxi_period_weekday(
        weekday_selected,
        data)
    density_taxi_Beijing = density_Beijing * RATIO_TAXI_TOTAL_SAMPLE_BEIJING
    density_taxi_Paris = density_Paris * RATIO_TAXI_TOTAL_SAMPLE_PARIS
    density_taxi_NewYork = density_NewYork * RATIO_TAXI_TOTAL_SAMPLE_NEWYORK
    # density of the taxis of a selected time in Beijing
    density_car_Beijing = density_taxi_Beijing * RATIO_CAR_TAXI_BEIJING
    density_car_Paris = density_taxi_Paris * RATIO_CAR_TAXI_PARIS
    density_car_NewYork = density_taxi_NewYork * RATIO_CAR_TAXI_NEWYORK
    return ceil(density_taxi_Beijing), ceil(density_taxi_Paris), ceil(density_taxi_NewYork), ceil(density_car_Beijing), ceil(density_car_Paris), ceil(density_car_NewYork)


def display_density_weekday(data):
    """show the density of cars and taxis according to the period choosed


    Args:
        data (pandas.DataFrame): 
            the data of the Beijing taxis trafic data 
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
    density_taxi_hour_Beijing, density_taxi_hour_Paris, density_taxi_hour_NewYrok, density_car_Beijing, density_car_Paris, density_car_NewYork = density_car_period_weekday(
        weekday[weekday_selected], data)
    # show the result
    # show the result
    st.write('Taxis density of ',
             weekday_selected, 'in Beijing is', density_taxi_hour_Beijing, 'per km².')
    st.write('Taxis density of ',
             weekday_selected,  'in Paris is', density_taxi_hour_Paris, 'per km².')
    st.write('Taxis density of ',
             weekday_selected, 'in NewYork is', density_taxi_hour_NewYrok, 'per km².')
    st.write('Cars density of ',
             weekday_selected, 'in Beijing is' 'in Beijing is', density_car_Beijing, 'per km².')
    st.write('Cars density of ',
             weekday_selected, 'in Beijing is' 'in Paris is', density_car_Paris, 'per km².')
    st.write('Cars density of ',
             weekday_selected, 'in Beijing is' 'in NewYork is', density_car_NewYork, 'per km².')


def main():
    """the main part of the page
    """

    # create the container blocks
    dataset = st.container()
    density_hour = st.container()
    density_weekday = st.container()

    # charge the dataset
    with dataset:
        path = "csv/taxi_data_reduced.csv"
        data = charge_data(path)

    with density_hour:
        display_density_hour(data)

    with density_weekday:
        display_density_weekday(data)
