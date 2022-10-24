import streamlit as st
import math
import re
import csv
import datetime
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from heapq import *


def searchPoint(lon, lat, position_of_file_data, Pointtype):
    
    with open(position_of_file_data, 'r') as f:
    
        next(f)     
    
        dis = math.inf      
        reader = csv.reader(f)
    
        for row in reader:
        
            geo = str(row[5]).split(';')
    
            for i in geo:
                longitudeM = str(i).split(':')[0]
                latitudeM = str(i).split(':')[1]

                tempdistance = ((lon-float(longitudeM))*10000)**2 + \
                    ((lat-float(latitudeM))*10000)**2
    
                if tempdistance < dis:
                    dis = tempdistance     
    
                    if Pointtype == 0:      
                        idPoint = row[2]
    
                    else:                  
                        idPoint = row[1]
    return int(idPoint)



def initGraph(fileLoc):

    graph = {1: {1: 0}}     
   
    for row in csv.reader(open(fileLoc), delimiter=','):
     
        if row[0] == "LinkID":      
            continue
        
        if int(row[1]) not in graph.keys():
            graph[int(row[1])] = {}

        
        if int(row[2]) not in graph.keys():
            graph[int(row[2])] = {}
        
        graph[int(row[1])][int(row[2])] = float(row[3])
       
        if int(row[1]) not in graph[int(row[2])].keys():
            graph[int(row[2])][int(row[1])] = math.inf  
      
        else:
            graph[int(row[2])][int(row[1])] = float(row[2])
    
    return graph


def initialisedistanceance(graph, sts):

    """initiliaze distance
    Args:
        graph 
        sts
    Returns:
        distance
    """
    
    distance = {sts: 0}
    
    for vertex in graph:
    
        if vertex != sts:
     
            distance[vertex] = math.inf
    
    return distance


def Dijkstra(graph, s):
            
    """Dijkstra
    Args:
        graph 
        s
    Returns:
        parent_dij 
        distance
    """
    queue_dij = []     
    heappush(queue_dij, (0, s))
    seen = set()
    seen.add(s)
    parent_dij = {s: None}
    distance = initialisedistanceance(graph, s)

    while len(queue_dij) > 0:
        
        pair = heappop(queue_dij) 
        distance = pair[0]
        vertex = pair[1]
        seen.add(vertex)
        nodes = graph[vertex].keys()
        
        for w in nodes:
            
            if w not in seen:
                
                if distance + graph[vertex][w] < distance[w]:
                    heappush(queue_dij, (distance + graph[vertex][w], w))
                    parent_dij[w] = vertex
                    distance[w] = distance + graph[vertex][w]
    return parent_dij, distance


def datetimeInput():
    
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input(
            "Please enter the date",
            datetime.date(2020, 6, 6))
    
    with col2:
        time = st.time_input('Please enter the time', datetime.time(0, 0))

    week = date.isoweekday()
    hour = time.hour
    
    return week, hour


def getLoc_of_file(week, hour):
    # Determine the name of the road network file to be used based on the day and hour of the week
    
    if week < 6:
        hour_str_l = str(hour)
        
        if len(hour_str_l) == 1:
            hour_str_l = '0'+hour_str_l
        hourStrR = str(hour+1)
        
        if len(hourStrR) == 1:
            hourStrR = '0'+hourStrR
        
        mapFile = 'weekday/0408' + hour_str_l + hourStrR + '_map.csv'
    
    else:
        hour_str_l = str(int(hour/2)*2)
        
        if len(hour_str_l) == 1:
            hour_str_l = '0'+hour_str_l
        
        hourStrR = str(int(hour/2)*2+2)
        
        if len(hourStrR) == 1:
            hourStrR = '0'+hourStrR
        
        mapFile = 'weekend/0203' + hour_str_l + hourStrR + '_map.csv'

    fileLoc = 'csv/map/'+mapFile
    return fileLoc


