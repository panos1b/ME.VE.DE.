import math


def read_instance(path: str) -> tuple[dict[tuple[int, int], float], dict[int, float]]:
    """
    This method reads an instance file and  returns two dictionaries containing metrics for the nodes

    :param path: This parameters should contain the path for the instance txt file
    :return: The fist dictionairy connects two node ids to the distance between them. The second one connects
    a node id to the capacity of that node
    """
    with open(path) as fp:
        current_node = []
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
                    current_node.append(int(entry))
                except ValueError:
                    current_node.append(float(entry))
            nodes.append(current_node.copy())
            current_node.clear()

    demand_dictionary = {node_id: node[3] for node_id, node in enumerate(nodes)}
    # this dictionary will connect node ids with capacity

    distance_dictionary = {(i, j): math.dist([node_i[1], node_i[2]], [node_j[1], node_j[2]]) for i, node_i in
                           enumerate(nodes) for j, node_j in enumerate(nodes)}
    # this dictionary will connect tuples (x,y) to the distance of modes with id x and y

    return distance_dictionary, demand_dictionary


if __name__ == '__main__':
    distances, demands = read_instance('Instance.txt')