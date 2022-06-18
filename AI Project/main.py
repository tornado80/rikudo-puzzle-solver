import random
from typing import Callable, List, Any
import numpy as np
from genetic import GeneticAlgorithmModel, Gene


def find_next(s):
    i = s.find(' ')
    last = 0
    while i != -1:
        try:
            yield int(s[last:i])
        except:
            pass
        last = i
        i = s.find(' ', i+1)
    try:
        yield int(s[last:])
    except:
        pass


def find_int(x, k):
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] == k:
                return [i, j]
    return [-1, -1]


with open('D:\\Projects\\AI Project\\input.txt') as f:
    lines = f.readlines()

(n_max, m_max, max_num) = [i for i in find_next(lines[0])]
cells = []
fixed_nums = []
for i in range(n_max):
    t = []
    for k in find_next(lines[i+1]):
        if len(t) >= m_max:
            raise Exception('error')
        t.append(k)
        if k>0:
            fixed_nums.append(k)
    cells.append(t)

[r] = [i for i in find_next(lines[n_max+1])]
consts = []
for i in range(r):
    t = []
    for k in find_next(lines[n_max + 2 + i]):
        t.append(k)
    consts.append(t)

empty_cells = []
for i in range(n_max):
    for j in range(len(cells[i])):
        if cells[i][j] == 0:
            empty_cells.append([i, j])

print(empty_cells)


def neighbor_num(a, b):
    return abs(a-b) == 1


def neighbor_cell(x1, x2):
    if x1[0] == x2[0]:
        return abs(x1[1] - x2[1]) == 1
    elif x1[0] + 1 == x2[0] and len(cells[x1[0]]) > len(cells[x2[0]]):
        return x1[1] == x2[1] or x1[1] == x2[1] + 1
    elif x1[0] + 1 == x2[0] and len(cells[x1[0]]) < len(cells[x2[0]]):
        return x1[1] == x2[1] or x1[1] + 1 == x2[1]
    elif x1[0] == x2[0] + 1 and len(cells[x1[0]]) > len(cells[x2[0]]):
        return x1[1] == x2[1] or x1[1] + 1 == x2[1]
    elif x1[0] == x2[0] + 1 and len(cells[x1[0]]) < len(cells[x2[0]]):
        return x1[1] == x2[1] or x1[1] == x2[1] + 1
    else:
        return False


def objective(item):
    correct = 0.0
    for i in range(len(item)):
        cells[empty_cells[i][0]][empty_cells[i][1]] = item[i]
    for i in range(r):
        correct += 100*neighbor_num(cells[consts[i][0]][consts[i][1]], cells[consts[i][2]][consts[i][3]])
    for i in range(1, max_num):
        if i in fixed_nums or i+1 in fixed_nums:
            correct += 1000*neighbor_cell(find_int(cells, i), find_int(cells, i + 1))
        else:
            correct += neighbor_cell(find_int(cells, i), find_int(cells, i+1))

    return correct


def dist(x1, x2):
    if abs(x1[0]-x2[0]) > 1:
        return abs(x1[0]-x2[0])
    return 0


def objective1(item):
    miss = 0.0
    for i in range(len(item)):
        cells[empty_cells[i][0]][empty_cells[i][1]] = item[i]
    for i in range(r):
        miss += 100*(1-neighbor_num(cells[consts[i][0]][consts[i][1]], cells[consts[i][2]][consts[i][3]]))
    for i in range(1, max_num):
        miss += dist(find_int(cells, i), find_int(cells, i+1))
        miss += (1-neighbor_cell(find_int(cells, i), find_int(cells, i + 1)))
    return 1/miss

def random_perm_genes(n):
    solution = []
    for i in range(1, max_num+1):
        if find_int(cells, i)[0] == -1:
            solution.append(i)
    population = []
    for i in range(n):
        random.shuffle(solution)
        population.append(Gene(solution.copy(), objective(solution)))
    return population


pure_gene = []
for i in range(1, max_num+1):
    if find_int(cells, i)[0] == -1:
        pure_gene.append(i)


def crossover(parent1, parent2):
    if len(parent1.values) != len(parent2.values):
        raise Exception('Gene sizes are not equal!!')
    transform = {pure_gene[i]: i for i in range(len(pure_gene))}
    child1, child2 = [], []
    for u in parent1.values:
        child1.append(parent2.values[transform[u]])
    for u in parent2.values:
        child2.append(parent1.values[transform[u]])
    return Gene(child1, objective(child1)), Gene(child2, objective(child2))


def mutation(gene):
    gene_size = len(gene.values)
    i1, i2 = np.random.choice(range(gene_size), 2, replace=False)
    gene_values = gene.values
    gene_values[i1], gene_values[i2] = gene_values[i2], gene_values[i1]
    return Gene(gene_values, objective(gene_values))

model = GeneticAlgorithmModel(len(pure_gene), 300)
model.compile(crossover, mutation, random_perm_genes, 0.8, 0.5)
r = model.fit(1000, metrics=['best_objective']) #'mutates', 'crossovers', ...
import matplotlib.pyplot as plt
plt.plot(range(len(r)), r)
plt.xlabel('epochs')
plt.ylabel('objective value')
plt.show()
