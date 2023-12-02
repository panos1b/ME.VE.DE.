import math


def read_instance(path: str) -> tuple[dict[tuple[int, int], float], dict[int, float]]:
    """
    This method reads an instance file and  returns two dictionaries containing metrics for the nodes

    :param path: This parameters should contain the path for the instance txt file
    :return: The fist dictionairy connects two node ids to the distance between them. The second one connects
    a node id to the capacity of that node
    """
    with open(path) as fp:
        currentnodeinfo = []
        nodes = []

        # ignore first values
        for line in fp:
            if line.strip() == "NODES INFO":  # We are done reading parameters moving on to nodes
                break
        #####################################################
        # Read more parameters if necessary
        #     else:
        #         key, value = line.split(",")
        #         match key:
        #             case "CAPACITY":
        #                 CAPACITY = value
        #             case "EMPTY_VEHICLE_WEIGHT":
        #                 EMPTY_VEHICLE_WEIGHT = value
        #             case "CUSTOMERS":
        #                 CUSTOMERS = value
        #####################################################
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
    return distance_dictionary, demand_dictionary


if __name__ == '__main__':
    distance_dictionary, demand_dictionary = read_instance('Instance.txt')
