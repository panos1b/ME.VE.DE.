#from TSP_Model import Model
from Solver import *
FILE_NAME = 'test.txt'

m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()
s.ReportSolutionToFile(sol, FILE_NAME)
with open(FILE_NAME, 'r') as f:
    print("\n"+f.read())
