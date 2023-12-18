from AGenLibrary import Element, GeneticAlgorithm
from random import sample, randint
import numpy as np

#Parameters
p = 100  # population size
pc = 0.2  # elite percentage
pm = 0.01  # mutations
ps = 0.05  # mutation severity
n=80   #liczba studentów
m= 8   #liczba przedmiotów
limit=70 # limit osoób na przedmiocie


#MATRIX_IN=[[2, 3, 5, 4, 1],[4, 1, 5, 2, 3],[1, 5, 3, 4, 2],[3, 2, 4, 1, 5],[5, 4, 1, 3, 2],[2, 4, 3, 5, 1],[1, 3, 4, 2, 5],[5, 1, 4, 3, 2]]
MATRIX_IN= [[3, 2, 4, 7, 6, 5, 1, 8], [2, 8, 7, 1, 5, 4, 3, 6], [2, 4, 8, 1, 5, 3, 6, 7], [8, 1, 2, 6, 5, 3, 7, 4], [2, 7, 1, 8, 5, 6, 3, 4], [5, 6, 8, 1, 3, 4, 7, 2], [6, 4, 1, 8, 7, 2, 5, 3], [1, 5, 2, 7, 3, 6, 8, 4], [4, 2, 7, 1, 8, 6, 5, 3], [2, 7, 1, 5, 3, 4, 8, 6], [1, 2, 6, 5, 3, 4, 8, 7], [3, 6, 5, 2, 4, 1, 7, 8], [7, 1, 4, 6, 3, 5, 2, 8], [8, 2, 7, 1, 6, 3, 4, 5], [3, 2, 7, 6, 8, 4, 1, 5], [5, 7, 3, 8, 4, 2, 6, 1], [5, 1, 7, 4, 6, 3, 8, 2], [8, 3, 7, 1, 5, 2, 6, 4], [7, 2, 4, 5, 6, 3, 1, 8], [6, 5, 7, 2, 1, 8, 4, 3], [7, 5, 8, 6, 1, 2, 3, 4], [6, 7, 5, 2, 1, 8, 3, 4], [3, 2, 5, 7, 6, 4, 8, 1], [4, 7, 1, 2, 3, 5, 8, 6], [5, 7, 1, 4, 3, 8, 2, 6], [4, 3, 1, 2, 7, 8, 6, 5], [1, 2, 5, 8, 7, 6, 3, 4], [6, 3, 1, 4, 5, 7, 2, 8], [2, 1, 6, 3, 5, 4, 8, 7], [8, 7, 3, 5, 2, 6, 4, 1], [4, 1, 5, 7, 3, 6, 8, 2], [6, 5, 3, 8, 7, 1, 4, 2], [3, 5, 7, 1, 6, 4, 8, 2], [7, 5, 4, 3, 8, 1, 2, 6], [8, 1, 4, 2, 7, 6, 3, 5], [4, 2, 7, 8, 6, 1, 3, 5], [1, 6, 8, 7, 5, 3, 4, 2], [5, 7, 2, 1, 6, 4, 8, 3], [4, 8, 6, 5, 7, 1, 2, 3], [3, 5, 7, 1, 6, 2, 8, 4], [4, 3, 6, 7, 1, 5, 2, 8], [5, 7, 1, 2, 6, 8, 3, 4], [4, 1, 7, 5, 3, 8, 2, 6], [6, 7, 1, 3, 5, 4, 2, 8], [2, 3, 1, 8, 7, 4, 6, 5], [2, 8, 1, 7, 3, 4, 5, 6], [3, 6, 4, 1, 2, 7, 5, 8], [2, 1, 3, 8, 5, 7, 6, 4], [2, 4, 8, 1, 6, 7, 5, 3], [5, 1, 4, 8, 2, 7, 6, 3], [2, 8, 4, 1, 7, 3, 6, 5], [3, 4, 2, 7, 1, 6, 8, 5], [3, 2, 8, 7, 6, 1, 5, 4], [3, 5, 1, 8, 4, 7, 2, 6], [2, 7, 8, 1, 6, 5, 3, 4], [2, 4, 1, 5, 6, 7, 8, 3], [8, 1, 4, 3, 5, 6, 7, 2], [3, 8, 5, 4, 6, 1, 7, 2], [5, 4, 8, 2, 3, 6, 7, 1], [4, 6, 5, 2, 8, 3, 1, 7], [7, 8, 5, 1, 4, 3, 6, 2], [6, 5, 7, 2, 3, 8, 4, 1], [4, 2, 7, 8, 3, 5, 6, 1], [8, 6, 3, 5, 7, 4, 2, 1], [3, 6, 8, 2, 7, 1, 4, 5], [6, 2, 4, 8, 5, 1, 3, 7], [2, 6, 7, 3, 5, 4, 8, 1], [1, 2, 3, 6, 8, 7, 4, 5], [4, 2, 3, 5, 1, 7, 6, 8], [6, 1, 2, 7, 3, 5, 4, 8], [4, 2, 6, 3, 8, 7, 1, 5], [2, 7, 5, 3, 4, 8, 1, 6], [4, 7, 8, 2, 1, 6, 3, 5], [2, 8, 7, 4, 1, 3, 6, 5], [8, 7, 3, 4, 5, 6, 2, 1], [6, 1, 2, 7, 3, 4, 8, 5], [8, 3, 7, 2, 4, 1, 5, 6], [6, 1, 4, 8, 5, 2, 7, 3], [6, 4, 7, 2, 1, 8, 5, 3], [6, 5, 4, 2, 3, 1, 7, 8]]
MAX_ITERATION=100

