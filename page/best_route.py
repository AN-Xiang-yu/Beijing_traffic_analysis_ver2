# best_route.py

import streamlit as st
import csv
import math
import folium
from heapq import *
import datetime
from streamlit_folium import folium_static
from streamlit_folium import st_folium


START_POINT = 0
END_POINT = 1


def searchPoint(long, lat, file, Pointtype):
    """Match the start node or end node based on the input latitude and longitude

    Args:
        long (float): longtitude of the node
        lat (float): latitude of the node
        file (str): the file used
        Pointtype (int): the type of the point (START_POINT/END_POINT)

    Returns:
        int: the id of the point to start or end
    """
    with open(file, 'r') as f:
        # skip first line
        next(f)
        # distance is initialized to infinity
        distance = math.inf
        # read files
        file = csv.reader(f)
        # Iterate through the geometry to find the closest point M(longM, latM) at distance (long, lat) and update the corresponding distance and idPoint in time
        for row in file:
            geometry = str(row[5]).split(';')
            for point in geometry:
                # Get to point M (longM, latM)
                longM, latM = str(point).split(
                    ':')[0], str(point).split(':')[1]
                # We can calculate its linear distance in latitude and longitude, and then display

                # Calculate the distance between M and the input point
                tempoDistance = ((long-float(longM))*10000)**2 + \
                    ((lat-float(latM))*10000)**2
                if tempoDistance < distance:
                    # tempoDistance is smaller than dis, then update distance, and update idPoint.
                    distance = tempoDistance
                    if Pointtype == START_POINT:      # Starting point
                        idPoint = row[2]
                    else:                   # Endpoint
                        idPoint = row[1]
    return int(idPoint)


# Initialize node distance data graph based on a specific road network
def initGraph(file):
    """initiliaze distance
    Args:
        file (str): the location of the file
    Returns:
        dict: the graph initialized
    """
    graph = {1: {1: 0}}     # Store data with dictionarY
    with open(file) as f:
        # skip first line
        next(f)
        for row in csv.reader(f, delimiter=','):
            # Add node starting point
            if int(row[1]) not in graph.keys():
                graph[int(row[1])] = {}

            # Add node endpoints
            if int(row[2]) not in graph.keys():
                graph[int(row[2])] = {}
            # Add an endpoint to the start node and define the distance between them
            graph[int(row[1])][int(row[2])] = float(row[3])
            # Can't get from the end to some starting point
            if int(row[1]) not in graph[int(row[2])].keys():
                # inf infinity, unreachable between nodes
                graph[int(row[2])][int(row[1])] = math.inf
            # Can get from the end to some starting point
            else:
                graph[int(row[2])][int(row[1])] = float(row[2])
        print(graph)
    return graph


def datetimeInput():
    """Enter the time to perform
    Returns:
        int, int: the week and hour entered
    """
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input(
            "Please enter the date",
            datetime.date(2022, 10, 24))
    with col2:
        time = st.time_input('Please enter the time', datetime.time(0, 0))

    weekday = date.isoweekday()
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


def get_pos(lat, long):
    """get the latitude and longitude of the point

    Args:
        lat (float): latitude of the point
        long (float): longitude of the point

    Returns:
        float, float: latitude and longitude of the point
    """
    return lat, long


def reset_start_end_point():
    """reset the values of the latitude and longitude of the start and end points
    """
    # initialise point of start and end points
    st.session_state.start_long = 0
    st.session_state.start_lat = 0
    st.session_state.end_long = 0
    st.session_state.end_lat = 0


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


def startEndPointInput(fileLoc):
    """select the starting and ending points

    Args:
        fileLoc (str): Path to the file that will be used

    Returns:
        float, float, float, float, int, int:  The first four are the latitude and longitude of the start and end points, 
        and the last two are the cluster numbers of the start and end points
    """
    # initialise path start and end points
    if 'start_long' not in st.session_state:
        reset_start_end_point()
    # initialise the map
    m = folium.Map(location=[39.9632245, 116.280983], zoom_start=11,
                   tiles='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunityENG/MapServer/tile/{z}/{y}/{x}',
                   attr='default')
    # show the longitude and latitude of each clikc
    m.add_child(folium.LatLngPopup())
    # show the map
    map = st_folium(m, height=350, width=700)

    # Assign values to start and end points
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

    # button of reset the values of the start and end points
    clear_start_point = st.button(
        "Reset the start point and end point", key="bt_reset_points")
    # reset the values of the start and end points
    if clear_start_point:
        reset_start_end_point()
    # show the informations of the latitude and longitude of the point
    col1, col2 = st.columns(2)
    with col1:
        showPointInfo(st.session_state.start_lat,
                      st.session_state.start_long, 'start point')
    with col2:
        showPointInfo(st.session_state.end_lat,
                      st.session_state.end_long, 'end point')

    if st.session_state.start_lat != 0 and st.session_state.end_lat != 0:
        fromNode = searchPoint(
            st.session_state.start_long, st.session_state.start_lat, fileLoc, START_POINT)
        toNode = searchPoint(st.session_state.end_long,
                             st.session_state.end_lat, fileLoc, END_POINT)

        return st.session_state.start_long, st.session_state.start_lat, st.session_state.end_long, st.session_state.end_lat, fromNode, toNode

    # Do not start the algorithm until the button to start searching is pressed
    return 0, 0, 0, 0, 0, 0


