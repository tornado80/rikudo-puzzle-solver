import os
from main import solve


N = 1


for test in sorted(os.listdir("tests")):
    print("Processing", test)
    fitness = 0
    success = 0
    for i in range(N):
        puzzle, objective_values = solve(f"tests/{test}") #, metrics=['best_objective'])
        fitness += objective_values[-1]
        if fitness == 100:
            success += 1
    print(test, "success rate:", success / N, "average fitness:", fitness / N)
