from abc import abstractmethod, ABC
from random import choice
import random

is_running = False
list_x = []
list_y = []

MATRIX_IN=  [[1,2,3],[2,1,3],[1,2,3]]
MAX_ITERATION=300

n=len(MATRIX_IN)
m=len(MATRIX_IN[0])
num_of_iteration=0

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
                 selection_model: list, stop_condition: callable, mutation_probability: float = 0.1,
                 weight_elite: float=1, weight_rank: float=1, weight_roulette: float=1, weight_tournament: float=0):
        self.first_generation_func = first_population_generator
        self.selection_model = selection_model
        self.stop_condition = stop_condition
        self.mutation_probability = mutation_probability
        self.weight_elite = weight_elite
        self.weight_rank = weight_rank
        self.weight_roulette = weight_roulette
        self.weight_tournament = weight_tournament


    def run(self):
        global n,m
        population = self.first_generation_func(n,m)
        population.sort(key=lambda x: -x.fitness)
        population_len = len(population)
        i = 1
        global list_x, list_y
        list_x=[]
        list_y=[]
        global is_running
        while is_running:
            is_running = True
            strategy = random.choices(self.selection_model, weights=[self.weight_rank, self.weight_elite,
                                                                     self.weight_roulette], k=1)[0]
            selected = strategy(population)
            new_population = selected.copy()
            while len(new_population) != population_len:
                child = choice(population).crossover(choice(population))
                if random.random() <= self.mutation_probability:
                    child.mutation()
                if child.check_group_limits() == 0:
                    new_population.append(child)
            population = new_population
            the_best_match = max(population, key=lambda x: x.fitness)
            list_x.append(i)
            list_y.append(the_best_match.fitness)
            #print("Iteration number: {} Matrix: {} fitness: {}".format(i, the_best_match, the_best_match.fitness))
            global num_of_iteration
            num_of_iteration = i
            if self.stop_condition(i):
                break
            i += 1

    def update_variables_elite(self, new_weight_elite):
        self.weight_elite = new_weight_elite
    def update_variables_roulette(self, new_weight_roulette):
        self.weight_roulette = new_weight_roulette
    def update_variables_tournament(self, new_weight_tournament):
        self.weight_tournament = new_weight_tournament
    def update_variables_rank(self, new_weight_rank):
        self.weight_rank = new_weight_rank





