import csv
import pandas as pd
import numpy as np


def box_creation(key_points, save_path):
    """ box creation : encapsulate correspondence and write a new road network algorithm
    args : key_points, save_path: path to the file that will be use        
    """

    database_test = key_points
    write_test = save_path

    data_map = 'csv/mMap.csv'

    # stock lat and long
    a = []

    with open(database_test, 'r') as f:

        reader = csv.reader(f)

        for row in reader:
            a.append([row[2], row[3]])

        print(a)

    write = []
    # Display the results to see how many data were matched and how many points were matched
    resultat = []

    with open(data_map, 'r') as f:
        next(f)
        reader = csv.reader(f)

        for row in reader:
            counter = 0
            geometry = row[5]
            geometry = geometry.split(";")

            for i in geometry:
                i = i.split(":")

                for number in a:

                    if float(number[0]) - 0.00015 <= float(i[0]) <= float(number[0]) + 0.00015 and \
                            float(number[1]) - 0.00015 <= float(i[1]) <= float(number[1]) + 0.00015:
                        counter += 1

            if counter != 0:
                resultat.append(counter)
                row[3] = float(row[3]) / float(counter + 1)

            write.append(row)

    print("Nombre de correspondances sur les données :" + str(resultat))
    print("Nombre total de données sur le match :", resultat.__len__())
    print("La quantité de données qui doit être écrite sur le nouveau réseau routier :", write.__len__())

    # 1. create file
    f = open(write_test, 'w', encoding='utf-8', newline='')

    # 2. construct to write
    csv_writer = csv.writer(f)

    # 3. contruct header of the file
    csv_writer.writerow(["LinkID", "FromNode", "ToNode",
                        "Length", "RoadClass", "Geometry"])

    for row in write:
        csv_writer.writerow(row)
        counter += 1
        print("Line numbers written in", format(counter))
    f.close()

    return str(key_points+" finished！")
