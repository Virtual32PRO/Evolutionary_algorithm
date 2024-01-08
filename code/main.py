import tkinter as tk
import threading
from AGenLibrary import Element, GeneticAlgorithm
from random import sample, randint
import random
import numpy as np
import AGenLibrary
from frontend import PlottingApp, LabelManager, ButtonManager, EntryManager
from ReloadFront import Reload
from InformationFront import Information
from InstructionFront import Instruction
from WelcomeFront import Welcome
from PIL import Image, ImageTk


#Parameters
p = 100  # population size
pc = 0.2  # elite percentage
ps = 0.05  # mutation severity
pm = 0.01  # mutations
limit = 50 #limit w grupach


#limits section
def excluded_subjects(num_of_subject):
    """Funkcja generująca dwa adresy """
    address = sample(range(num_of_subject), 2)
    return address


def limits(num_of_subject):
    """Funkcja generująca adresy przedmiotów wspierających się i przemiotów zabronionych"""
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

def roulette_wheel_selection_model(generation):
    num_of_parents = int(len(generation) * pc)
    sorted_by_assess = sorted(generation, key=lambda x: -x.fitness)
    num_of_element = len(generation)
    weight_list = []
    sum=0
    for iter in  sorted_by_assess:
        sum=sum+iter.fitness
    for iter in range(num_of_element):
        element= sorted_by_assess[iter]
        weight_list.append(element.fitness/sum)
    selected_parent = random.choices(sorted_by_assess, weights=weight_list, k=num_of_parents)
    return selected_parent

def tournament_selection_model(generation):
    pass

def rank_selection_model(generation):
    num_of_parents = int(len(generation) * pc)
    sorted_by_assess = sorted(generation, key=lambda x: -x.fitness)
    num_of_element = len(generation)
    weight_of_last_element = 0.05
    weight_of_first_element = (200 / num_of_element) - weight_of_last_element
    difference = (weight_of_last_element - weight_of_first_element) / (num_of_element - 1)
    weight_list = []
    for iter in range(num_of_element):
        weight_list.append((weight_of_first_element + (iter - 1) * difference))
    selected_parent = random.choices(sorted_by_assess, weights=weight_list, k=num_of_parents)
    return selected_parent


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
        if values['probability_elite']:
            genetic_algorithm.update_variables_elite(float(values['probability_elite']))
        if values['probability_rank']:
            genetic_algorithm.update_variables_rank(float(values['probability_rank']))
        if values['probability_roulette']:
            genetic_algorithm.update_variables_roulette(float(values['probability_roulette']))
        if values['probability_tournament']:
            genetic_algorithm.update_variables_tournament(float(values['probability_tournament']))

    except ValueError as e:
        print("Wprowadzono nieprawidłowe dane:", e)
def start():
    """Funkcja odpowiedzialna za start algorytmu"""
    AGenLibrary.is_running = True
    reload = Reload(window, reload_action)
    threading.Thread(target=genetic_algorithm.run).start()
    window.after(0, lambda: show_frame(reload.frame))

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
        """Metoda sprawdzająca czy ScheduleMatrix należy do grupy rozwiązań dozwolonych"""
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

def show_frame(frame):
    frame.tkraise()
def reload_action():
    stop()
    show_frame(main_frame)
if __name__ == "__main__":
    genetic_algorithm = GeneticAlgorithm(
        first_population_generator=first_population_generator,
        selection_model=[rank_selection_model, elite_selection_model, roulette_wheel_selection_model],
        #selection_model=elite_selection_model,
        stop_condition=stop_condition,
        mutation_probability=pm,
        weight_elite=0.5,
        weight_roulette=0.5
    )
    window = tk.Tk()
    window.title("Evolutionary Algorithm")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}+0+0")

    #utworzenie ramki głównej
    main_frame = tk.Frame(window)
    main_frame.place(relwidth=1, relheight=1)

    #wczytanie obrazu dla ramki głównej
    img = Image.open('obraz6.png')
    resized_img = img.resize((1600, 800), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_img)
    background_label = tk.Label(main_frame, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    #inicjalizacja ramek
    instruction = Instruction(window, lambda: show_frame(welcome_page.frame))
    information = Information(window, lambda: show_frame(welcome_page.frame))
    welcome_page = Welcome(window,
                           lambda: show_frame(main_frame),
                           lambda: show_frame(instruction.frame),
                           lambda: show_frame(information.frame))

    #zarządzanie interfacem badawczym
    app = PlottingApp(main_frame)

    label_manager = LabelManager(main_frame, AGenLibrary.MATRIX_IN)
    label_manager.place_labels()

    entry_manager = EntryManager(main_frame)
    update_variables(entry_manager)

    button_manager = ButtonManager(main_frame, start, stop, update_variables,entry_manager,label_manager,show_frame,welcome_page)
    button_manager.place_buttons()

    welcome_page.show()
    window.mainloop()

