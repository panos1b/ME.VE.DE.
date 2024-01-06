from Solver import *
FILE_NAME = 'example_solution.txt'

m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()
s.ReportSolutionToFile(sol, FILE_NAME)
with open(FILE_NAME, 'r') as f:
    print("\n"+f.read())
