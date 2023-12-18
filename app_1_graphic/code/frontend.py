import tkinter as tk
from matplotlib.figure import Figure
import AGenLibrary
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

MATRIX_IN=  [[1,2,3],[2,1,3],[1,2,3]]
MAX_ITERATION=300

n=len(MATRIX_IN)
m=len(MATRIX_IN[0])

class PlottingApp:
    def __init__(self, master):
        self.master = master

        self.button = tk.Button(self.master, text="Rysuj wykres", command=self.draw_plot)
        self.button.place(x=220, y=10, width=100, height=25)

        self.button_clear = tk.Button(self.master, text="Wyczyść wykres", command=self.clear_plot)
        self.button_clear.place(x=350, y=10, width=100, height=25)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().place(x=200, y=50, width=480, height=360)


    def clear_plot(self):
        self.plot.cla()
        self.canvas.draw()

    def draw_plot(self):
        x = AGenLibrary.list_x
        y = AGenLibrary.list_y
        try:
            self.plot.plot(x, y)
            self.canvas.draw()
        except Exception as e:
            print(e)

class LabelManager:
    def __init__(self, master,matrix_in):
        self.master = master

        self.label_p = tk.Label(master, text="P")
        self.label_pc = tk.Label(master, text="PC")
        self.label_pm = tk.Label(master, text="PM")
        self.label_ps = tk.Label(master, text="PS")
        self.label_limit=tk.Label(master,text="Limit w grupach")
        self.label_iter = tk.Label(master, text="Podaj liczbę iteracji")
        self.label_legenda = tk.Label(master,
                                      text="P - Liczność populacji - domyślnie 100,\n"
                                           "PC - Liczba od 0 do 1 definiująca ile procent całej populacji należy do elity, - domyślnie 0.2\n"
                                           "PM - Liczba od 0 do 1 definiująca ile procent całej populacji ulegnie mutacji - domyślnie 0.01,\n"
                                           "PS - Liczba od 0 do 1 definiująca ile chromosomów danego osobnika ulegnie mutacji - domyślnie 0.05",
                                      font=("Arial", 12),
                                      justify=tk.LEFT)
        self.label_matrix_in=tk.Label(master,text='\n'.join(['\t'.join(map(str, row)) for row in matrix_in]))
        self.label_matrix_description = tk.Label(master, text="Macierz preferencji studentów:")
        self.label_n = tk.Label(master, text="Liczba wierszy")
        self.label_m = tk.Label(master, text="Liczba kolumn")


    def update_matrix_label(self, new_matrix):
        new_text = '\n'.join(['\t'.join(map(str, row)) for row in new_matrix])
        self.label_matrix_in.config(text=new_text)


    def place_labels(self):
        self.label_p.place(x=20, y=180)
        self.label_pc.place(x=20, y=230)
        self.label_pm.place(x=20, y=280)
        self.label_ps.place(x=20, y=330)
        self.label_iter.place(x=20, y=380)
        self.label_limit.place(x=20,y=430)
        self.label_legenda.place(x=20, y=480)
        self.label_matrix_in.place(x=750, y=100)
        self.label_matrix_description.place(x=750, y=20)
        self.label_n.place(x=950, y=20)
        self.label_m.place(x=1150, y=20)
class ButtonManager:
    def __init__(self, master, start_action, stop_action, update_action,entry_manager_instance,label_manager_instance,limits):
        self.master = master
        self.label_manager=label_manager_instance
        self.entry_manager=entry_manager_instance
        self.start_button = tk.Button(master, text="Start", command=start_action)
        self.stop_button = tk.Button(master, text="Stop", command=stop_action)
        self.update_button = tk.Button(master, text="Wprowadź dane", command=lambda: update_action(self.entry_manager))
        self.create_matrix_button = tk.Button(master, text="Wygeneruj preferencje studentów", command=lambda:create_preference_matrix(self.label_manager))
        self.condition1_button=tk.Button(master,text="Warunek wykluczający przedmioty",command=lambda:limits(m))
        #self.condition2_button = tk.Button(master, text="Warunek łączący przedmioty", command=condition2)

    def place_buttons(self):
        self.start_button.place(x=10, y=10, width=100, height=25)
        self.stop_button.place(x=10, y=40, width=100, height=25)
        self.update_button.place(x=10, y=150, width=100, height=25)
        self.create_matrix_button.place(x=500, y=10, width=200, height=25)
        self.condition1_button.place(x=20, y=600,width=200,height=25)
        #self.condition2_button.place(x=20, y=650, width=200, height=25)

def create_preference_matrix(label_manager, rows=None,columns=None,):
    global n, m
    if rows is None:
        rows = n
    if columns is None:
        columns = m
    matrix = [0 for _ in range(rows)]
    for i in range(rows):
        matrix[i]=random.sample(range(1,columns+1),columns)
    global MATRIX_IN
    MATRIX_IN=matrix
    label_manager.update_matrix_label(matrix)

class EntryManager:
    def __init__(self, master):
        self.master = master
        self.entries = {}

        # Tworzenie pól Entry
        self.entries['p'] = tk.Entry(master)
        self.entries['pc'] = tk.Entry(master)
        self.entries['pm'] = tk.Entry(master)
        self.entries['ps'] = tk.Entry(master)
        self.entries['limit']=tk.Entry(master)
        self.entries['iter'] = tk.Entry(master)
        self.entries['n'] = tk.Entry(master)
        self.entries['m'] = tk.Entry(master)

        # Rozmieszczanie pól Entry
        self.entries['p'].place(x=10, y=200, width=100, height=25)
        self.entries['pc'].place(x=10, y=250, width=100, height=25)
        self.entries['pm'].place(x=10, y=300, width=100, height=25)
        self.entries['ps'].place(x=10, y=350, width=100, height=25)
        self.entries['iter'].place(x=10, y=400, width=100, height=25)
        self.entries['limit'].place(x=10,y=450,width=100,height=25)
        self.entries['n'].place(x=950, y=50, width=100, height=25)
        self.entries['m'].place(x=1150, y=50, width=100, height=25)

    def get_values(self):
        # Pobieranie wartości z pól Entry
        return {key: entry.get() for key, entry in self.entries.items()}


