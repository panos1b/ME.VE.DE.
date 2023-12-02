import math
import random

with open('Instance.txt') as fp:
    currentnodeinfo = []
    nodes = []

    # ignore first values
    for line in fp:
        if line.strip() == "NODES INFO":  # We are done reading parameters moving on to nodes
            break
        else:
            key, value = line.split(",")
            match key:
                case "CAPACITY":
                    CAPACITY = value
                case "EMPTY_VEHICLE_WEIGHT":
                    EMPTY_VEHICLE_WEIGHT = value
                case "CUSTOMERS":
                    CUSTOMERS = value
    fp.__next__()  # The headers are ignored!
    for line in fp:
        for entry in line.split(","):  # split values according to commas
            try:
                currentnodeinfo.append(int(entry))
            except ValueError:
                currentnodeinfo.append(float(entry))
        nodes.append(currentnodeinfo.copy())
        currentnodeinfo.clear()

distance_dictionary = dict()  # this dictionary will connect node ids with capacity#
demand_dictionary = dict()  # this dictionary will connect tuples (x,y) to the distance of modes with id x and y#
for i in range(len(nodes)):
    demand_dictionary[i] = nodes[i][3]
    for j in range(len(nodes)):
        Ix = nodes[i][1]
        Iy = nodes[i][2]
        Jx = nodes[j][1]
        Jy = nodes[j][2]
        distance = math.dist([Ix, Iy], [Jx, Jy])
        distance_dictionary[(i, j)] = distance

print(distance_dictionary)
print(demand_dictionary)
