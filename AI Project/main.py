import random
from typing import List
import numpy as np
from genetic import GeneticAlgorithmModel, Gene, GeneticAlgorithmBehaviour
from puzzle import Puzzle, Dots
from gui import draw_puzzle


class Behaviour(GeneticAlgorithmBehaviour):
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.row_count, self.column_count, self.max_num = puzzle.row_count, puzzle.column_count, puzzle.max_num
        self.cells = puzzle.cells
        self.fixed_nums = puzzle.fixed_nums
        self.empty_cells = puzzle.empty_cells
        self.dot_count = puzzle.dot_count
        self.dots: Dots = puzzle.dots
        puzzle.calculate_cells_pairwise_distances()
        self.pure_gene = []
        for i in range(1, self.max_num + 1):
            if not puzzle.find_coordinates(i):
                self.pure_gene.append(i)
        self.transform = {self.pure_gene[i]: i for i in range(len(self.pure_gene))}

    def objective1(self, gene: List[int]):
        correct = 0.0
        puzzle.set_empty_cells(gene)
        for i in range(self.dot_count):
            correct += 10 * puzzle.is_successor(self.dots[i][0], self.dots[i][1])
        for i in range(1, self.max_num):
            if i in self.fixed_nums or i + 1 in self.fixed_nums:
                correct += 100 * puzzle.is_neighbour(puzzle.find_coordinates(i), puzzle.find_coordinates(i + 1))
            else:
                correct += puzzle.is_neighbour(puzzle.find_coordinates(i), puzzle.find_coordinates(i + 1))

        return correct

    def objective(self, gene: List[int]):
        miss = 0.0
        tt = 0
        puzzle.set_empty_cells(gene)
        for i in range(self.dot_count):
            tt += puzzle.is_successor(self.dots[i][0], self.dots[i][1])
        for i in range(1, self.max_num):
            if i in self.fixed_nums or i + 1 in self.fixed_nums:
                miss += 10 * (10 - puzzle.pairwise_distances[
                    (puzzle.find_coordinates(i), puzzle.find_coordinates(i + 1))
                ]) ** 3
            else:
                miss += 10 * (10-puzzle.pairwise_distances[
                    (puzzle.find_coordinates(i), puzzle.find_coordinates(i + 1))
                ]) ** 2

        t = 0
        for i in range(1, self.max_num):
            if puzzle.pairwise_distances[puzzle.find_coordinates(i), puzzle.find_coordinates(i + 1)] != 1:
                break
            t += 1

        return miss + t + 10*tt**3

    def random_population(self, population_size: int):
        solution = []
        for i in range(1, self.max_num + 1):
            if not puzzle.find_coordinates(i):
                solution.append(i)
        population = []
        for i in range(population_size):
            random.shuffle(solution)
            population.append(Gene(solution.copy(), self.objective(solution)))
        return population

    def crossover(self, parent1: Gene, parent2: Gene):
        if len(parent1.values) != len(parent2.values):
            raise Exception('Gene sizes are not equal!!')
        child1, child2 = [], []
        for u in parent1.values:
            child1.append(parent2.values[self.transform[u]])
        for u in parent2.values:
            child2.append(parent1.values[self.transform[u]])
        return Gene(child1, self.objective(child1)), Gene(child2, self.objective(child2))

    def mutation(self, gene: Gene):
        gene_size = len(gene.values)
        i1, i2 = np.random.choice(range(gene_size), 2, replace=False)
        gene_values = gene.values
        gene_values[i1], gene_values[i2] = gene_values[i2], gene_values[i1]
        return Gene(gene_values, self.objective(gene_values))

    def is_goal(self, gene: Gene) -> bool:
        self.puzzle.set_empty_cells(gene.values)
        for i in range(1, self.max_num):
            if puzzle.pairwise_distances[puzzle.find_coordinates(i), puzzle.find_coordinates(i + 1)] != 1:
                return False
        for cell1, cell2 in self.dots:
            if not puzzle.is_successor(cell1, cell2):
                return False
        return True


#import matplotlib.pyplot as plt
#plt.plot(range(len(r)), r)
#plt.xlabel('epochs')
#plt.ylabel('objective value')
#plt.show()

with open('input.txt') as f:
    puzzle = Puzzle.parse(f.read())

behaviour = Behaviour(puzzle)
model = GeneticAlgorithmModel(behaviour, 1000, 0.1, 2)
r = model.fit(300, metrics=['best_objective'])  # 'mutates', 'crossovers', ...
g = model.best_sol()
puzzle.set_empty_cells(g.values)
draw_puzzle(str(puzzle), behaviour.empty_cells)
