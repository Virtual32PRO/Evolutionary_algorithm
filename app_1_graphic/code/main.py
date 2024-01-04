import tkinter as tk
import threading
from AGenLibrary import Element, GeneticAlgorithm
from random import sample, randint
import numpy as np
import AGenLibrary
from frontend import PlottingApp, LabelManager,ButtonManager,EntryManager


#Parameters
p = 100  # population size
pc = 0.2  # elite percentage
pm = 0.01  # mutations
ps = 0.05  # mutation severity
limit = 50 #limit w grupach

#limits section
def excluded_subjects(num_of_subject):
    address = sample(range(num_of_subject), 2)
    return address


def limits(num_of_subject):
    bad_subjects = excluded_subjects(num_of_subject)
    good_subjects = excluded_subjects(num_of_subject)
    if bad_subjects == good_subjects:
        good_subjects = excluded_subjects(num_of_subject)
    return bad_subjects, good_subjects

bad_address, good_address = limits(AGenLibrary.m)

#general codes section

def elite_selection_model(generation):
    """Funkcja realizująca strategię elitarną"""
    max_selected = int(len(generation) * pc)
    sorted_by_assess = sorted(generation, key=lambda x: -x.fitness)
    return sorted_by_assess[:max_selected]

def stop_condition(iteration):
    """Funkcja realizująca warunek stopu poprzez liczbę iteracji"""
    return iteration==AGenLibrary.MAX_ITERATION

def first_population_generator(num_of_student,num_of_subject):
    """Funkcja odpowiadająca za generację populacji początkowej"""
    return [ScheduleMatrix(create_matrix(num_of_student,num_of_subject)) for _ in range(p)]

def create_matrix(n, m):
    """Funkcja odpowiedzialna za tworzenie macierzy wewnętrznej (binarnej)"""
    matrix = []
    for _ in range(n):
        verse=random_verse(m)
        matrix.append(verse)
    return matrix
def random_verse(m):
    """Funkcja odpowiedzialna za stworzenie wektora binarnego o sumie wartości pozycji równej 3"""
    global bad_address, good_address
    verse = [0 for _ in range(m)]
    address = sample(range(m), 3)
    if (bad_address[0] in address and bad_address[1] in address) or ((good_address[0] in address) ^ (good_address[1] in address)):
        address = sample(range(m), 3)
    for i in address:
        verse[i] = 1
    return verse

def create_mask(n):
    """Funkcja odpowiedzialna za stworzenie maski o rozmiarze n"""
    return [randint(0,1) for _ in range(n)]

#section responsible for control

def update_variables(entry_manager):
    """Funkcja odpowiedzialna za aktualizacje parametrów algorytmu"""
    global p, pc, pm, ps

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
        if values['iter']:
            AGenLibrary.MAX_ITERATION = int(values['iter'])
        if values['n']:
            AGenLibrary.n = int(values['n'])
        if values['m']:
            AGenLibrary.m = int(values['m'])
    except ValueError as e:
        print("Wprowadzono nieprawidłowe dane:", e)
def start():
    """Funkcja odpowiedzialna za start algorytmu"""
    AGenLibrary.is_running = True
    threading.Thread(target=genetic_algorithm.run).start()

def stop():
    """Funkcja odpowiedzialna za zatrzymanie algorytmu"""
    AGenLibrary.is_running = False

#Schedule Class

class ScheduleMatrix(Element):
    """Klasa reprezentująca pojedyńczy przydział przedmiotów do studentów"""
    def __init__(self, matrix):
        self.matrix = matrix
        self.n=len(matrix)
        self.m=len(matrix[0])
        super().__init__()

    def _perform_mutation(self):
        """Metoda odpowiedzialna za mutacje"""
        for _ in range(int(ps*self.n)):
            random_index = randint(0, self.n-1)
            self.matrix[random_index]=random_verse(self.m)


    def crossover(self, element2: 'ScheduleMatrix' ) -> 'ScheduleMatrix':
        """Metoda odpowiedzialna za krzyżowanie macierzy"""
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
        global limit
        if any(element > limit for element in columns_sum):
            return 1
        else:
            return 0

    def evaluate_function(self):
        """Metoda odpowiedzialna za wyznaczenie funkcji celu dla danego przydziału"""
        matrix1 = np.array(self.matrix)
        matrix2 = np.array(AGenLibrary.MATRIX_IN)
        product = np.multiply(matrix1, matrix2)
        return np.sum(product)


    def __repr__(self):
        """Reprezentacja przydziału"""
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

    label_manager = LabelManager(window, AGenLibrary.MATRIX_IN)
    label_manager.place_labels()

    entry_manager = EntryManager(window)
    update_variables(entry_manager)

    button_manager = ButtonManager(window, start, stop, update_variables,entry_manager,label_manager)
    button_manager.place_buttons()

    window.mainloop()

