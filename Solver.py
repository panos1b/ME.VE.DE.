import random

from VRP_Model import *


class Solution:
    """
    Represents a solution to the VRP instance.

    Attributes:
    -----------
    cost : float
        The total cost of the solution.
    routes : list
        A list containing the routes of vehicles in the solution.

    Methods:
    --------
    __init__():
        Initializes a Solution object with default attributes (cost = 0.0 and routes= []).
    """

    def __init__(self):
        self.cost = 0.0
        self.routes = []

class Saving:
    def __init__(self, n1, n2, sav):
        self.n1 = n1
        self.n2 = n2
        self.score = sav


class RelocationMove(object):
    """
    Represents a relocation move between nodes (customers) in a VRP solution.

    Attributes:
    -----------
    originRoutePosition : int or None
        Position of the origin route in the solution's routes list.
    targetRoutePosition : int or None
        Position of the target route in the solution's routes list.
    originNodePosition : int or None
        Position of the origin node within its route.
    targetNodePosition : int or None
        Position of the target node within its route.
    costChangeOriginRt : float or None
        Change in cost if the origin node is relocated.
    costChangeTargetRt : float or None
        Change in cost if the target node is relocated.
    moveCost : float
        Cost of the relocation move.

    Methods:
    --------

    __init__():
        Initialize a RelocationMove object with default attributes.

    Initialize():
        Reset all attributes to their initial state. The moveCost attribute is initialized with a high non-logical value (10^9) to signify that it needs to be recalculated during the relocation process.

    """

    def __init__(self):
        """
        Initialize a RelocationMove object with default attributes.
        """
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None
        self.moveCost_penalized = None  # gls

    def Initialize(self):
        """
        Reset all attributes of the RelocationMove object to their initial state.
        """
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9
        self.moveCost_penalized = 10 ** 9  # gls


class SwapMove(object):
    """
    Represents a potential swap move in the VRP.

    Attributes:
        positionOfFirstRoute (int): Index of the first route involved in the swap.
        positionOfSecondRoute (int): Index of the second route involved in the swap.
        positionOfFirstNode (int): Index of the node in the first route to be swapped.
        positionOfSecondNode (int): Index of the node in the second route to be swapped.
        costChangeFirstRt (float): Cost change associated with the swap in the first route.
        costChangeSecondRt (float): Cost change associated with the swap in the second route.
        moveCost (float): Total cost change resulting from the swap operation.
    """

    def __init__(self):
        """
        Initializes a SwapMove object.

        The moveCost attribute is set to a large value (10^9) to ensure it is initially higher than any potential cost change.
        """
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None
        self.moveCost_penalized = None  # gls

    def Initialize(self):
        """
        Resets the attributes of the SwapMove object to their initial values.

        The moveCost attribute is set back to a large value to allow easy replacement with a better cost during calculations.
        """
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9
        self.moveCost_penalized = 10 ** 9  # gls


class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9


class CustomerInsertionAllPositions(object):
    """
    Represents a potential customer insertion into all possible positions along a route.

    Attributes:
        customer (Node): The customer node to be inserted.
        route (Route): The route where the customer is to be inserted.
        insertionPosition (Position): The position at which the customer is to be inserted in the route.
        cost (float): The cost associated with the insertion position,
                      Initialized to a large value to allow easy replacement with a better cost.
    """

    def __init__(self):
        """
        Initializes a CustomerInsertionAllPositions object.

        The cost attribute is set to a large value (10^9) to ensure it is initially higher than any potential insertion cost.
        """
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.cost = 10 ** 9


class TwoOptMove(object):
    """
    Represents a potential 2-opt move in the VRP.

    Attributes:
        positionOfFirstRoute (int): Index of the first route involved in the 2-opt move.
        positionOfSecondRoute (int): Index of the second route involved in the 2-opt move.
        positionOfFirstNode (int): Index of the first node to be swapped.
        positionOfSecondNode (int): Index of the second node to be swapped.
        moveCost (float): Cost of the relocation move.

    Methods:
        Initialize(): Resets the attributes to their default values, setting moveCost to a large value(10^9).
    """

    def __init__(self):
        """
        Initializes a TwoOptMove object with default attributes.
        """
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None
        self.moveCost_penalized = None  # gls

    def Initialize(self):
        """
        Resets the attributes to their initial values, setting moveCost to a large value(10^9).
        """
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9
        self.moveCost_penalized = 10 ** 9  # gls


