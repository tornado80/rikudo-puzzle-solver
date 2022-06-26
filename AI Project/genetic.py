import random
from abc import ABC, abstractmethod
from typing import Callable, List, Any
import numpy as np


class Gene:
    def __init__(self, values: list, objective_val: float = 0):
        self.values = values
        self.objective_val = objective_val

    def copy(self):
        return Gene(self.values.copy(), self.objective_val)


class GeneticAlgorithmBehaviour(ABC):
    @abstractmethod
    def crossover(self, parent1: Gene, parent2: Gene):
        pass

    @abstractmethod
    def mutation(self, gene: Gene):
        pass

    @abstractmethod
    def is_goal(self, gene: Gene):
        pass

    @abstractmethod
    def random_population(self, population_size: int):
        pass


class GeneticAlgorithmModel:
    def __init__(self, behaviuor: GeneticAlgorithmBehaviour, population_size: int, crossover_coeff: float, mutation_coeff: float):
        self.__crossover_num = 0
        self.__mutation_num = 0
        self.__population_size: int = population_size
        self.population: list[Gene] = []
        self.objectives: list[float] = []
        self.__objectives_sum: float = 0
        self.__crossover_num = self.__population_size * crossover_coeff
        self.__mutation_num = self.__population_size * mutation_coeff
        self.__behaviour = behaviuor

    def __choose_weighted(self, k):
        objectives_sum = sum(self.objectives)
        return np.random.choice(
            self.population, size=k, replace=False,
            p=[u / objectives_sum for u in self.objectives])

    def __choose_best(self, k):
        l1 = self.population.copy()
        l1.sort(key=lambda e: e.objective_val)
        return l1[-k:]

    def extend(self, genes):
        self.population.extend(genes)
        self.objectives.extend([t.objective_val for t in genes])

    def remove(self, gene):
        i1 = self.population.index(gene)
        self.population.pop(i1)
        self.objectives.pop(i1)

    def __print_on_epoch(self, epoch, metrics):
        if not metrics:
            return
        print('Epoch #' + str(epoch) + ' -->', end='')
        if 'best_objective' in metrics:
            t = np.argmax(self.objectives)
            print(' best_objective_val=', self.objectives[t], end='')
            print(' ,best_objective=', self.population[t].values, end='')
        print('\n')

    def fit(self, epochs, metrics=None):
        epoch = 1
        self.population = self.__behaviour.random_population(self.__population_size)
        self.objectives = [t.objective_val for t in self.population]
        self.__print_on_epoch(0, metrics)
        best_objectives = []
        best_objectives.append(self.__choose_best(1)[0].objective_val)
        while epoch <= epochs:

            crossover_index = 0
            while crossover_index < self.__crossover_num:
                parent1, parent2 = self.__choose_weighted(2)
                child1, child2 = self.__behaviour.crossover(parent1.copy(), parent2.copy())
                self.extend([child1, child2])
                if metrics and 'crossovers' in metrics:
                    print(
                        f'Crossovering:\n  {parent1.values} \n  {parent2.values} \n  childs: \n  {child1.values} \n  {child2.values}')
                crossover_index += 2

            mutation_index = 0
            while mutation_index < self.__mutation_num:
                to_mutate = random.choice(self.population)
                mutated = self.__behaviour.mutation(to_mutate.copy())
                self.extend([mutated])
                if metrics and 'mutates' in metrics:
                    print(f'Mutating:\n  {to_mutate.values} \n  mutated: \n  {mutated.values}')
                mutation_index += 1

            self.population = self.__choose_best(self.__population_size)
            self.objectives = [t.objective_val for t in self.population]

            self.__print_on_epoch(epoch, metrics)
            best_gene = self.__choose_best(1)[0]
            best_objectives.append(best_gene.objective_val)
            if self.__behaviour.is_goal(best_gene):
                return best_objectives
            epoch += 1

        return best_objectives

    def best_solution(self):
        return self.__choose_best(1)[0]
