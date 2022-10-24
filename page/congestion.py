# congestion.py

import re
import streamlit as st
import csv
import math
import folium
from heapq import *
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from datetime import datetime, time, timedelta, date
from math import ceil


def datetimeInput():
    """Enter the time to perform
    Returns:
        int, int: the week and hour entered
    """
    col1, col2 = st.columns(2)
    with col1:
        date_selected = st.date_input(
            "Please enter the date",
            date(2020, 6, 6))
    with col2:
        time = st.time_input('Please enter the time', time(0, 0))

    weekday = date_selected.isoweekday()
    hour = time.hour
    return weekday, hour


def getFileLoc(weekday, hour):
    """Determine the name of the road network file 
       to be used based on the day and hour of the week

    Args:
        weekday (int): the weekday entered
        hour (int): the hour entered

    Returns:
        str: the location of the file to be used
    """
    if weekday < 6:
        hourStart = str(hour)
        if len(hourStart) == 1:
            hourStart = '0'+hourStart
        hourEnd = str(hour+1)
        if len(hourEnd) == 1:
            hourEnd = '0'+hourEnd
        mapFile = 'weekday/0408' + hourStart + hourEnd + '_map.csv'
    else:
        hourStart = str(int(hour/2)*2)
        if len(hourStart) == 1:
            hourStart = '0'+hourStart
        hourEnd = str(int(hour/2)*2+2)
        if len(hourEnd) == 1:
            hourEnd = '0'+hourEnd
        mapFile = 'weekend/0203' + hourStart + hourEnd + '_map.csv'

    file = 'csv/map/'+mapFile
    return file


def main():
    """the main part of the page
    """
    # create the container blocks
    input_congestion = st.container()

    with input_congestion:
        # select the time
        datetimeInput()