class Solver:
    """
    A class that provides methods to solve the Vehicle Routing Problem (VRP).

    Attributes:
    -----------
    allNodes : list
        List containing all nodes in the VRP, including the depot and customers.
    customers : list
        List containing only the customer nodes.
    depot : Node
        The depot node where all routes begin and end.
    distanceMatrix : list of lists
        A 2D list representing the distance between each pair of nodes.
    capacity : float
        The capacity of the vehicles in the VRP.
    sol : Solution
        An instance of the Solution class representing the current solution.
    bestSolution : Solution
        An instance of the Solution class representing the best solution found so far.

    Methods:
    --------
    __init__(m):
        Initialize the Solver with the given model 'm'.
        - m: An instance of the Model class containing problem data.
    solve():
        Main method to solve the VRP.
         Executes a sequence of methods to construct and optimize the solution.


    SetRoutedFlagToFalseForAllCustomers():
        Set the 'isRouted' flag to False for all customer nodes.
        Ensures that all customers are unrouted before constructing a new solution.

    ApplyNearestNeighborMethod():
        Construct initial routes using the Nearest Neighbor method.
        Continues to assign customers to routes until all are assigned or capacity constraints are violated.
        Uses the distance matrix to determine the nearest customers every time.

    LocalSearch(operator):
        Apply local search techniques to further optimize the solution.
        - operator: An integer representing the type of local search move (0: Relocation, 1: Swap, 2: TwoOpt).
        Implements the specified local search operator to explore neighboring solutions.

    cloneRoute(rt):
         Clone a given route 'rt' to create an identical route object.
        - rt: The route to be cloned.
        Returns the cloned route.

    cloneSolution(sol):
         Clone a given solution 'sol' to create an identical solution object.
        - sol: The solution to be cloned.
        Returns the cloned solution.

    FindBestRelocationMove(rm):
        Find the best relocation move to optimize the solution.
        Evaluates all possible relocations and identifies the move with the greatest cost improvement.
        - rm: An instance of the RelocationMove class to store the best move details.
        Returns the identified best relocation move.

    InitializeOperators(rm, sm, top):
         Initializes the move operators for local search.
         - rm: The relocation move object to be initialized.
        - sm: The swap move object to be initialized.
        - top: The 2-opt move object to be initialized.

    FindBestTwoOptMove(top):
        Finds the best 2-opt move among all possible combinations of routes and nodes.
        - top: The TwoOptMove object to store the best move information.

    CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
        Checks whether the capacity of the given routes is violated after a potential 2-opt move.
        - rt1: Index of the first route involved in the swap.
        - nodeInd1: Index of the node in `rt1` before which the segment load is calculated.
        - rt2: Index of the second route involved in the swap.
        - nodeInd2: Index of the node in `rt2` before which the segment load is calculated.
        Returns True if the capacity is violated. Otherwise, it return false.

    StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
        Stores the information of the best 2-opt move in the provided TwoOptMove object.
        - rtInd1: Index of the first route in the solution.
        - rtInd2: Index of the second route in the solution.
        - nodeInd1: Index of the first node in the first route.
        - nodeInd2: Index of the second node in the second route.
        - moveCost: The cost associated with the 2-opt move.
        - top: TwoOptMove object to be updated with the best move information.

    ApplyTwoOptMove(top):
        Applies the best 2-opt move to the solution based on the information provided in the TwoOptMove object.
        - top: TwoOptMove object which contains the information about the best 2-opt move.

    UpdateRouteCostAndLoad(rt: Route):
        Updates the cost and load of a given route.
        - rt: The route whose cost and load need to be updated.

    IdentifyMinimumCostInsertion(best_insertion):
        Identifies the minimum cost insertion for a customer into existing routes.
        - best_insertion: An object to store information about the best insertion.

    ApplyCustomerInsertionAllPositions(insertion):
        Applies the customer insertion at all possible positions within a route.
        - insertion: An object containing information about the customer insertion.
    """

    def __init__(self, m):
        """
        Initialize the Solver with the given model 'm'.
        - m: An instance of the Model class containing problem data.
        """
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None
        self.searchTrajectory = []
        self.minTabuTenure = 15
        self.maxTabuTenure = 150

        # gls
        rows = len(self.allNodes)
        self.distance_matrix_penalized = [[self.distanceMatrix[i][j] for j in range(rows)] for i in range(rows)]
        self.times_penalized = [[0 for j in range(rows)] for i in range(rows)]
        self.penalized_n1_ID = -1
        self.penalized_n2_ID = -1

    def solve(self):
        """
        Main method to solve the VRP.
        Executes a sequence of methods to construct and optimize the solution.

        Returns:
        --------
        Solution
            The optimized solution for the VRP.
        """
        self.SetRoutedFlagToFalseForAllCustomers()

        print("Applying Nearest Neighbour method")
        self.ApplyNearestNeighborMethod()

        self.bestSolution = self.cloneSolution(self.sol)

        print("Applying GLS")
        self.GLS()

        print("Applying ClownMove (seed: 5, factor: 1.01)")
        self.ClownMove(5, 1.01)
        print("Applying ClownMove (seed: 4, factor: 1.01)")
        self.ClownMove(4, 1.01)
        print("Applying ClownMove (seed: 3, factor: 1)")
        self.ClownMove(3)
        print("Applying ClownMove (seed: 2, factor: 1.01)")
        self.ClownMove(2, 1.01)
        print("Applying ClownMove (seed: 1, factor: 1.01)")
        self.ClownMove(1, 1.01)

        print("Applying threeOPT")
        self.threeOPT(5)

        print("Applying Route Reversal")
        self.reverseRoutes()

        print("Applying Random Route Part Reversal (seed: 5)")
        self.randomlyPartlyReverseRoutes(5)

        self.clearCost()

        print("Applying Tabu")
        self.Tabu()


        print("Applying ClownMove (seed: 5, factor: 1.01)")
        self.ClownMove(5, 1.01)

        print("Applying ClownMove (seed: 4, factor: 1.01)")
        self.ClownMove(4, 1.01)

        print("Applying ClownMove (seed: 3, factor: 1.01)")
        self.ClownMove(3, 1.01)

        print("Applying ClownMove (seed: 2, factor: 1.01)")
        self.ClownMove(2, 1.01)

        print("Applying Random Route Part Reversal (seed: 1)")
        self.randomlyPartlyReverseRoutes(1)

        print("Applying Tabu")
        self.Tabu()

        print("Applying Random Route Part Reversal (seed: 1)")
        self.randomlyPartlyReverseRoutes(1)

        print("Applying Tabu")
        self.Tabu()
        return self.sol

    def clearCost(self):
        self.sol.cost = 0
        for route in self.sol.routes:
            (route_tn_km, route_dem) = route.calculate_route_details(self)
            self.sol.cost += route_tn_km
            route.cost = route_tn_km

    def SetRoutedFlagToFalseForAllCustomers(self):
        """
        Set the 'isRouted' flag to False for all customer nodes.
        Ensures that all customers are unrouted before constructing a new solution.
        """
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False

    def ApplyNearestNeighborMethod(self):
        """
        Construct initial routes using the Nearest Neighbor method.
        Continues to assign customers to routes until all are assigned or capacity constraints are violated.
        Uses the distance matrix to determine the nearest customers every time.
        """
        modelIsFeasible = True
        self.sol = Solution()
        insertions = 0

        while (insertions < len(self.customers)):
            bestInsertion = CustomerInsertion()
            lastOpenRoute: Route = self.GetLastOpenRoute()

            if lastOpenRoute is not None:
                self.IdentifyBestInsertion(bestInsertion, lastOpenRoute)

            if (bestInsertion.customer is not None):
                self.ApplyCustomerInsertion(bestInsertion)
                insertions += 1
            else:
                # If there is an empty available route
                if lastOpenRoute is not None and len(lastOpenRoute.sequenceOfNodes) == 2:
                    modelIsFeasible = False
                    break
                else:
                    rt = Route(self.depot, self.capacity)
                    self.sol.routes.append(rt)

    def GLS(self):
        random.seed(1)
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()

        while terminationCondition is False:
            operator = random.randint(0, 2)
            self.InitializeOperators(rm, sm, top)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMoveForGLS(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost_penalized < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        self.penalize_arcsForGLS()
                        localSearchIterator = localSearchIterator - 1
            # Swaps
            elif operator == 1:
                self.FindBestSwapMoveForGLS(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost_penalized < 0:
                        self.ApplySwapMove(sm)
                    else:
                        self.penalize_arcsForGLS()
                        localSearchIterator = localSearchIterator - 1
            elif operator == 2:
                self.FindBestTwoOptMoveForGLS(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost_penalized < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        self.penalize_arcsForGLS()
                        localSearchIterator = localSearchIterator - 1

            #     self.TestSolution()

            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1
            if localSearchIterator == 23:
                terminationCondition = True

        self.sol = self.bestSolution

    def threeOPT(self, seed: int, iterations: int = 99999) -> None:
        """
        Apply the 3-opt optimization heuristic to improve the solution.

        :param seed: Seed for the random number generator to ensure reproducibility.
        :type seed: int
        :param iterations: Number of iterations for the 3-opt optimization (default is 99999).
        :type iterations: int
        """

        random.seed(seed)
        for _ in range(iterations):
            route_position: int = random.randint(0, len(self.sol.routes) - 1)
            route: Route = self.sol.routes[route_position]
            for _ in range(random.randint(20, 30)):
                try:
                    node_start_position = random.randint(1, len(route.sequenceOfNodes) - 4)
                except Exception:
                    continue
                node_1 = route.sequenceOfNodes[node_start_position]
                node_2 = route.sequenceOfNodes[node_start_position + 1]
                node_3 = route.sequenceOfNodes[node_start_position + 2]
                copy_of_route = self.cloneRoute(route)
                nodes = [node_1, node_2, node_3]
                for random_node in random.sample(nodes, 3):
                    copy_of_route.sequenceOfNodes[node_start_position] = random_node
                    node_start_position += 1
                tn_km_new, _ = copy_of_route.calculate_route_details(self)
                tn_km_old, _ = route.calculate_route_details(self)
                if tn_km_new < tn_km_old * 0.98:
                    self.sol.routes[route_position]: Route = copy_of_route

    def ClownMove(self, seed: int, worse_solution_factor: float = 1.0, iterations: int = 999999):
        """
        Its name comes from clowns which usually juggle balls the same way we juggle the nodes!
        Randomly picks 2 pairs of nodes and swaps them

        :arg seed: Pick a number 1~5
        :arg iterations: How many times (999999) recommended
        :arg worse_solution_factor: Accept a worse solution (used for unblocking)
        :returns: None
        """

        def capacity_is_violated(rt1, rt2):
            """
            Checks whether the capacity of the given routes is violated
            """

            load_1 = 0
            for node in rt1.sequenceOfNodes:
                load_1 += node.demand

            if load_1 > rt1.capacity:
                return True

            load_2 = 0
            for node in rt2.sequenceOfNodes:
                load_2 += node.demand

            if load_2 > rt2.capacity:
                return True
            return False
        def flip_nodes():
            copy_of_route_1 = self.cloneRoute(route_1)
            copy_of_route_2 = self.cloneRoute(route_2)
            copy_of_route_1.sequenceOfNodes[node_position_1] = node_2_a
            copy_of_route_1.sequenceOfNodes[node_position_1+1] = node_2_b
            copy_of_route_2.sequenceOfNodes[node_position_2] = node_1_a
            copy_of_route_2.sequenceOfNodes[node_position_2+1] = node_1_b
            if capacity_is_violated(copy_of_route_1, copy_of_route_2) or \
                    len(copy_of_route_1.sequenceOfNodes) < 3 or len(copy_of_route_2.sequenceOfNodes) < 3:
                return
            else:

                tn_km_1_new, _ = copy_of_route_1.calculate_route_details(self)
                tn_km_1_old, _ = route_1.calculate_route_details(self)
                tn_km_2_new, _ = copy_of_route_2.calculate_route_details(self)
                tn_km_2_old, _ = route_2.calculate_route_details(self)
                if tn_km_1_new + tn_km_2_new < (tn_km_1_old + tn_km_2_old)*worse_solution_factor:
                    self.sol.routes[route_position_1]: Route = copy_of_route_1
                    self.sol.routes[route_position_2]: Route = copy_of_route_2

        random.seed(seed)
        iters = iterations
        for _ in range(iters):
            route_position_1 = random.randint(0, len(self.sol.routes) - 1)
            route_position_2 = random.randint(0, len(self.sol.routes) - 1)
            route_1: Route = self.sol.routes[route_position_1]
            route_2: Route = self.sol.routes[route_position_2]
            try:
                node_position_1 = random.randint(1, len(route_1.sequenceOfNodes)-3)
                node_position_2 = random.randint(1, len(route_2.sequenceOfNodes)-3)
            except Exception:
                continue
            node_1_a = route_1.sequenceOfNodes[node_position_1]
            node_1_b = route_1.sequenceOfNodes[node_position_1+1]
            node_2_a = route_2.sequenceOfNodes[node_position_2]
            node_2_b = route_2.sequenceOfNodes[node_position_2+1]
            if route_2 != route_1:
                flip_nodes()

    def cloneRoute(self, rt: Route):
        """
        Create a deep copy of a given route.

        Parameters:
        -----------
        rt : Route
            The route object to be cloned.

        Returns:
        --------
        Route
            Cloned route object.
        """
        cloned = Route(self.depot, self.capacity)
        cloned.cost = rt.cost
        cloned.load = rt.load
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        """
        Create a deep copy of a given solution.

        Parameters:
        -----------
        sol : Solution
            The solution object to be cloned.

        Returns:
        --------
        Solution
            Cloned solution object.
        """
        cloned = Solution()
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.cost = self.sol.cost
        return cloned

    def FindBestRelocationMoveForGLS(self, rm):
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[originRouteIndex]
            for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                for targetRouteIndex in range(0, len(self.sol.routes)):
                    rt2: Route = self.sol.routes[targetRouteIndex]
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes) - 1):

                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue

                        costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[F.ID][B.ID] + \
                                    self.distanceMatrix[B.ID][G.ID]
                        costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + \
                                      self.distanceMatrix[F.ID][G.ID]

                        costAdded_penalized = self.distance_matrix_penalized[A.ID][C.ID] + \
                                              self.distance_matrix_penalized[F.ID][B.ID] + \
                                              self.distance_matrix_penalized[B.ID][G.ID]
                        costRemoved_penalized = self.distance_matrix_penalized[A.ID][B.ID] + \
                                                self.distance_matrix_penalized[B.ID][C.ID] + \
                                                self.distance_matrix_penalized[F.ID][G.ID]

                        originRtCostChange = self.distanceMatrix[A.ID][C.ID] - self.distanceMatrix[A.ID][B.ID] - \
                                             self.distanceMatrix[B.ID][C.ID]
                        targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID] - \
                                             self.distanceMatrix[F.ID][G.ID]

                        moveCost = costAdded - costRemoved

                        moveCost_penalized = costAdded_penalized - costRemoved_penalized

                        if (moveCost_penalized < rm.moveCost_penalized):
                            self.StoreBestRelocationMoveForGLS(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                               targetNodeIndex, moveCost, moveCost_penalized,
                                                               originRtCostChange,
                                                               targetRtCostChange, rm)

    def FindBestRelocationMove(self, rm, iterator="", use_tabu=False):
        """
        Identify the best relocation move to improve the current solution.

        Parameters:
        -----------
        rm : RelocationMove
            Object to store the details of the best relocation move.
        """
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[originRouteIndex]
            for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                for targetRouteIndex in range(0, len(self.sol.routes)):
                    rt2: Route = self.sol.routes[targetRouteIndex]
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes) - 1):

                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue

                        costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[F.ID][B.ID] + \
                                    self.distanceMatrix[B.ID][G.ID]
                        costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + \
                                      self.distanceMatrix[F.ID][G.ID]

                        originRtCostChange = self.distanceMatrix[A.ID][C.ID] - self.distanceMatrix[A.ID][B.ID] - \
                                             self.distanceMatrix[B.ID][C.ID]
                        targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID] - \
                                             self.distanceMatrix[F.ID][G.ID]

                        moveCost = costAdded - costRemoved

                        if use_tabu == True:
                            if (self.MoveIsTabu(B, iterator, moveCost)):
                                continue

                        if (moveCost < rm.moveCost):
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                         targetNodeIndex, moveCost, originRtCostChange,
                                                         targetRtCostChange, rm)

    def FindBestSwapMove(self, sm, iterator="", use_tabu = False):
        """
        Finds the best swap move among all possible combinations of nodes in the solution's routes.

        Args:
            self: Instance of the VehicleRoutingProblem class.
            sm (SwapMove): The SwapMove object to store the best swap move.

        Returns:
            None

        This method iterates through all routes and nodes, evaluating potential swap moves.
        It calculates the cost changes for each move and updates the provided SwapMove object
        with the details of the best move found.
        """
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.cloneRoute(self.sol.routes[firstRouteIndex])
            for secondRouteIndex in range(firstRouteIndex, len(self.sol.routes)):
                rt2: Route = self.cloneRoute(self.sol.routes[secondRouteIndex])
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                # case of consecutive nodes swap
                                costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][b2.ID] + \
                                              self.distanceMatrix[b2.ID][c2.ID]
                                costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][b1.ID] + \
                                            self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded - costRemoved
                            else:

                                costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                                costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                                costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                                costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        else:
                            if rt1.load - b1.demand + b2.demand > self.capacity:
                                continue
                            if rt2.load - b2.demand + b1.demand > self.capacity:
                                continue

                            costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                            costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                            costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                            costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                            if use_tabu == True:
                                if self.MoveIsTabu(b1, iterator, moveCost) or self.MoveIsTabu(b2, iterator, moveCost):
                                    continue

                        if moveCost < sm.moveCost:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

    def FindBestSwapMoveForGLS(self, sm):
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range(firstRouteIndex, len(self.sol.routes)):
                rt2: Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][b2.ID] + \
                                              self.distanceMatrix[b2.ID][c2.ID]
                                costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][b1.ID] + \
                                            self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded - costRemoved

                                costRemoved_penalized = self.distance_matrix_penalized[a1.ID][b1.ID] + self.distance_matrix_penalized[b1.ID][b2.ID] + \
                                                        self.distance_matrix_penalized[b2.ID][c2.ID]
                                costAdded_penalized = self.distance_matrix_penalized[a1.ID][b2.ID] + self.distance_matrix_penalized[b2.ID][b1.ID] + \
                                                      self.distance_matrix_penalized[b1.ID][c2.ID]
                                moveCost_penalized = costAdded_penalized - costRemoved_penalized

                            else:
                                costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                                costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                                costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                                costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                costRemoved1_penalized = self.distance_matrix_penalized[a1.ID][b1.ID] + self.distance_matrix_penalized[b1.ID][c1.ID]
                                costAdded1_penalized = self.distance_matrix_penalized[a1.ID][b2.ID] + self.distance_matrix_penalized[b2.ID][c1.ID]
                                costRemoved2_penalized = self.distance_matrix_penalized[a2.ID][b2.ID] + self.distance_matrix_penalized[b2.ID][c2.ID]
                                costAdded2_penalized = self.distance_matrix_penalized[a2.ID][b1.ID] + self.distance_matrix_penalized[b1.ID][c2.ID]
                                moveCost_penalized = costAdded1_penalized + costAdded2_penalized - (costRemoved1_penalized + costRemoved2_penalized)
                        else:
                            if rt1.load - b1.demand + b2.demand > self.capacity:
                                continue
                            if rt2.load - b2.demand + b1.demand > self.capacity:
                                continue

                            costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                            costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                            costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                            costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]
                            costRemoved1_penalized = self.distance_matrix_penalized[a1.ID][b1.ID] + self.distance_matrix_penalized[b1.ID][c1.ID]
                            costAdded1_penalized = self.distance_matrix_penalized[a1.ID][b2.ID] + self.distance_matrix_penalized[b2.ID][c1.ID]
                            costRemoved2_penalized = self.distance_matrix_penalized[a2.ID][b2.ID] + self.distance_matrix_penalized[b2.ID][c2.ID]
                            costAdded2_penalized = self.distance_matrix_penalized[a2.ID][b1.ID] + self.distance_matrix_penalized[b1.ID][c2.ID]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            moveCost_penalized = costAdded1_penalized + costAdded2_penalized - (
                                        costRemoved1_penalized + costRemoved2_penalized)
                        if moveCost_penalized < sm.moveCost_penalized:
                            self.StoreBestSwapMoveForGLS(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, moveCost_penalized, costChangeFirstRoute, costChangeSecondRoute, sm)

    def ApplyRelocationMove(self, rm: RelocationMove, iterator=" " , use_tabu = False):
        """
        Applies the relocation move to the current solution.

        Args:
            rm (RelocationMove): The relocation move to be applied.

        Returns:
            None

        This method updates the solution by relocating a node from its current position
        to a new position within the same route or a different route, as specified by the
        given relocation move. The solution's cost, route costs, and loads are adjusted accordingly.
        """

        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.cost += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.cost += rm.costChangeOriginRt
            targetRt.cost += rm.costChangeTargetRt
            originRt.load -= B.demand
            targetRt.load += B.demand

        self.sol.cost += rm.moveCost

        newCost = self.CalculateTotalCost(self.sol)

        if use_tabu == True:
            self.SetTabuIterator(B, iterator)

    def ApplySwapMove(self, sm, iterator="", use_tabu = False):
        """
        Apply a swap move to the solution.

        Parameters:
        - sm (SwapMove): The swap move containing information about the move.

        Returns:
        None
        """
        oldCost = self.CalculateTotalCost(self.sol)
        rt1 = self.sol.routes[sm.positionOfFirstRoute]
        rt2 = self.sol.routes[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            rt1.cost += sm.moveCost
        else:
            rt1.cost += sm.costChangeFirstRt
            rt2.cost += sm.costChangeSecondRt
            rt1.load = rt1.load - b1.demand + b2.demand
            rt2.load = rt2.load + b1.demand - b2.demand

        self.sol.cost += sm.moveCost

        newCost = self.CalculateTotalCost(self.sol)

        if use_tabu == True:
            self.SetTabuIterator(b1, iterator)
            self.SetTabuIterator(b2, iterator)

    def GetLastOpenRoute(self):
        """
        Get the last open route in the current solution.

        Returns:
        - Route or None: The last open route if routes exist, otherwise None.
        """
        if len(self.sol.routes) == 0:
            return None
        else:
            return self.sol.routes[-1]

    def IdentifyBestInsertion(self, bestInsertion, rt):
        """
        Identifies the best customer insertion for a given route, considering capacity constraints.

        Parameters:
        - bestInsertion (CustomerInsertion): An object to store information about the best insertion.
        - rt (Route): The route for which the insertion is being considered.

        Returns:
        None

        Modifies the bestInsertion object with the details of the best customer insertion.
        """
        for i in range(1, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                if rt.load + candidateCust.demand <= rt.capacity:
                    lastNodePresentInTheRoute = rt.sequenceOfNodes[-2]
                    trialCost = self.distanceMatrix[lastNodePresentInTheRoute.ID][candidateCust.ID]
                    if trialCost < bestInsertion.cost:
                        bestInsertion.customer = candidateCust
                        bestInsertion.route = rt
                        bestInsertion.cost = trialCost

    def ApplyCustomerInsertion(self, insertion):
        """
        Applies the customer insertion to the given route in the solution.

        Parameters:
        - insertion (CustomerInsertion): An object containing information about the customer insertion.

        Returns:
        None

        Modifies the route and solution to reflect the applied customer insertion.
        """
        insCustomer = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = len(rt.sequenceOfNodes) - 1
        rt.sequenceOfNodes.insert(insIndex, insCustomer)

        beforeInserted = rt.sequenceOfNodes[-3]

        costAdded = self.distanceMatrix[beforeInserted.ID][insCustomer.ID] + self.distanceMatrix[insCustomer.ID][
            self.depot.ID]
        costRemoved = self.distanceMatrix[beforeInserted.ID][self.depot.ID]

        rt.cost += costAdded - costRemoved
        self.sol.cost += costAdded - costRemoved

        rt.load += insCustomer.demand

        insCustomer.isRouted = True

    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost,
                                originRtCostChange, targetRtCostChange, rm: RelocationMove):
        """
        Stores the information about the best relocation move in the given RelocationMove object.

        Parameters:
        - originRouteIndex (int): Index of the origin route.
        - targetRouteIndex (int): Index of the target route.
        - originNodeIndex (int): Index of the node in the origin route.
        - targetNodeIndex (int): Index of the node in the target route.
        - moveCost (float): Cost change due to the relocation move.
        - originRtCostChange (float): Cost change in the origin route.
        - targetRtCostChange (float): Cost change in the target route.
        - rm (RelocationMove): RelocationMove object to store the information.

        Returns:
        None

        Modifies the given RelocationMove object with the information about the best relocation move.
        """
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def StoreBestRelocationMoveForGLS(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex,
                                      moveCost,
                                      moveCost_penalized, originRtCostChange, targetRtCostChange, rm: RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost
        rm.moveCost_penalized = moveCost_penalized

    def StoreBestSwapMoveForGLS(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost,
                                moveCost_penalized, costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost
        sm.moveCost_penalized = moveCost_penalized
    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost,
                          costChangeFirstRoute, costChangeSecondRoute, sm):
        """
        Stores the information about the best swap move in the given SwapMove object.

        Parameters:
        - firstRouteIndex (int): Index of the first route involved in the swap.
        - secondRouteIndex (int): Index of the second route involved in the swap.
        - firstNodeIndex (int): Index of the node in the first route.
        - secondNodeIndex (int): Index of the node in the second route.
        - moveCost (float): Cost change due to the swap move.
        - costChangeFirstRoute (float): Cost change in the first route.
        - costChangeSecondRoute (float): Cost change in the second route.
        - sm (SwapMove): SwapMove object to store the information.

        Returns:
        None

        Modifies the given SwapMove object with the information about the best swap move.
        """

        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost

    def CalculateTotalCost(self, sol):
        """
        Calculates the total cost of a given solution.

        Parameters:
        - sol (Solution): Solution object for which the total cost is calculated.

        Returns:
        float: Total cost of the solution.

        Iterates through each route in the solution and computes the sum of distances
        between consecutive nodes in each route, using the distance matrix.
        """
        c = 0
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                c += self.distanceMatrix[a.ID][b.ID]
        return c

    def InitializeOperators(self, rm, sm, top):
        """
        Initializes the move operators for local search.

        Parameters:
        - rm (RelocationMove): The relocation move object to be initialized.
        - sm (SwapMove): The swap move object to be initialized.
        - top (TwoOptMove): The 2-opt move object to be initialized.

        Returns:
        None
        """
        rm.Initialize()
        sm.Initialize()
        top.Initialize()

    def FindBestTwoOptMove(self, top, iterator="", use_tabu = False):
        """
        Finds the best 2-opt move among all possible combinations of routes and nodes.

        Parameters:
        - top (TwoOptMove): The TwoOptMove object to store the best move information.

        Returns:
        None
        """
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2: Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2
                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                        moveCost = 10 ** 9

                        A = rt1.sequenceOfNodes[nodeInd1]
                        B = rt1.sequenceOfNodes[nodeInd1 + 1]
                        K = rt2.sequenceOfNodes[nodeInd2]
                        L = rt2.sequenceOfNodes[nodeInd2 + 1]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 2:
                                continue
                            costAdded = self.distanceMatrix[A.ID][K.ID] + self.distanceMatrix[B.ID][L.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.sequenceOfNodes) - 2 and nodeInd2 == len(rt2.sequenceOfNodes) - 2:
                                continue

                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue
                            costAdded = self.distanceMatrix[A.ID][L.ID] + self.distanceMatrix[B.ID][K.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        if use_tabu == True:
                            if self.MoveIsTabu(A, iterator, moveCost) or self.MoveIsTabu(K, iterator, moveCost):
                                continue

                        if moveCost < top.moveCost:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

    def FindBestTwoOptMoveForGLS(self, top):
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2: Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                        moveCost = 10 ** 9
                        moveCost_penalized = 10 ** 9

                        A = rt1.sequenceOfNodes[nodeInd1]
                        B = rt1.sequenceOfNodes[nodeInd1 + 1]
                        K = rt2.sequenceOfNodes[nodeInd2]
                        L = rt2.sequenceOfNodes[nodeInd2 + 1]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 2:
                                continue
                            costAdded = self.distanceMatrix[A.ID][K.ID] + self.distanceMatrix[B.ID][L.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            costAdded_penalized = self.distance_matrix_penalized[A.ID][K.ID] + self.distance_matrix_penalized[B.ID][L.ID]
                            costRemoved_penalized = self.distance_matrix_penalized[A.ID][B.ID] + self.distance_matrix_penalized[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                            moveCost_penalized = costAdded_penalized - costRemoved_penalized
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.sequenceOfNodes) - 2 and nodeInd2 == len(rt2.sequenceOfNodes) - 2:
                                continue

                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue
                            costAdded = self.distanceMatrix[A.ID][L.ID] + self.distanceMatrix[B.ID][K.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            costAdded_penalized = self.distance_matrix_penalized[A.ID][L.ID] + self.distance_matrix_penalized[B.ID][K.ID]
                            costRemoved_penalized = self.distance_matrix_penalized[A.ID][B.ID] + self.distance_matrix_penalized[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                            moveCost_penalized = costAdded_penalized - costRemoved_penalized
                        if moveCost_penalized < top.moveCost_penalized:
                            self.StoreBestTwoOptMoveForGLS(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, moveCost_penalized, top)

    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):
        """
        Checks whether the capacity of the given routes is violated after a potential 2-opt move.

        Parameters:
        - rt1 (Route): Index of the first route involved in the swap.
        - nodeInd1 (int): Index of the node in `rt1` before which the segment load is calculated.
        - rt2 (Route): Index of the second route involved in the swap.
        - nodeInd2 (int): Index of the node in `rt2` before which the segment load is calculated.

        Returns:
        - bool: True if the capacity is violated. Otherwise, it return false.
        """

        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.sequenceOfNodes[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.load - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.sequenceOfNodes[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.load - rt2FirstSegmentLoad

        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.capacity):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.capacity):
            return True

        return False

    def StoreBestTwoOptMoveForGLS(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, moveCost_penalized, top):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost
        top.moveCost_penalized = moveCost_penalized

    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
        """
        Stores the information of the best 2-opt move in the provided TwoOptMove object.

        Parameters:
        - rtInd1 (int): Index of the first route in the solution.
        - rtInd2 (int): Index of the second route in the solution.
        - nodeInd1 (int): Index of the first node in the first route.
        - nodeInd2 (int): Index of the second node in the second route.
        - moveCost (float): The cost associated with the 2-opt move.
        - top (TwoOptMove): TwoOptMove object to be updated with the best move information.
        """
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost

    def ApplyTwoOptMove(self, top, iterator="", use_tabu = False):
        """
        Applies the best 2-opt move to the solution based on the information provided in the TwoOptMove object.

        It updates the overall cost of the solution.

        Parameters:
        - top (TwoOptMove): TwoOptMove object which contains the information about the best 2-opt move.
        """
        rt1: Route = self.sol.routes[top.positionOfFirstRoute]
        rt2: Route = self.sol.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment
            if use_tabu == True:
                self.SetTabuIterator(rt1.sequenceOfNodes[top.positionOfFirstNode], iterator)
                self.SetTabuIterator(rt1.sequenceOfNodes[top.positionOfSecondNode], iterator)
            rt1.cost += top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            if use_tabu == True:
                self.SetTabuIterator(rt1.sequenceOfNodes[top.positionOfFirstNode], iterator)
                self.SetTabuIterator(rt2.sequenceOfNodes[top.positionOfSecondNode], iterator)

            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)

        self.sol.cost += top.moveCost

    def UpdateRouteCostAndLoad(self, rt: Route):
        """
        Updates the cost and load of a given route.

        Parameters:
        - rt (Route): The route whose cost and load need to be updated.
        """
        tc = 0
        tl = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i + 1]
            tc += self.distanceMatrix[A.ID][B.ID]
            tl += A.demand
        rt.load = tl
        rt.cost = tc

    def TestSolution(self):
        """
        Calculates the total cost of the solution and compares it with the stored solution cost.
        """
        totalSolCost = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtCost = 0
            rtLoad = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtCost += self.distanceMatrix[A.ID][B.ID]
                rtLoad += A.demand
            totalSolCost += rt.cost

    def ReportSolutionToFile(self, sol, filename):
        sol.cost = 0
        for route in sol.routes:
            (route_tn_km, route_dem) = route.calculate_route_details(self)
            sol.cost += route_tn_km
            route.cost = route_tn_km
        with open(filename, 'w') as file:
            file.write("Cost:\n")
            file.write(str(sol.cost) + "\n")

            file.write("Routes:\n")
            file.write(str(len(sol.routes) - 1) + "\n")

            for i in range(len(sol.routes) - 1):
                rt = sol.routes[i]
                nodes = ["0"] + [str(node.ID) for node in rt.sequenceOfNodes if
                                 node.ID != 0]  # Include a zero at the beginning
                route_str = ",".join(nodes) + "\n"
                file.write(route_str)

    def reverseRoutes(self):
        """
        Takes all routes and tries to see if the reversed route is better.
        This makes a difference due to tonnage!

        :returns: None
        """

        for i, route in enumerate(self.sol.routes):
            (old_route_tn_km, _) = route.calculate_route_details(self)
            copy_of_route = self.cloneRoute(route)
            copy_of_route.sequenceOfNodes.reverse()
            (new_route_tn_km, _) = copy_of_route.calculate_route_details(self)
            if new_route_tn_km < old_route_tn_km:
                self.sol.routes[i] = copy_of_route

    def randomlyPartlyReverseRoutes(self, seed: int, iterations=99999):
        """
        Partly reverses subsets of routes

        :arg seed: Pick a number 1~5
        :arg iterations: How many times (99999) recommended
        :returns: None
        """
        def reverse(list):
            """
            Revese!
            Args:
                list:

            Returns:

            """
            temp_list = [item for item in list]
            j = len(temp_list)-1
            for i in range(len(list)):
                list[j] = temp_list[i]
                j -= 1
            return list
        random.seed(seed)
        for _ in range(iterations):
            for i, route in enumerate(self.sol.routes):
                try:
                    start = random.randint(1, len(route.sequenceOfNodes) - 2)
                    end = random.randint(start+2, len(route.sequenceOfNodes) - 2)
                except Exception:
                    continue
                (old_route_tn_km, _) = route.calculate_route_details(self)
                copy_of_route = self.cloneRoute(route)
                # takes a list slice and partly reverses it. Kinda in place like C++
                copy_of_route.sequenceOfNodes[start:end] = reverse(copy_of_route.sequenceOfNodes[start:end])
                (new_route_tn_km, _) = copy_of_route.calculate_route_details(self)
                if new_route_tn_km < old_route_tn_km:
                    self.sol.routes[i] = copy_of_route

    def penalize_arcsForGLS(self):
        max_criterion = 0
        pen_1 = -1
        pen_2 = -1
        for i in range(len(self.sol.routes)):
            rt = self.sol.routes[i]
            for j in range(len(rt.sequenceOfNodes) - 1):
                id1 = rt.sequenceOfNodes[j].ID
                id2 = rt.sequenceOfNodes[j + 1].ID
                criterion = self.distanceMatrix[id1][id2] / (1 + self.times_penalized[id1][id2])
                if criterion > max_criterion:
                    max_criterion = criterion
                    pen_1 = id1
                    pen_2 = id2
        self.times_penalized[pen_1][pen_2] += 1
        self.times_penalized[pen_2][pen_1] += 1

        pen_weight = 0.15

        self.distanceMatrix[pen_1][pen_2] = (1 + pen_weight * self.times_penalized[pen_1][pen_2]) * self.distanceMatrix[pen_1][pen_2]
        self.distanceMatrix[pen_2][pen_1] = (1 + pen_weight * self.times_penalized[pen_2][pen_1]) * self.distanceMatrix[pen_2][pen_1]
        self.penalized_n1_ID = pen_1
        self.penalized_n2_ID = pen_2

    def Tabu(self):
        self.bestSolution = self.cloneSolution(self.sol)
        use_tabu = True
        solution_cost_trajectory = []
        random.seed(1)
        terminationCondition = False
        localSearchIterator = 0
        stuck_iterator=0
        rm = RelocationMove()
        sm = SwapMove()
        top:TwoOptMove = TwoOptMove()
        while terminationCondition is False:
            if localSearchIterator % 100 == 0:
                self.reverseRoutes()
            operator = random.randint(0,2)
            rm.Initialize()
            sm.Initialize()
            top.Initialize()
            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm, localSearchIterator, use_tabu)
                if rm.originRoutePosition is not None:
                    self.ApplyRelocationMove(rm, localSearchIterator, use_tabu)
            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm, localSearchIterator, use_tabu)
                if sm.positionOfFirstRoute is not None:
                    self.ApplySwapMove(sm, localSearchIterator, use_tabu)
            elif operator == 2:
                self.FindBestTwoOptMove(top, localSearchIterator, use_tabu)
                if top.positionOfFirstRoute is not None:
                    self.ApplyTwoOptMove(top, localSearchIterator, use_tabu)
            self.TestSolution()
            solution_cost_trajectory.append(self.sol.cost)
            self.sol.cost=0
            #idenify if solution is stuck at local optimum and uses a different operator
            for route in self.sol.routes:
                (route_tn_km, route_dem) = route.calculate_route_details(self)
                self.sol.cost += route_tn_km
                route.cost = route_tn_km
            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)
                stuck_iterator=0
            else:
                stuck_iterator = stuck_iterator + 1
            if stuck_iterator > 400:
                select=random.randint(1,3)
                if select == 1:
                    self.ClownMove(1, 1.01, 1000)
                if select == 2 :
                    self.randomlyPartlyReverseRoutes(1,2)
                elif select == 3:
                    self.reverseRoutes()
                stuck_iterator = 0
            localSearchIterator = localSearchIterator + 1
            if localSearchIterator > 250:
                terminationCondition = True
        self.sol = self.bestSolution

    def MoveIsTabu(self, n: Node, iterator, moveCost):
        if moveCost + self.sol.cost < self.bestSolution.cost - 0.001:
            return False
        if iterator < n.isTabuTillIterator:
            return True
        return False

    def SetTabuIterator(self, n: Node, iterator):
        n.isTabuTillIterator = iterator + random.randint(self.minTabuTenure, self.maxTabuTenure)
