import math

class Model:
"""
Represents a Vehicle Routing Problem (VRP) model.

Attributes:
allNodes (List[Node]): A list containing all nodes, including customers and the warehouse.
customers (List[Node]): A list containing only customer nodes.
matrix (List[List[float]]): A matrix representing the distance between nodes.
capacity (int): The capacity of the vehicles.
empty_vehicle_weight (int): The weight of an empty vehicle.
total_customers (int): The total number of customers.

Methods:
BuildModel(): Reads the data from 'Instance.txt' and builds the VRP model.
"""


# instance variables
    def __init__(self):
        """
        Initializes a Model object.
        """
        self.allNodes = []
        self.customers = []
        self.matrix = []
        self.capacity = -1

    def BuildModel(self):
        """
        Reads the data of the 'Instance.txt' and builds the VRP model
        """

        with open('Instance.txt', 'r') as file:
            for line in file:
                line = line.strip()  
                if line.startswith('CAPACITY'):
                    self.capacity = int(line.split(',')[1])
                elif line.startswith('EMPTY_VEHICLE_WEIGHT'):
                    self.empty_vehicle_weight = int(line.split(',')[1])
                elif line.startswith('CUSTOMERS'):
                    self.total_customers = int(line.split(',')[1])
                elif line.startswith('ID') or line.startswith('NODES INFO'):
                    continue
                else:
                    id, x, y, demand = line.split(',')
                    node = Node(int(id),int(x), int(y),float(demand))
                    self.allNodes.append(node)
                    if id!=0:
                        self.customers.append(node)                                  
        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]
        for i in range(0, len(self.allNodes)): #calculate distance between nodes
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist
      # for i in range(0, len(self.allNodes)):
       #    self.matrix[i][0] = 0  # make move from customer to depot costless


class Node:
    """
    Represents a customer node in the network.

    Attributes:
    -----------
    x : int
        The x-coordinate of the node in the network.
    y : int
        The y-coordinate of the node in the network.
    ID : int
        The unique identifier for the node.
    demand : float
        The demand associated with the customer node.
    isRouted : bool
        A flag indicating if the node has been routed in a solution or not.

    Methods:
    --------
    __init__(idd, xx, yy, dem):
        Initializes a Node object with given attributes.

    """

    def __init__(self, idd, xx, yy, dem):
        """
        Initialize a Node object.

        Parameters:
        -----------
        idd : int
            Unique identifier for the node.
        xx : int
            x-coordinate of the node.
        yy : int
            y-coordinate of the node.
        dem : float
            Demand associated with the node.

        """

        self.x = xx
        self.y = yy
        self.ID = idd
        self.demand = dem
        self.isRouted = False

class Route:
    def __init__(self, dp, cap):
        """
        Initializes a route with a starting depot and maximum capacity.

        Parameters:
        - depot (Node): The starting depot for the route.
        - capacity (float): The maximum capacity of the route.
        """
        # Initialize with the depot twice (start and end)
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.sequenceOfNodes.append(dp)
        self.cost = 0 # Initialize route cost to zero
        self.capacity = cap # Maximum capacity of the route
        self.load = 0 # Current load on the route
        self.length = 0  # Current length on the route

    def DemandAfterNode(self, start_index):
        """
        Takes a vrp route and calculates the demand from the node ID given till the end

        :param start_index: the starting index for the nodes (inclusive)
        :type start_index:int
        :return: The demand from the start_index node till the end
        """

        return sum(node.demand for node in self.sequenceOfNodes[start_index :])


    def DistanceBeforeNode(self, end_index, solver_instance):
        """
        Takes a vrp route and calculates the distance from the start till the node ID given

        :param end_index: The index to end at
        :param solver_instance: The instance of the solution (hint: use self)
        :return: The total distance before the node
        """

        return sum(
            solver_instance.distanceMatrix[self.sequenceOfNodes[index].ID][self.sequenceOfNodes[index + 1].ID]
            for index in range(end_index - 1)
        )