def excluded_subjects(m):
    verse = [0 for _ in range(m)]
    address = sample(range(m), 2)
    for i in address:
        verse[i] = 1
    return address


def limit(m):
    j = 1
    bad_subjects=[]
    good_subjects=[]
    while j != 0:
        bad_subjects = excluded_subjects(m)
        good_subjects = excluded_subjects(m)
        if bad_subjects == good_subjects:
            good_subjects = excluded_subjects(m)
        else:
            j -= 1
    return bad_subjects,good_subjects

bad_address,good_address=limit(m)

def create_matrix_in(n,m):
    matrix = [0 for _ in range(m) for _ in range(n)]
    for i in range(n):
        matrix[i]=sample(range(1,m+1),m)
    return matrix

def elite_selection_model(generation):
    max_selected = int(len(generation) * pc)
    sorted_by_assess = sorted(generation, key=lambda x: -x.fitness)
    return sorted_by_assess[:max_selected]

def stop_condition(iteration):
    return iteration==MAX_ITERATION

def first_population_generator():
    return [ScheduleMatrix(create_matrix(n,m,good_address,bad_address)) for _ in range(p)]

def create_matrix(n, m,good_address,bad_address):
    matrix = []
    for _ in range(n):
        verse=random_verse(m,good_address,bad_address)
        matrix.append(verse)
    return matrix

def random_verse(m,good_address,bad_address):
    i=1
    b1=bad_address[0]
    b2=bad_address[1]
    g1=good_address[0]
    g2=good_address[1]
    verse = [0 for _ in range(m)]
    address=[]
    while i!=0:
        address = sample(range(m), 3)
        if not(b1 in address and b2 in address) and not((g1 in address) ^ (g2 in address)) :
            i = i - 1
    for i in address:
        verse[i] = 1
    return verse



def create_mask(n):
    return [randint(0,1) for _ in range(n)]




class ScheduleMatrix(Element):

    def __init__(self, matrix):
        self.matrix = matrix
        self.n=len(matrix)
        self.m=len(matrix[0])
        super().__init__()





    def _perform_mutation(self):
        for _ in range(int(ps*n)):
            random_index = randint(0, n-1)
            self.matrix[random_index]=random_verse(m,good_address,bad_address)


    def crossover(self, element2: 'Element' ) -> 'Element':
        mask=create_mask(self.n)
        child=[]
        for i in range(self.n):
            decision=mask[i]
            if decision ==1:
                child.append(self.matrix[i])
            else:
                child.append(element2.matrix[i])
        return ScheduleMatrix(child)




    def evaluate_function(self):
        matrix1 = np.array(self.matrix)
        matrix2 = np.array(MATRIX_IN)
        product = np.multiply(matrix1, matrix2)
        return np.sum(product)


    def __repr__(self):
        return str(self.matrix)



if __name__ == "__main__":
    genetic_algorithm = GeneticAlgorithm(
        first_population_generator=first_population_generator,
        selection_model=elite_selection_model,
        stop_condition=stop_condition,
        mutation_probability=pm
    )

    genetic_algorithm.run()
    print(bad_address,good_address)