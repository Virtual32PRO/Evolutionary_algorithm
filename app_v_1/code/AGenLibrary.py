from abc import abstractmethod, ABC
from random import random, choice
import numpy as np
from random import sample, randint

p = 100  # population size
pc = 0.2  # elite percentage
pm = 0.01  # mutations
ps = 0.05  # mutation severity
n=80   #liczba studentów
m= 8  #liczba przedmiotów
limit=80 # limit osoób na przedmiocie



def check_group_limits(matrix, limit):
    matrix=np.array(list(matrix))
    matrix = np.transpose(matrix)
    columns_sum = [sum(kolumna) for kolumna in matrix]
    if any(element > limit for element in columns_sum):
        return 1
    else:
        return 0




class Element(ABC):

    def __init__(self):
        self.fitness = self.evaluate_function()

    def mutation(self):
        self._perform_mutation()
        self.fitness = self.evaluate_function()

    @abstractmethod
    def _perform_mutation(self):
        pass

    @abstractmethod
    def crossover(self, element2: 'Element' ) -> 'Element':
        pass



    @abstractmethod
    def evaluate_function(self):
        pass

class GeneticAlgorithm:

    def __init__(self, first_population_generator: callable,
                 selection_model: callable, stop_condition: callable, mutation_probability: float = 0.1):
        self.first_generation_func = first_population_generator
        self.selection_model = selection_model
        self.stop_condition = stop_condition
        self.mutation_probability = mutation_probability



    def run(self):
        population = self.first_generation_func()
        population.sort(key=lambda x: -x.fitness)
        population_len = len(population)
        i = 0


        while True:
            selected = self.selection_model(population)
            new_population = selected.copy()
            while len(new_population) != population_len:
                child = choice(population).crossover(choice(population))
                if random() <= self.mutation_probability:
                    child.mutation()
                if check_group_limits(child.matrix, limit) == 0:
                    new_population.append(child)


            population = new_population
            the_best_match = max(population, key=lambda x: x.fitness)
            print("Matrix: {} S: {} fitness: {}".format(i, the_best_match, the_best_match.fitness))
            i += 1
            if self.stop_condition(i):
                break



