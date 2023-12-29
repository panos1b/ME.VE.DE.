from VRP_Model import *
from SolutionDrawer import *


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

    def Initialize(self):
        """
        Resets the attributes to their initial values, setting moveCost to a large value(10^9).
        """
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9


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

    Always_keep_an_empty_route():
       Ensure there is always at least one empty route available.
       Adds a new route if the last route is partially filled.

    MinimumInsertions():
         Construct initial routes using the minimum insertions.
         Continuously identifies the best customer to insert into the current routes. (prioritizes inserting customers with the least additional distance.)

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

    TestSolution():
        Tests the integrity of the solution by checking route costs and loads.

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
        # self.ApplyNearestNeighborMethod()
        self.MinimumInsertions()
        self.LocalSearch(1)
        self.LocalSearch(0)
        self.LocalSearch(2)
        return self.sol

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

        if (modelIsFeasible == False):
            print('FeasibilityIssue')
            # reportSolution

    # def MinimumInsertions(self):
    #     modelIsFeasible = True
    #     self.sol = Solution()
    #     insertions = 0
    #
    #     while (insertions < len(self.customers)):
    #         bestInsertion = CustomerInsertionAllPositions()
    #         lastOpenRoute: Route = self.GetLastOpenRoute()
    #
    #         if lastOpenRoute is not None:
    #             self.IdentifyBestInsertionAllPositions(bestInsertion, lastOpenRoute)
    #
    #         if (bestInsertion.customer is not None):
    #             self.ApplyCustomerInsertionAllPositions(bestInsertion)
    #             insertions += 1
    #         else:
    #             # If there is an empty available route
    #             if lastOpenRoute is not None and len(lastOpenRoute.sequenceOfNodes) == 2:
    #                 modelIsFeasible = False
    #                 break
    #             # If there is no empty available route and no feasible insertion was identified
    #             else:
    #                 rt = Route(self.depot, self.capacity)
    #                 self.sol.routes.append(rt)
    #
    #     if (modelIsFeasible == False):
    #         print('FeasibilityIssue')
    #         # reportSolution
    #
    #     self.TestSolution()

    def Always_keep_an_empty_route(self):
        """
        Ensure there is always at least one empty route available.
        Adds a new route if the last route is partially filled.
        """
        if len(self.sol.routes) == 0:
            rt = Route(self.depot, self.capacity)
            self.sol.routes.append(rt)
        else:
            rt = self.sol.routes[-1]
            if len(rt.sequenceOfNodes) > 2:
                rt = Route(self.depot, self.capacity)
                self.sol.routes.append(rt)

    def MinimumInsertions(self):
        """
         Construct initial routes using the minimum insertions.
         Continuously identifies the best customer to insert into the current routes. (prioritizes inserting customers with the least additional distance.)
        """
        model_is_feasible = True
        self.sol = Solution()
        insertions = 0

        while insertions < len(self.customers):
            best_insertion = CustomerInsertionAllPositions()
            self.Always_keep_an_empty_route()
            self.IdentifyMinimumCostInsertion(best_insertion)

            if best_insertion.customer is not None:
                self.ApplyCustomerInsertionAllPositions(best_insertion)
                insertions += 1
            else:
                print('FeasibilityIssue')
                model_is_feasible = False
                break

        if model_is_feasible:
            self.TestSolution()

    def LocalSearch(self, operator):
        """
        Apply local search techniques to further optimize the solution.

        Parameters:
        -----------
        operator : int
            Type of local search operation to perform (0: Relocation, 1: Swap, 2: TwoOpt).
        """
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()

        while terminationCondition is False:

            self.InitializeOperators(rm, sm, top)
#            SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            elif operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True

