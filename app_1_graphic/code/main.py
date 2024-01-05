import tkinter as tk
import threading
from AGenLibrary import Element, GeneticAlgorithm
from random import sample, randint
import numpy as np
import AGenLibrary
from frontend import PlottingApp, LabelManager,ButtonManager,EntryManager
import frontend

#Parameters
p = 100  # population size
pc = 0.2  # elite percentage
pm = 0.01  # mutations
ps = 0.05  # mutation severity
limit = 50 #limit w grupach



#general codes section

def excluded_subjects(m):
    verse = [0 for _ in range(m)]
    address = sample(range(m), 2)
    for i in address:
        verse[i] = 1
    return address


def limits(m):
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

    bad_address=bad_subjects
    good_address=good_subjects
    return bad_address,good_address

bad_address,good_address=limits(frontend.m)




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
    return iteration==frontend.MAX_ITERATION

def first_population_generator():
    return [ScheduleMatrix(create_matrix(frontend.n,frontend.m)) for _ in range(p)]

def create_matrix(n, m):
    global good_address,bad_address
    matrix = []
    for _ in range(n):
        verse=random_verse(m)
        matrix.append(verse)
    return matrix
def random_verse(m):
    global bad_address,good_address
    i=1
    b1=bad_address[0]
    b2=bad_address[1]
    g1=good_address[0]
    g2=good_address[1]
    verse = [0 for _ in range(m)]
    address=[]
    while i!=0:
        address = sample(range(m), 3)
        if not(b1 in address and b2 in address) and not((g1 in address) ^ (g2 in address)):
            i = i - 1
    for i in address:
        verse[i] = 1
    return verse

def create_mask(n):
    return [randint(0,1) for _ in range(n)]

def update_variables(entry_manager):
    global p, pc, pm, ps,limit

    values = entry_manager.get_values()

    try:
        if values['p']:
            p = int(values['p'])
        if values['pc']:
            pc = float(values['pc'])
        if values['pm']:
            pm = float(values['pm'])
        if values['ps']:
            ps = float(values['ps'])
        if values['limit']:
            limit=int(values['limit'])
        if values['iter']:
            frontend.MAX_ITERATION = int(values['iter'])
        if values['n']:
            frontend.n = int(values['n'])
        if values['m']:
            frontend.m = int(values['m'])
    except ValueError as e:
        print("Wprowadzono nieprawidłowe dane:", e)
def start():

    AGenLibrary.is_running = True
    threading.Thread(target=genetic_algorithm.run).start()

def stop():

    AGenLibrary.is_running = False

class ScheduleMatrix(Element):

    def __init__(self, matrix):
        self.matrix = matrix
        self.n=len(matrix)
        self.m=len(matrix[0])
        super().__init__()

    def _perform_mutation(self):
        for _ in range(int(ps*self.n)):
            random_index = randint(0, self.n-1)
            self.matrix[random_index]=random_verse(self.m)


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

    def check_group_limits(self):
        matrix = np.array(list(self.matrix))
        matrix = np.transpose(matrix)
        columns_sum = [sum(kolumna) for kolumna in matrix]
        if any(element > limit for element in columns_sum):
            return 1
        else:
            return 0


    def evaluate_function(self):
        matrix1 = np.array(self.matrix)
        matrix2 = np.array(frontend.MATRIX_IN)
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
    window = tk.Tk()
    window.title("Evolutionary Algorithm")
    window.geometry("1300x700")

    app = PlottingApp(window)

    label_manager = LabelManager(window,frontend.MATRIX_IN)
    label_manager.place_labels()

    entry_manager = EntryManager(window)
    values = entry_manager.get_values()
    update_variables(entry_manager)

    button_manager = ButtonManager(window, start, stop, update_variables,entry_manager,label_manager,limits)
    button_manager.place_buttons()

    window.mainloop()


