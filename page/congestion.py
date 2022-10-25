# congestion.py

import statistics
import streamlit as st
import pandas as pd
import csv
import math
import folium
from folium.plugins import HeatMap
from heapq import *
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import plotly.express as px
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
            date(2022, 10, 24))
    with col2:
        time_selected = st.time_input('Please enter the time', time(0, 0))

    weekday = date_selected.isoweekday()
    hour = time_selected.hour
    return weekday, hour


def getFileLoc(weekday, hour):
    """Determine the name of the road network file 
       to be used based on the day and hour of the week

    Args:
        weekday (int): the weekday entered
        hour (int): the hour entered

    Returns:
        str, str: the location of the file to be used
    """
    if weekday < 6:
        hourStart = str(hour)
        if len(hourStart) == 1:
            hourStart = '0'+hourStart
        hourEnd = str(hour+1)
        if len(hourEnd) == 1:
            hourEnd = '0'+hourEnd
        mapFile = 'csv/map/weekday/0408' + hourStart + hourEnd + '_map.csv'
        segmentFile = 'csv/segment/'+'weekday/0408' + hourStart + hourEnd + '.csv'
    else:
        hourStart = str(int(hour/2)*2)
        if len(hourStart) == 1:
            hourStart = '0'+hourStart
        hourEnd = str(int(hour/2)*2+2)
        if len(hourEnd) == 1:
            hourEnd = '0'+hourEnd
        mapFile = 'csv/map/weekend/0203' + hourStart + hourEnd + '_map.csv'
        segmentFile = 'csv/segment/'+'weekend/0203' + hourStart + hourEnd + '.csv'

    return mapFile, segmentFile


def congestion_color(number_car):
    """determine congestion based on the number of vehicles

    Args:
        number_car (int): number of vehicles

    Returns:
        str: color of the line on the map
    """
    if number_car < 10:
        return 'lightgreen'
    elif number_car < 20:
        return 'yellow'
    else:
        return 'red'


def show_congestion_route_map(data_map):
    """show the congestion map

    Args:
        data_map (pd.DataFrame): the map data
    """
    "show the load profress"
    bar = st.progress(0)
    mmap = folium.Map(location=[39.9632245, 116.280983], zoom_start=11,
                      tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                      attr='default', key='result')

    index = -1
    for i in data_map.iterrows():
        index = index + 1
        # get the geometry point
        geometry = i[1]['Geometry'].split(";")
        number_car = int(i[1]['NumberPoints'])
        # get the start and end point
        point_start = geometry[0].split(':')
        point_end = geometry[len(geometry)-1].split(':')
        # get the line to print
        line = [[float(point_start[1]), float(point_start[0])]] + \
            [[float(point_end[1]), float(point_end[0])]]
        # add the line to the map
        folium.PolyLine(line, color=congestion_color(
            number_car)).add_to(mmap)
        bar.progress(index/(len(data_map)-1))
    # show the map
    folium_static(mmap)


def show_congestion_heat_map(data_segment):
    """show the heat map of the congestion

    Args:
        data_segment (pd.DataFrame): the segement data
    """
    # extracting longitude and latitude values to separate lists
    longs = data_segment['long'].tolist()
    lats = data_segment['lat'].tolist()
    # calculating mean longitude and latitude values
    meanLong = statistics.mean(longs)
    meanLat = statistics.mean(lats)
    # create base map object using Map()
    mapObj = folium.Map(location=[meanLat, meanLong], zoom_start=14.5)
    # create heatmap layer
    heatmap = HeatMap(list(zip(lats, longs)),
                      min_opacity=0.2,

                      radius=50, blur=50,
                      max_zoom=1)
    # add heatmap layer to base map
    heatmap.add_to(mapObj)
    # show the map
    folium_static(mapObj)


def main():
    """the main part of the page
    """
    # create the container blocks
    input_congestion = st.container()
    dataset = st.container()
    congestion_route_map = st.container()
    congestion_heat_map = st.container()

    # input of the datetime
    with input_congestion:
        week, hour = datetimeInput()
        # get the path of the map file
        file_map, file_segment = getFileLoc(week, hour)

    # charge the dataset
    with dataset:
        data_map = pd.read_csv(file_map)
        data_segment = pd.read_csv(
            file_segment, names=['taxi_id', 'time', 'long', 'lat'])

    # show the congestion map
    with congestion_route_map:
        st.title('Route map')
        show_congestion_route_map(data_map)

    # show the heat map of the congestion
    with congestion_heat_map:
        st.title('Heat map')
        show_congestion_heat_map(data_segment)
