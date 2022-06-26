import random
from typing import List, Dict
import numpy as np
from genetic import GeneticAlgorithmModel, Gene, GeneticAlgorithmBehaviour
from puzzle import Puzzle
from gui import draw_puzzle


class Behaviour(GeneticAlgorithmBehaviour):
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.transform: Dict[int, int] = {}
        self.calculate_transformation_of_solved_nums_to_permutation()
        self.fitness_evaluations = 0

    def calculate_transformation_of_solved_nums_to_permutation(self):
        pure_gene = []
        for i in range(1, self.puzzle.max_num + 1):
            if i not in self.puzzle.fixed_nums:
                pure_gene.append(i)
        self.transform = {pure_gene[i]: i for i in range(len(pure_gene))}

    def fitness3(self, gene: List[int]):
        correct = 0.0
        for i in range(self.puzzle.dot_count):
            correct += 10 * self.puzzle.is_successor(self.puzzle.dots[i][0], self.puzzle.dots[i][1])
        for i in range(1, self.puzzle.max_num):
            if i in self.puzzle.fixed_nums or i + 1 in self.puzzle.fixed_nums:
                correct += 100 * self.puzzle.is_neighbour(self.puzzle.find_coordinates(i), self.puzzle.find_coordinates(i + 1))
            else:
                correct += self.puzzle.is_neighbour(self.puzzle.find_coordinates(i), self.puzzle.find_coordinates(i + 1))

        return correct

    def objective(self, gene: List[int]):
        self.fitness_evaluations += 1
        self.puzzle.set_empty_cells(gene)
        return self.fitness(gene)

    def fitness1(self, gene: List[int]):
        # in the following code we are assuming 1 and max_num are always fixed
        i = 1
        total_fitness = 1
        max_total_fitness = 1
        while i < self.puzzle.max_num:
            # each segment is the numbers between two successive fixed nums
            segment_size = 1
            i += 1
            max_distance_in_segment = 1
            while True:  # iterating over the numbers in a segment
                segment_size += 1
                previous_cell = self.puzzle.find_coordinates(i - 1)
                current_cell = self.puzzle.find_coordinates(i)
                max_distance_in_segment = max(
                    max_distance_in_segment,
                    self.puzzle.pairwise_distances[previous_cell, current_cell]
                )
                if i in self.puzzle.fixed_nums:
                    break
                i += 1
            max_segment_fitness = 2 ** segment_size
            segment_fitness = max(1, max_segment_fitness - 2 ** (max_distance_in_segment - 1))
            total_fitness *= segment_fitness
            max_total_fitness *= max_segment_fitness - 1
        dots_satisfied = 0
        for i in range(self.puzzle.dot_count):
            dots_satisfied += self.puzzle.is_successor(self.puzzle.dots[i][0], self.puzzle.dots[i][1])
        y = total_fitness / max_total_fitness * 100
        x = dots_satisfied / (self.puzzle.max_num - 1) * 100
        return x * 0.1 + y * 0.9

    def fitness(self, gene: List[int]):
        mx = 0
        miss = 0.0
        tt = 0
        for i in range(self.puzzle.dot_count):
            tt += self.puzzle.is_successor(self.puzzle.dots[i][0], self.puzzle.dots[i][1])

        mx = 10*(self.puzzle.dot_count**3)
        for i in range(1, self.puzzle.max_num):
            if i in self.puzzle.fixed_nums or i + 1 in self.puzzle.fixed_nums:
                miss += 10 * (10 - self.puzzle.pairwise_distances[
                    (self.puzzle.find_coordinates(i), self.puzzle.find_coordinates(i + 1))
                ]) ** 3
                mx += 10*(9**3)
            else:
                miss += 10 * (10-self.puzzle.pairwise_distances[
                    (self.puzzle.find_coordinates(i), self.puzzle.find_coordinates(i + 1))
                ]) ** 2
                mx += 10 * (9 ** 2)
        t = 0

        for i in range(1, self.puzzle.max_num):
            if self.puzzle.pairwise_distances[self.puzzle.find_coordinates(i), self.puzzle.find_coordinates(i + 1)] != 1:
                break
            t += 1
        mx += self.puzzle.max_num - 1
        return (miss + t + 10*tt**3)/mx*100

    def random_population(self, population_size: int):
        solution = []
        for i in range(1, self.puzzle.max_num + 1):
            if i not in self.puzzle.fixed_nums:
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
        for i in range(1, self.puzzle.max_num):
            if self.puzzle.pairwise_distances[self.puzzle.find_coordinates(i), self.puzzle.find_coordinates(i + 1)] != 1:
                return False
        for cell1, cell2 in self.puzzle.dots:
            if not self.puzzle.is_successor(cell1, cell2):
                return False
        return True


with open('input1.txt') as f:
    puzzle = Puzzle.parse(f.read())

behaviour = Behaviour(puzzle)

"""
good_gene = Gene([31, 12, 29, 32, 13, 10, 9, 33, 14, 16, 8, 27, 34, 17, 7, 25, 35, 18, 24, 2, 4, 22, 21, 20], 0)
bad_gene = Gene([31, 12, 29, 32, 13, 14, 10, 33, 34, 9, 8, 27, 35, 16, 7, 25, 18, 17, 24, 2, 4, 22, 21, 20], 0)
puzzle.set_empty_cells(bad_gene.values)
print(behaviour.objective(bad_gene.values))
draw_puzzle(str(puzzle), behaviour.puzzle.empty_cells)
"""

model = GeneticAlgorithmModel(behaviour, 1000, 0.1, 2)
objective_values = model.fit(300, metrics=['best_objective'])  # 'mutates', 'crossovers', ...
best_solution = model.best_solution()
puzzle.set_empty_cells(best_solution.values)
draw_puzzle(str(puzzle), behaviour.puzzle.empty_cells, objective_values)