def initialisedistanceance(graph, fromNode):
    """initiliaze distance
    Args:
        graph (dict): 
        fromNode (int): the id of the start node
    Returns:
        float: the distance initialized
    """
    distance = {fromNode: 0}
    for node in graph:
        if node != fromNode:
            distance[node] = math.inf
    return distance


def Dijkstra(graph, fromNode):
    """Shortest Circuit Sutra Algorithm

    Args:
        graph (dict): the graph
        fromNode (int): the id of the node to start

    Returns:
        list: all of the nodes passed
    """
    queue = []
    heappush(queue, (0, fromNode))
    # already seen points
    seen = set()
    seen.add(fromNode)
    # nodes that need to be warped
    parent = {fromNode: None}
    # distance initialized
    distance = initialisedistanceance(graph, fromNode)

    while len(queue) > 0:
        pair = heappop(queue)
        TempoDistance, node = pair[0], pair[1]
        seen.add(node)
        nodes = graph[node].keys()
        for i in nodes:
            if i not in seen:
                if TempoDistance + graph[node][i] < distance[i]:
                    heappush(queue, (TempoDistance + graph[node][i], i))
                    parent[i] = node
                    distance[i] = TempoDistance + graph[node][i]
    return parent


def getPointPassed(toNode, parent_dij, file):
    """get all the point passed

    Args:
        toNode (int): le point to 
        parent (dict): all the point that can be passed

    Returns:
        list: all the point passed
    """
    ployList = []   # Record the latitude and longitude points passed from the starting point to the end point in this way
    count = 0       # Record the number of geometries passing through the road

    try:
        while parent_dij[toNode] is not None:
            fromNode = parent_dij[toNode]

            with open(file, 'r') as f:
                next(f)
                for row in csv.reader(f, delimiter=','):
                    if str(row[1]) == str(fromNode) and str(row[2]) == str(toNode):
                        count += 1
                        numberPoints = row[6]
                        geo = str(row[5]).split(';')
                        geo.reverse()
                        for i in geo:
                            lonTmp = float(str(i).split(':')[0])
                            latTmp = float(str(i).split(':')[1])
                            ployList.append([latTmp, lonTmp, numberPoints])
                toNode = fromNode
    except TypeError:
        st.write('No cluster found')

    st.write("Number of cluster：" + str(count))
    if count == 0:
        st.write("No reachable path found")
        exit(0)

    return ployList


def calc_distance(p1, p2):
    """calculate the distance between two nodes

    Args:
        p1 ((float,float)): the coordinates of first node
        p1 ((float,float)): the coordinates of second node

    Returns:
        float: the distance between two nodes 
    """
    lat1, long1 = p1
    lat2, long2 = p2
    theta = long1 - long2
    dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.cos(math.radians(theta))
    if dist - 1 > 0:
        dist = 1
    elif dist + 1 < 0:
        dist = -1
    dist = math.acos(dist)
    dist = math.degrees(dist)
    miles = dist * 60 * 1.1515 * 1.609344
    return miles


def calcul_total_distance(ployList):
    """calculate the total distance to pass all the points

    Args:
        ployList (list): the list of all the points

    Returns:
        float: the total distance to pass all the points
    """
    distance_cumul = 0

    for index in range(0, len(ployList)):
        if(index != len(ployList)-1):
            lat1 = ployList[index][0]
            long1 = ployList[index][1]
            p1 = (lat1, long1)
            lat2 = ployList[index+1][0]
            long2 = ployList[index+1][1]
            p2 = (lat2, long2)
            distance_cumul = distance_cumul + calc_distance(p1, p2)
    return distance_cumul


def congestion_color(number_car):
    """determine congestion based on the number of vehicles

    Args:
        number_car (int): number of vehicles

    Returns:
        str: color of the line on the map
    """
    if number_car < 5:
        return 'green'
    elif number_car < 10:
        return 'yellow'
    else:
        return 'red'


