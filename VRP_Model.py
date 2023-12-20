import math

class Model:

# instance variables
    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.matrix = []
        self.capacity = -1

    def BuildModel(self):
        """ Reads the data of the Instance and builds the VRP model"""

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
    def __init__(self, idd, xx, yy, dem):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.demand = dem
        self.isRouted = False

class Route:
    def __init__(self, dp, cap):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.sequenceOfNodes.append(dp)
        self.cost = 0
        self.capacity = cap
        self.load = 0