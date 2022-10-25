# congestion.py

import streamlit as st
import pandas as pd
import csv
import math
import folium
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


def main():
    """the main part of the page
    """
    # create the container blocks
    input_congestion = st.container()
    dataset = st.container()

    with input_congestion:
        # input of the datetime
        week, hour = datetimeInput()
        # get the path of the map file
        file = getFileLoc(week, hour)
        bar = st.progress(0)

    with dataset:
        data = pd.read_csv(file)
        # fig = px.density_mapbox(data, lat='lat', lon='long', z='n_points', radius=10,
        #                         center=dict(lat=39.9632245, lon=116.280983), zoom=10,
        #                         mapbox_style="stamen-terrain")
        # fig = px.line_mapbox(data, lat="lat", lon="long",
        #                      color="n_points", zoom=3, height=300)

        # fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat=41,
        #                   margin={"r": 0, "t": 0, "l": 0, "b": 0})
        # st.plotly_chart(fig, use_container_width=True)
        mmap = folium.Map(location=[39.9632245, 116.280983], zoom_start=11,
                          tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                          attr='default', key='result')
        index = -1
        for i in data.iterrows():
            index = index + 1

            geometry = i[1]['Geometry'].split(";")
            number_car = int(i[1]['NumberPoints'])

            point_start = geometry[0].split(':')
            point_end = geometry[len(geometry)-1].split(':')
            line = [[float(point_start[1]), float(point_start[0])]] + \
                [[float(point_end[1]), float(point_end[0])]]
            folium.PolyLine(line, color=congestion_color(
                number_car)).add_to(mmap)
            bar.progress(index/(len(data)-1))

        folium_static(mmap)
