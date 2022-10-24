import pandas as pd
import csv
from __future__ import division
from math import pi, sqrt, sin, cos
"""
    The aim is to change coordinates from World Geodetic System (WGS) to Mars Coordinate System (GCJ).
    We store latitude and longitude data of taxis in mMap.csv.
    Select from 1 to 1000 files.
"""

constA = 6378245.0
constB = 0.00669342162296594323

# World Geodetic System ==> Mars Geodetic System
def changeC(worldLat, worldLon):
    if outOfChina(worldLat, worldLon):
        marsLat = worldLat
        marsLon = worldLon
        return
    
    dLat = changeLat(worldLon - 105.0, worldLat - 35.0)
    dLon = changeLon(worldLon - 105.0, worldLat - 35.0)
    radLat = worldLat / 180.0 * pi
    magic = sin(radLat)
    magic = 1 - constB * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / ((constA * (1 - constB)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (constA / sqrtMagic * cos(radLat) * pi)
    marsLat = worldLat + dLat
    marsLon = worldLon + dLon
    return marsLon, marsLat


def outOfChina(lat, lon):
    if lon < 72.004 or lon > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


def changeLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret


def changeLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret


if __name__ == "__main__":
    f1 = open('csv/segment/weekday/04082324.csv', 'w')        # 'a+' : read and write, no deleting ; 'w' : write and delete
    timeA = '23:00:00'
    timeB = '24:00:00'
    # Tlat and Tlon are examples
    Tlat = 39.85155
    Tlon = 116.69169
    print(Tlat, Tlon)
    print(changeC(Tlat, Tlon))

    for aa in csv.reader(open('csv/path.csv')):     # path.csv = taxis data
        f = open(str(aa)[2:-2])     # Obtain path of taxi aa
        data = pd.read_csv(f, names=['ID', 'time', 'lat', 'lon'])
        # Drop duplicates.
        data = data.drop_duplicates(subset=['ID', 'time', 'lat', 'lon'])
        # Drop null values
        data = data.dropna(axis=0, how='any')
        # Order by ascending time
        data = data.set_index('time')
        # Obtain data by time periods
        timeDat1 = data['2008-02-04 ' + timeA:'2008-02-04 ' + timeB]
        timeDat2 = data['2008-02-05 ' + timeA:'2008-02-05 ' + timeB]
        timeDat3 = data['2008-02-06 ' + timeA:'2008-02-06 ' + timeB]
        timeDat4 = data['2008-02-07 ' + timeA:'2008-02-07 ' + timeB]
        timeDat5 = data['2008-02-08 ' + timeA:'2008-02-08 ' + timeB]
        # Goup in timeDat
        timeDat = timeDat1.append(timeDat2).append(timeDat3).append(timeDat4).append(timeDat5)
        print(timeDat)
        timeDat.to_csv('D:/data/tmp.csv')
        for row in csv.reader(open('D:/data/tmp.csv'), delimiter=','):
            if row[3] == 'lon':     # Jump until 'lon' is read
                continue
            # Out of Beijing
            if float(row[2]) < 115.0 or float(row[2]) > 118.0 or float(row[3]) < 39.0 or float(row[3]) > 42.0:
                continue
            # Conversion of longitude and latitude
            lat = str(changeC(float(row[3]), float(row[2]))[0])
            lon = str(changeC(float(row[3]), float(row[2]))[1])
            print(lat, lon)
            # Find points in starTrek
            if 116.152675 <= float(lat) <= 116.409291 and 39.885149 <= float(lon) <= 40.0413:
                print('Available points :' + row[1] + ',' + row[0] + ',' + lat + ',' + lon + '\r')
                f1.write(row[1] + ',' + row[0] + ',' + lat + ',' + lon + '\r')