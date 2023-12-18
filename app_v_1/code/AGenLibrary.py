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


def excluded_subjects(m):
    verse = [0 for _ in range(m)]
    address = sample(range(m), 2)
    for i in address:
        verse[i] = 1
    return address

def generate_binary_list(length, forbidden_positions):
    ones_count = 3
    allowed_positions = [i for i in range(length) if i not in forbidden_positions]

    if len(allowed_positions) < ones_count:
        raise ValueError("Zbyt mało dostępnych pozycji dla jednynek.")

    random_ones_positions = sample(allowed_positions, ones_count)
    binary_list = [1 if i in random_ones_positions else 0 for i in range(length)]

    return binary_list

def check_bad_subject_limits(matrix,address):
    m=len(matrix[0])
    for i,wiersz in enumerate(matrix):
        if all(wiersz[i] == 1 for i in address):
            new_row=generate_binary_list(m,address)
            matrix[i]=new_row

    return matrix

def check_good_subject_limits(matrix,address):
    for wiersz in matrix:
        if any(all(wiersz[j] == 1 for j in id) for id in address):
            return 1
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
        j=1
        while j !=0:
            bad_subjects=excluded_subjects(m)
            good_subjects=excluded_subjects(m)
            if bad_subjects==good_subjects:
                good_subjects=excluded_subjects(m)
            else:
                j-=1

        print("Przedmioty wykluczające się :",bad_subjects)
        print("Przedmioty, które muszą być razem: ",good_subjects)

        while True:
            selected = self.selection_model(population)
            new_population = selected.copy()
            while len(new_population) != population_len:
                child = choice(population).crossover(choice(population))
                if random() <= self.mutation_probability:
                    child.mutation()
                child.matrix=check_bad_subject_limits(child.matrix,bad_subjects)
                if check_group_limits(child.matrix, limit) == 0:
                    new_population.append(child)


            population = new_population
            the_best_match = max(population, key=lambda x: x.fitness)
            print("Matrix: {} S: {} fitness: {}".format(i, the_best_match, the_best_match.fitness))
            i += 1
            if self.stop_condition(i):
                break



