import os
from main import solve


N = 1


for test in sorted(os.listdir("tests")):
    print("Processing", test)
    fitness = 0
    success = 0
    best_fitness = 0
    solved_puzzle_with_best_fitness = None
    for i in range(N):
        puzzle, objective_values = solve(f"tests/{test}") #, metrics=['best_objective'])
        fitness += objective_values[-1]
        if fitness > best_fitness:
            best_fitness = fitness
            solved_puzzle_with_best_fitness = puzzle
        if fitness == 100:
            success += 1
    print(test, "success rate:", success / N, "average fitness:", fitness / N)
    with open(f"tests/output.{test}", "w") as f:
        f.write(str(solved_puzzle_with_best_fitness))
    with open(f"tests/solved_cells.{test}", "w") as f:
        f.write("\n".join(f"{i} {j}" for i, j in solved_puzzle_with_best_fitness.empty_cells))