#from TSP_Model import Model
from Solver import *
import sol_checker
FILE_NAME = 'test.txt'

m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()
s.ReportSolutionToFile(sol, FILE_NAME)
with open(FILE_NAME, 'r') as f:
    print("\n"+f.read())
sol_checker.load_model(FILE_NAME)