def calcul_price_taxi(taxi_distance):
    """Calculate the cost of a cab ride

    Args:
        taxi_distance (float): kilometers traveled by cabs

    Returns:
        int: price of cab ride
    """
    BASE_KILOMETER = 3  # kilometers for base price
    BASE_PRICE = 10  # base price of taxi in Beijing in 2008
    PRICE_PER_KILOMETER = 2  # Price over base km

    if taxi_distance <= BASE_KILOMETER:
        return BASE_PRICE
    else:
        return BASE_PRICE + PRICE_PER_KILOMETER * math.ceil(taxi_distance-BASE_KILOMETER)


def showPath(ployList, latFromT, longFromT, latToT, longToT):
    """show the path passed

    Args:
        ployList (list): the list where we can find all the point passed
        latFromT (float): the latitude of the point to start
        longFromT (float): the longtitude of the point to start
        latToT (float): the latitude of the point to end
        longToT (float): the longtitude of the point to end
    """
    # initialize the map
    mmap = folium.Map(location=[39.9632245, 116.280983], zoom_start=11,
                      tiles='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunityENG/MapServer/tile/{z}/{y}/{x}',
                      attr='default', key='result')
    # initialize the start and end walking lines
    start_line = [[latFromT, longFromT], [
        ployList[len(ployList)-1][0], ployList[len(ployList)-1][1]]]
    end_line = [[latToT, longToT], [ployList[0][0], ployList[0][1]]]
    # the distance and time of taxi
    distance_taxi = round(calcul_total_distance(ployList), 3)
    average_time_taxi = round((distance_taxi/23)*60, 1)
    # the distance and time of walking
    distance_start_walk = round(calcul_total_distance(start_line), 3)
    average_time_taxi_start_walk = round((distance_start_walk/7.5)*60, 1)
    distance_end_walk = round(calcul_total_distance(end_line), 3)
    average_time_taxi_end_walk = round((distance_end_walk/7.5)*60, 1)
    # print the walking line
    folium.PolyLine(start_line, color='blue',
                    tooltip='walking path ' + str(distance_start_walk) + ' km for ' + str(average_time_taxi_start_walk)+' min').add_to(mmap)
    folium.PolyLine(end_line, color='blue',
                    tooltip='walking path ' + str(distance_end_walk) + ' km for ' + str(average_time_taxi_end_walk)+' min').add_to(mmap)
    # print the taxi line
    for index_point in range(0, len(ployList)-2):
        point_start = ployList[index_point]
        point_end = ployList[index_point+1]
        number_car = int(point_start[2]) + int(point_end[2])
        line = [[float(point_start[0]), float(point_start[1])]] + \
            [[float(point_end[0]), float(point_end[1])]]
        folium.PolyLine(line, color=congestion_color(number_car)).add_to(mmap)
    # mark the start and end point
    folium.Marker([latFromT, longFromT],  tooltip='Start point',
                  icon=folium.Icon(color='blue')).add_to(mmap)
    folium.Marker([latToT, longToT], tooltip='End point',
                  icon=folium.Icon(color='red')).add_to(mmap)
    mmap.add_child(folium.LatLngPopup())
    # show trip details
    price_taxi = calcul_price_taxi(distance_taxi)
    st.write('For this trip you can expect to pay '+str(price_taxi) +
             " ¥ and it will take you", round(average_time_taxi_start_walk+average_time_taxi+average_time_taxi_end_walk, 2), "min")
    st.write('For this trip, you will need to walk for ' + str(distance_start_walk) +
             ' km for ' + str(average_time_taxi_start_walk)+' min')
    st.write('And then, you will need to take the taxi for ' + str(distance_taxi) +
             ' km for ' + str(average_time_taxi)+' min')
    st.write('And the end, you will need to walk for ' + str(distance_end_walk) +
             ' km for ' + str(average_time_taxi_end_walk)+' min')
    folium_static(mmap)


def main():
    """the main part of the page
    """
    # initialise longFromT
    longFromT = 0
    # input of the datetime
    week, hour = datetimeInput()
    # get the path of the map file
    file = getFileLoc(week, hour)
    # input of the start and end point
    longFromT, latFromT, longToT, latToT, fromNode, toNode = startEndPointInput(
        file)
    # initialize graph
    graph = initGraph(file)

    if longFromT != 0:
        parent = Dijkstra(graph, fromNode)
        # get all the points passed
        ployList = getPointPassed(toNode, parent, file)
        # show the path at the map
        showPath(ployList, latFromT, longFromT, latToT, longToT)
