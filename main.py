import math
import random

random.seed(3)
VEHICLE_NUMBER = 14
CAPACITY = 200
CUSTOMERS = 100


def total_distance(routes, distance_dictionary):
    total_distance = 0
    for route in routes:
        route_distance = 0
        for i in range(len(route) - 1):
            node1 = route[i]
            node2 = route[i + 1]
            route_distance += distance_dictionary[(node1, node2)]
        total_distance += route_distance
    return total_distance


def optimize_routes(routes, distance_dictionary, num_iterations):
    best_routes = routes.copy()
    best_distance = total_distance(best_routes, distance_dictionary)
    for _ in range(num_iterations):
        # Randomly select a route
        route_index = random.randint(0, len(routes) - 1)
        route = routes[route_index]
        # Randomly select two non-depot nodes in the route
        nodes_to_swap = random.sample(route[1:-1], 2)
        # Swap the selected nodes in the route
        new_route = route.copy()
        node1_index = new_route.index(nodes_to_swap[0])
        node2_index = new_route.index(nodes_to_swap[1])
        new_route[node1_index], new_route[node2_index] = new_route[node2_index], new_route[node1_index]
        new_routes = routes.copy()
        new_routes[route_index] = new_route
        # Calculate the total distance of the new routes
        new_distance = total_distance(new_routes, distance_dictionary)
        # Update the best routes if the new routes have a shorter distance
        if new_distance < best_distance:
            best_routes = new_routes
            best_distance = new_distance
    return best_routes


def greedy_vrp_with_optim(distance_dictionary, demand_dictionary, num_vehicles, vehicle_capacity, random_iterations):
    # Initialize variables
    routes = [[0] for _ in range(num_vehicles)]
    vehicle_load = [0 for _ in range(num_vehicles)]
    unvisited_nodes = set(range(1, 101))
    total_demand = sum(demand_dictionary.values())

    # Iterate until all demand is covered
    while total_demand > 0:
        for i in range(num_vehicles):
            if total_demand <= 0:
                break
            # Find the closest unvisited node that the vehicle can serve
            min_distance = float('inf')
            closest_node = None
            for node in unvisited_nodes:
                if demand_dictionary[node] + vehicle_load[i] <= vehicle_capacity:
                    if distance_dictionary[(routes[i][-1], node)] < min_distance:
                        min_distance = distance_dictionary[(routes[i][-1], node)]
                        closest_node = node

            # If a closest node was found, add it to the route and update vehicle load and cost
            if closest_node:
                routes[i].append(closest_node)
                vehicle_load[i] += demand_dictionary[closest_node]
                unvisited_nodes.remove(closest_node)
                total_demand -= demand_dictionary[closest_node]

    # We try to optimize the routes using random numbers
    routes = optimize_routes(routes, distance_dictionary, random_iterations)
    with open("solution.txt", "w") as f:
        f.write("Cost:\n")
        f.write(str(5.558064 * total_distance(routes, distance_dictionary)) + "\n")
        f.write("Routes:\n")
        f.write(str(len(routes)) + "\n")
        for i in range(num_vehicles):
            if len(routes[i]) > 1:
                f.write(','.join(str(node) for node in routes[i]) + "\n")

with open('instance.txt') as fp:
    contents = fp.read()
    i = 0
    currentnodeinfo = []
    nodes = []
    for entry in contents.replace('\n', ','). \
            split(','):  # replace new lines with commas and then split according to commas#
        i += 1
        if i > 12:  # ignore first 12 values they are headers#
            try:
                currentnodeinfo.append(int(entry))
            except ValueError:
                pass
            if (i - 12) % 5 == 0:  # Every 5 values a new node is read#
                nodes.append(currentnodeinfo.copy())
                currentnodeinfo.clear()

    distance_dictionary = {}  # this dictionary will connect node ids with capacity#
    demand_dictionary = {}  # this dictionary will connect tuples (x,y) to the distance of modes with id x and y#
for i in range(len(nodes)):
    demand_dictionary[i] = nodes[i][3]
    for j in range(len(nodes)):
        Ix = nodes[i][1]
        Iy = nodes[i][2]
        Jx = nodes[j][1]
        Jy = nodes[j][2]
        distance = math.dist([Ix, Iy], [Jx, Jy])
        distance_dictionary[(i, j)] = distance

greedy_vrp_with_optim(distance_dictionary, demand_dictionary, 14, 200, 1000000)