def startEndPointInput(fileLoc):
    
    """select the starting and ending points
    Args:
        fileLoc (str): Path to the file that will be used
    Returns:
        float, float, float, float, int, int:  The first four are the latitude and longitude of the start and end points, 
        and the last two are the cluster numbers of the start and end points
    """
    
   
    if 'start_long' not in st.session_state:
        reset_start_end_point()
   
    
    m = folium.Map(location=[39.9632245, 116.280983], zoom_start=11,
                   tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                   attr='default')
    
    m.add_child(folium.LatLngPopup())
    
    map = st_folium(m, height=350, width=700)

    try:
        position = get_pos(map['last_clicked']['lat'],
                           map['last_clicked']['lng'])
        if st.session_state.start_lat == 0:
            st.session_state.start_lat = position[0]
            st.session_state.start_long = position[1]

        elif st.session_state.end_lat == 0:
            st.session_state.end_lat = position[0]
            st.session_state.end_long = position[1]
    
    except TypeError:
        st.write('Please click the point to select the starting and ending points')

    clear_start_point = st.button(
        "Reset the start point and end point", key="bt_reset_points")

    if clear_start_point:
        reset_start_end_point()

    col1, col2 = st.columns(2)
    
    with col1:
        showPointInfo(st.session_state.start_lat,
                      st.session_state.start_long, 'start point')
    with col2:
        showPointInfo(st.session_state.end_lat,
                      st.session_state.end_long, 'end point')

    if st.session_state.start_lat != 0 and st.session_state.end_lat != 0:
        frmNode = searchPoint(
            st.session_state.start_long, st.session_state.start_lat, fileLoc, 0)
        toNode = searchPoint(st.session_state.end_long,
                             st.session_state.end_lat, fileLoc, 1)

        return st.session_state.start_long, st.session_state.start_lat, st.session_state.end_long, st.session_state.end_lat, frmNode, toNode


    return 0, 0, 0, 0, 0, 0


def getPointPassed(toNode, parent_dij):

    """getPointPassed
    Args:
        toNode 
        parent_dij
    Returns:
        recordlatlong []
    """
    recordlatlong = []   # Record the latitude and longitude points passed from the starting point to the end point in this way
    counter = 0       # Record the number of geometries passing through the road

    try:
        while parent_dij[toNode] is not None:
            frmN = parent_dij[toNode]
            
            for row in csv.reader(open('csv/mMap.csv'), delimiter=','):
                
                if row[0] == "LinkID":
                    continue
                
                if str(row[1]) == str(frmN) and str(row[2]) == str(toNode):
                    counter += 1
                    geo = str(row[5]).split(';')
                    geo.reverse()
                    
                    for i in geo:
                        longitudeTmp = float(str(i).split(':')[0])
                        latitudeTmp = float(str(i).split(':')[1])
                        recordlatlong.append([latitudeTmp, longitudeTmp])
            
            toNode = frmN
    
    except TypeError:
        st.write('No cluster found')

    st.write("Number of cluster：" + str(counter))
    if counter == 0:
        st.write("No reachable path found")
        exit(0)

    return recordlatlong


def showPath(recordlatlong, latFromT, lonFromT, latToT, lonToT):

    """show the path
    Args:
        recordlatlong []
        latFromT  latitude from
        lonFromT  longitude from
        latToT     latitude to
        lonToT     longitude to
    Returns:
            map
    """
    
    mmap = folium.Map(location=[39.9632245, 116.280983], zoom_start=11,
                      tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                      attr='default', key='result')
    
    start_line = [[latFromT, lonFromT], recordlatlong[len(recordlatlong)-1]]
    
    end_line = [[latToT, lonToT], recordlatlong[0]]
    
    distance_taxi = round(calcul_total_temps(recordlatlong), 3)
    
    average_time_taxi = round((distance_taxi/23)*60, 1)
    
    distance_start_walk = round(calcul_total_temps(start_line), 3)
    
    average_time_taxi_start_walk = round((distance_start_walk/7.5)*60, 1)
    
    distance_end_walk = round(calcul_total_temps(end_line), 3)
    
    average_time_taxi_end_walk = round((distance_end_walk/7.5)*60, 1)
    
    folium.PolyLine(start_line, color='red',
                    tooltip='walking path ' + str(distance_start_walk) + ' km for ' + str(average_time_taxi_start_walk)+' min').add_to(mmap)
    folium.PolyLine(end_line, color='red',
                    tooltip='walking path ' + str(distance_end_walk) + ' km for ' + str(average_time_taxi_end_walk)+' min').add_to(mmap)
    folium.PolyLine(recordlatlong, color='green',
                    tooltip='taxi path ' + str(distance_taxi) + ' km for ' + str(average_time_taxi)+' min').add_to(mmap)
    folium.Marker([latFromT, lonFromT],  tooltip='Start point',
                  icon=folium.Icon(color='blue')).add_to(mmap)
    folium.Marker([latToT, lonToT], tooltip='End point',
                  icon=folium.Icon(color='red')).add_to(mmap)
    
    mmap.add_child(folium.LatLngPopup())

    price_taxi = calcul_price_taxi(distance_taxi)
    
    st.write('For this trip you can expect to pay '+str(price_taxi)+" ¥")
    st.write('For this trip, you will need to walk for ' + str(distance_start_walk) +
             ' km for ' + str(average_time_taxi_start_walk)+' min')
    st.write('And then, you will need to take the taxi for ' + str(distance_taxi) +
             ' km for ' + str(average_time_taxi)+' min')
    st.write('And the end, you will need to walk for ' + str(distance_end_walk) +
             ' km for ' + str(average_time_taxi_end_walk)+' min')
    folium_static(mmap)


