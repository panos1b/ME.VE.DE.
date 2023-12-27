import random
import math

class Node:
    def __init__(self, idd, xx, yy, dem=0, st=0):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.isRouted = False
        self.demand = dem


def load_model(file_name):
    '''
    Loads a vehicle routing problem model from a file.

    :param file_name: The name of the file containing the problem instance.
    :return: A tuple containing a list of Node objects, capacity, and empty vehicle weight.
    '''
    # List to store all nodes in the problem instance
    all_nodes = []

    # Read all lines from the input file
    all_lines = list(open(file_name, "r"))

    # Separator used in the input file
    separator = ','

    # Counter to keep track of the current line being processed
    line_counter = 0

    # Extract capacity from the first line of the file
    ln = all_lines[line_counter]
    no_spaces = ln.split(sep=separator)
    capacity = int(no_spaces[1])

    # Move to the next line and extract empty vehicle weight
    line_counter += 1
    ln = all_lines[line_counter]
    no_spaces = ln.split(sep=separator)
    empty_vehicle_weight = int(no_spaces[1])

    # Move to the next line and extract the total number of customers
    line_counter += 1
    ln = all_lines[line_counter]
    no_spaces = ln.split(sep=separator)
    tot_customers = int(no_spaces[1])

    # Skip three lines to reach the line with depot coordinates
    line_counter += 3
    ln = all_lines[line_counter]

    # Extract depot coordinates and create a Node object for the depot
    no_spaces = ln.split(sep=separator)
    x = float(no_spaces[1])
    y = float(no_spaces[2])
    depot = Node(0, x, y)
    all_nodes.append(depot)

    # Loop through each customer and create Node objects for them
    for i in range(tot_customers):
        line_counter += 1
        ln = all_lines[line_counter]
        no_spaces = ln.split(sep=separator)
        idd = int(no_spaces[0])
        x = float(no_spaces[1])
        y = float(no_spaces[2])
        demand = float(no_spaces[3])
        customer = Node(idd, x, y, demand)
        all_nodes.append(customer)

    # Return the list of nodes, capacity, and empty vehicle weight
    return all_nodes, capacity, empty_vehicle_weight



def distance(from_node, to_node):
    dx = from_node.x - to_node.x
    dy = from_node.y - to_node.y
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist


def calculate_route_details(nodes_sequence, empty_vehicle_weight):
    tot_dem = sum(n.demand for n in nodes_sequence)
    tot_load = empty_vehicle_weight + tot_dem
    tn_km = 0
    for i in range(len(nodes_sequence) - 1):
        from_node = nodes_sequence[i]
        to_node = nodes_sequence[i+1]
        tn_km += distance(from_node, to_node) * tot_load
        tot_load -= to_node.demand
    return tn_km, tot_dem


def test_solution(file_name, all_nodes, capacity, empty_vehicle_weight):
    all_lines = list(open(file_name, "r"))
    line = all_lines[1]
    objective_reported = float(line.strip())
    objective_calculated = 0

    times_visited = {}
    for i in range(1, len(all_nodes)):
        times_visited[i] = 0

    line = all_lines[3]
    vehs_used = int(line.strip())

    separator = ','
    line_counter = 4
    for i in range(vehs_used):
        ln = all_lines[line_counter]
        ln = ln.strip()
        no_commas = ln.split(sep=separator)
        ids = [int(no_commas[i]) for i in range(len(no_commas))]
        nodes_sequence = [all_nodes[idd] for idd in ids]
        rt_tn_km, rt_load = calculate_route_details(nodes_sequence, empty_vehicle_weight)
        for nn in range(1,len(nodes_sequence)):
            n_in = nodes_sequence[nn].ID
            times_visited[n_in] = times_visited[n_in] + 1
        # check capacity constraints
        if rt_load > capacity:
            print('Capacity violation. Route', i, 'total load is', rt_load)
            return
        objective_calculated += rt_tn_km
        line_counter += 1
    # check solution objective
    if abs(objective_calculated - objective_reported) > 0.001:
        print('Cost Inconsistency. Cost Reported', objective_reported, '--- Cost Calculated', objective_calculated)
        return

    # Check number of times each customer is visited
    for t in times_visited:
        if times_visited[t] != 1:
            print('Error: customer', t, 'not present once in the solution')
            return

    # everything is ok
    print('Solution is ΟΚ. Total Cost:', objective_calculated)

all_nodes, capacity, empty_vehicle_weight = load_model('Instance.txt')
test_solution('Instance.txt', all_nodes, capacity, empty_vehicle_weight)