#            self.TestSolution()

            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1
            print(localSearchIterator, self.sol.cost)

        self.sol = self.bestSolution

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

    def FindBestRelocationMove(self, rm):
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

                        if (moveCost < rm.moveCost):
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                         targetNodeIndex, moveCost, originRtCostChange,
                                                         targetRtCostChange, rm)

    def FindBestSwapMove(self, sm):
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

                        if moveCost < sm.moveCost:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

    def ApplyRelocationMove(self, rm: RelocationMove):
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
        # debuggingOnly
        if abs((newCost - oldCost) - rm.moveCost) > 0.0001:
            print('Cost Issue')

    def ApplySwapMove(self, sm):
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
        # debuggingOnly
        if abs((newCost - oldCost) - sm.moveCost) > 0.0001:
            print('Cost Issue')


    def ReportSolution(self, sol):
        """
        Print a report of the given solution.

        Parameters:
        - sol (Solution): The solution to be reported.

        Returns:
        None
        """
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.cost)
        print(self.sol.cost)


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
        for i in range(0, len(self.customers)):
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


    def FindBestTwoOptMove(self, top):
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
                        if moveCost < top.moveCost:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)


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


    def ApplyTwoOptMove(self, top):
        """
        Applies the best 2-opt move to the solution based on the information provided in the TwoOptMove object.

        It updates the overall cost of the solution.

        Parameters:
        - top (TwoOptMove): TwoOptMove object which contains the information about the best 2-opt move.
        """
        rt1: Route = self.sol.routes[top.positionOfFirstRoute]
        rt2: Route = self.sol.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            # lst = list(reversedSegment)
            # lst2 = list(reversedSegment)
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment

            # reversedSegmentList = list(reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            # rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

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
        Tests the integrity of the solution by checking route costs and loads.

        Also, it calculates the total cost of the solution and compares it with the stored solution cost.

        Note: This method is primarily for debugging purposes.

        Raises:
        - AssertionError: If any route cost or load does not match the stored values.
                          If the total solution cost does not match the stored solution cost.
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
            if abs(rtCost - rt.cost) > 0.0001:
                print('Route Cost problem')
            if rtLoad != rt.load:
                print('Route Load problem')

            totalSolCost += rt.cost

        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')


    def IdentifyMinimumCostInsertion(self, best_insertion):
        """

        Identifies the minimum cost insertion for a customer into existing routes.

        Updates the best_insertion object with information about the customer, route, insertion position,
        and the associated cost.

        Parameters:
        - best_insertion (CustomerInsertion): An object to store information about the best insertion.

        Returns:
        None
        """

        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                for rt in self.sol.routes:
                    if rt.load + candidateCust.demand <= rt.capacity:
                        for j in range(0, len(rt.sequenceOfNodes) - 1):
                            A = rt.sequenceOfNodes[j]
                            B = rt.sequenceOfNodes[j + 1]
                            costAdded = self.distanceMatrix[A.ID][candidateCust.ID] + self.distanceMatrix[candidateCust.ID][
                                B.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID]
                            trialCost = costAdded - costRemoved
                            if trialCost < best_insertion.cost:
                                best_insertion.customer = candidateCust
                                best_insertion.route = rt
                                best_insertion.insertionPosition = j
                                best_insertion.cost = trialCost
                    else:
                        continue


    def ApplyCustomerInsertionAllPositions(self, insertion):
        """
        Applies the customer insertion at all possible positions within a route.

        Marks the inserted customer as routed.

        Parameters:
        - insertion (CustomerInsertion): An object containing information about the customer insertion.

            Returns:
            None
        """
        insCustomer = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = insertion.insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1, insCustomer)
        rt.cost += insertion.cost
        self.sol.cost += insertion.cost
        rt.load += insCustomer.demand
        insCustomer.isRouted = True


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
            file.write(str(len(sol.routes)-1) + "\n")

            for i in range(len(sol.routes)-1):
                rt = sol.routes[i]
                nodes = ["0"] + [str(node.ID) for node in rt.sequenceOfNodes if
                                 node.ID != 0]  # Include a zero at the beginning
                route_str = ",".join(nodes) + "\n"
                file.write(route_str)