def get_pos(lat, long):
    
    """get the latitude and longitude of the point
    Args:
        lat (float): latitude of the point
        long (float): longitude of the point
    Returns:
        float, float: latitude and longitude of the point
    """
    return lat, long


def showPointInfo(lat, long, type_point):
    """show the informations of the latitude and longitude of the point
    Args:
        point_lat (float): _description_
        point_long (float): _description_
        type_point (str): type of the point 
    """
    if lat == 'Not defined':
        st.write("Please choose your "+type_point)
    else:
        st.write(type_point)
        st.write(lat, " ", long)


def reset_start_end_point():
    """reset the values of the latitude and longitude of the start and end points
    """
    # initialise point of start and end points
    st.session_state.start_long = 0
    st.session_state.start_lat = 0
    st.session_state.end_long = 0
    st.session_state.end_lat = 0



def calcul_distance_miles(lat1, lon1, lat2, lon2):

    """ calculate distance in miles 
       
    args : lat1, lon1,lat2,lon2 : latitudes and longitudes of 2 points
    returns : distance s in miles      
        
    """
    x = lon1 - lon2
    
    distance = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(x))
    
    if distance - 1 > 0:
        distance = 1
    
    elif distance + 1 < 0:
        distance = -1
    
    distance = math.acos(distance)
    distance = math.degrees(distance)
    miles = distance * 60 * 1.1515
    
    return miles

   
def distance_points(p1, p2):

    """ calculate distance between 2 points
       
        args : p1,p2, 2 points 
        returns : distance between 2 points in miles      
        
    """
    lat1, lon1 = p1
    lat2, lon2 = p2
        
    distance = calcul_distance_miles(lat1, lon1, lat2, lon2) * 1.609344
        
    return distance


def calcul_total_temps(recordlatlong):
    """Calculate total time
    Args:
        recordlatlong
    Returns:
        int: distance_cumul
    """    

    distance_cumul = 0

    for index in range(0, len(recordlatlong)):
        
        if(index != len(recordlatlong)-1):
            lat1 = recordlatlong[index][0]
            long1 = recordlatlong[index][1]
            p1 = (lat1, long1)
            lat2 = recordlatlong[index+1][0]
            long2 = recordlatlong[index+1][1]
            p2 = (lat2, long2)
            distance_cumul = distance_cumul + distance(p1, p2)
    
    return distance_cumul



def calcul_price_taxi(taxi_distance):
    """Calculate the cost of a cab ride
    Args:
        taxi_distance (float): kilometers traveled by cabs
    Returns:
        int: price of cab ride
    """

    km_base = 3  # kilometers for base price
    price_base = 10  # base price of taxi in Beijing in 2008
    km_price = 2  # Price over base km

    if taxi_distance <= km_base:
        return price_base
    else:
        return price_base + km_price * math.ceil(taxi_distance-km_base)


def main():
    """the main part of the page
    """

    lonFromT = 0

    week, hour = datetimeInput()


    fileLoc = getLoc_of_file(week, hour)

    lonFromT, latFromT, lonToT, latToT, frmNode, toNode = startEndPointInput(fileLoc)
    graph = initGraph(fileLoc)

    if lonFromT != 0:
        parent_dij, distance = Dijkstra(graph, frmNode)

        # get all the points passed
        recordlatlong = getPointPassed(toNode, parent_dij)
        # show the path at the map
        showPath(recordlatlong, latFromT, lonFromT, latToT, lonToT)
