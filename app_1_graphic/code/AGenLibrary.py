from abc import abstractmethod, ABC
from random import random, choice

is_running = False
list_x = []
list_y = []

MATRIX_IN=  [[1,2,3],[2,1,3],[1,2,3]]
MAX_ITERATION=300

n=len(MATRIX_IN)
m=len(MATRIX_IN[0])


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

    @abstractmethod
    def check_group_limits(self):
        pass

class GeneticAlgorithm:

    def __init__(self, first_population_generator: callable,
                 selection_model: callable, stop_condition: callable, mutation_probability: float = 0.1):
        self.first_generation_func = first_population_generator
        self.selection_model = selection_model
        self.stop_condition = stop_condition
        self.mutation_probability = mutation_probability


    def run(self):
        global n,m
        population = self.first_generation_func(n,m)
        population.sort(key=lambda x: -x.fitness)
        population_len = len(population)
        i = 0
        global list_x, list_y
        list_x=[]
        list_y=[]
        global is_running
        while  is_running:
            is_running = True
            selected = self.selection_model(population)
            new_population = selected.copy()
            while len(new_population) != population_len:
                child = choice(population).crossover(choice(population))
                if random() <= self.mutation_probability:
                    child.mutation()
                if child.check_group_limits() == 0:
                    new_population.append(child)
            population = new_population
            the_best_match = max(population, key=lambda x: x.fitness)
            list_x.append(i)
            list_y.append(the_best_match.fitness)
            print("Iteration number: {} Matrix: {} fitness: {}".format(i, the_best_match, the_best_match.fitness))
            i += 1
            if self.stop_condition(i):
                break






