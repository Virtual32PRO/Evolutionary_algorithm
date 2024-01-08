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
list_of_students=[i for i in range(AGenLibrary.n)]


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

def limits_in_groups(n,m):
    return [randint(round(n/2),n) for _ in range(m)]

limit=limits_in_groups(AGenLibrary.n,AGenLibrary.m)


def podziel_uczniow(uczniowie):
    uczniowie.sort()
    liczba_uczniow = len(uczniowie)
    limit_osob_w_grupie = 15

    liczba_grup = (liczba_uczniow + limit_osob_w_grupie - 1) // limit_osob_w_grupie
    grupy = [[] for _ in range(liczba_grup)]

    for i, uczen in enumerate(uczniowie):
        grupy[i % liczba_grup].append(uczen)

    return grupy,liczba_grup



groups,number_of_groups=podziel_uczniow(list_of_students)

def create_schedule(m):
    matrix=np.zeros((5,50))
    for i in range (m):
        while True:
            start_hour=randint(1,42)
            start_day=randint(0,4)
            if not(matrix[start_day][start_hour-1] == 1 or matrix[start_day][start_hour + 7] == 1):
                for j in range(start_hour, start_hour + 6):
                    matrix[start_day][j]=1
                break
    matrix=np.transpose(matrix)
    return matrix

def for_all_groups_basic(number,m):
    schedule=[]
    for i in range(number):
        schedule.append(create_schedule(m))
    return schedule

basic_schedule=for_all_groups_basic(number_of_groups,AGenLibrary.m)

def obieraki_plan(limit,m):
    liczba_grup=[]
    obieraki=[]
    obieraki_schedule=[]
    for j in limit:
        liczba_grup.append((j + 15 - 1) // 15)
    for i in liczba_grup:
        obieraki=create_schedule(i)
        obieraki_schedule.append(obieraki)
    return obieraki_schedule,liczba_grup

obieraki_schedule,liczba_grup=obieraki_plan(limit,AGenLibrary.m)

def assign_groups_for_obieraki(m):
    global obieraki_schedule
    podzial=[]
    for i in range(m):
        macierz=obieraki_schedule[i]
        macierz = np.array(list(macierz))
        macierz = np.transpose(macierz)
        poczatki_grup = []
        grupy = {}

        for wiersz_idx, wiersz in enumerate(macierz):
            wiersz_logiczny = wiersz == 1
            indeksy_grup = np.where(np.convolve(wiersz_logiczny, [1] * 6, mode='valid') == 6)[0]
            for indeks in indeksy_grup:
                poczatki_grup.append((wiersz_idx, indeks))

        licznik = 1
        for adres in poczatki_grup:
            grupy[licznik] = adres
            licznik += 1
        podzial.append(grupy)

    return podzial

podzial=assign_groups_for_obieraki(AGenLibrary.m)

def check_time(m):
    global basic_schedule
    global podzial
    all=[]
    for k in range(m):
        macierz=basic_schedule[k]
        matrix = []
        for index, slownik in enumerate(podzial):
            ids = []
            for key, adres in slownik.items():
                i, j = adres
                if 0 <= i < len(macierz) and 0 <= j < len(macierz[0]) and (macierz[i][j] == 1 or macierz[i+6][j]==1):
                    ids.append(key)
            matrix.append(ids)
        all.append(matrix)
    return all

excluded_groups=check_time(AGenLibrary.m)

def limit_for_time(m):
    global excluded_groups
    global groups
    numery_grup=[]
    for i in range(m):
        for wiersz in groups:
            if i in wiersz:
                numery_grup.append(wiersz)
    return numery_grup


limit_for_time_=limit_for_time(AGenLibrary.m)
    

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



def random_matrix_for_schedule(matrix,m,n):
    """Funkcja odpowiedzialna za towrzenie macierzy dla harmonagramu"""
    global liczba_grup
    for i in range(n):
        for j in range(m):
            if matrix[i][j]==1:
                matrix[i][j]=randint(1,liczba_grup[j])
    return matrix

def check_limits_for_schedule(matrix,m):
    global liczba_grup
    matrix=np.array(list(matrix))
    matrix=np.transpose(matrix)
    for i in range(m):
        for j in range(1,liczba_grup[i]+1):
            x=np.count_nonzero(matrix[i]==j)
            if x>15 or x<6:
                return 1
            else:
                return 0


def first_population_generator_for_schedule(matrix,num_of_student,num_of_subject):
    """Funkcja odpowiadająca za generację populacji początkowej dla harmonorgamu"""
    return [Harmongram(random_matrix_for_schedule(matrix,num_of_subject,num_of_student)) for _ in range(p)]





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
    global bad_address, good_address ,limit,list_of_students,groups, number_of_groups,basic_schedule ,obieraki_schedule,podzial,excluded_groups,limit_for_time_
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
        if values['m'] or values['n']:
            bad_address, good_address = limits(AGenLibrary.m)
            limit=limits_in_groups(AGenLibrary.n,AGenLibrary.m)
            list_of_students = [i for i in range(AGenLibrary.n)]
            groups, number_of_groups = podziel_uczniow(list_of_students)
            basic_schedule = for_all_groups_basic(number_of_groups,AGenLibrary.m)
            obieraki_schedule,liczba_grup=obieraki_plan(limit,AGenLibrary.m)
            podzial = assign_groups_for_obieraki(AGenLibrary.m)
            excluded_groups = check_time(AGenLibrary.m)
            limit_for_time_ = limit_for_time(AGenLibrary.m)
    except ValueError as e:
        print("Wprowadzono nieprawidłowe dane:", e)
def start():
    """Funkcja odpowiedzialna za start algorytmu"""
    AGenLibrary.is_running = True
    threading.Thread(target=genetic_algorithm.run).start()

def stop():
    """Funkcja odpowiedzialna za zatrzymanie algorytmu"""
    AGenLibrary.is_running = False

#Harmongram

class Harmonogram(Element):
    def __init__(self,matrix):
        self.matrix = matrix
        self.n=len(matrix)
        self.m=len(matrix[0])
        super().__init__()

    def __repr__(self):
        """Reprezentacja przydziału"""
        return str(self.matrix)



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
        if any(element > l for element, l in zip(columns_sum, limit)):
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
        mutation_probability=pm,
        first_population_generator_for_schedule=first_population_generator_for_schedule
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


