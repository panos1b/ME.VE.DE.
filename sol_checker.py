import random
import math

class Node:
    """
    Represents a node in a vehicle routing problem.

    Attributes:
        ID (int): The unique identifier for the node.
        x (float): The x-coordinate of the node's location.
        y (float): The y-coordinate of the node's location.
        isRouted (bool): Indicates whether the node is part of a route.
        demand (float): The demand associated with the node.
    """
    def __init__(self, idd, xx, yy, dem=0, st=0):
        """
        Initializes a Node object.
        """
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
    """
    Calculates the Euclidean distance between two nodes.

    Parameters:
        from_node (Node): The starting node.
        to_node (Node): The destination node.
                        The node after "from_node" node.

    Returns:
        float: The Euclidean distance between the two nodes.
    """
    dx = from_node.x - to_node.x
    dy = from_node.y - to_node.y
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist


def calculate_route_details(nodes_sequence, empty_vehicle_weight):
    """
    Calculates the total traveled distance multiplied by the total load and total demand of a route.

    Parameters:
        nodes_sequence (List[Node]): The sequence of nodes in the route.
        empty_vehicle_weight (float): The weight of an empty vehicle.

    Returns:
        Tuple[float, float]: A tuple containing the total traveled distance multiplied by the total load and total demand of the route.
    """
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
    """
    Verify the correctness  of a given solution to the VRP instance.

    This function reads the solution.txt file, reads the second line to get the reported objective and
    reads the fourth line to get the number of vehicles used, track how many times each customer (node) is visited in the solution. Also, processes the routes of each vehicle,
    and checks against the constraints and objectives to ensure the validity of the solution.

    Parameters:
    -----------
    file_name : str
        The path to the solution file containing the reported objective and vehicle routes.
    all_nodes : list
        A list containing all Node objects representing customers in the VRP instance.
    capacity : float
        The maximum capacity of each vehicle in the VRP instance.
    empty_vehicle_weight : float
        The weight of an empty vehicle, used for calculating route details.

    Returns:
    --------
    None. Prints messages indicating the verification result or errors.

    """
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