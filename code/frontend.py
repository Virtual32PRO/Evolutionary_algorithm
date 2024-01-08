import tkinter as tk
from matplotlib.figure import Figure
import AGenLibrary
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class PlottingApp:
    """Klasa reprezentująca wykres"""
    def __init__(self, master):
        self.master = master


        self.button = tk.Button(self.master, text="Rysuj wykres", command=self.draw_plot)
        self.button.place(x=220, y=40, width=100, height=25)

        self.button_clear = tk.Button(self.master, text="Wyczyść wykres", command=self.clear_plot)
        self.button_clear.place(x=350, y=40, width=100, height=25)

        self.fig = Figure(figsize=(7, 7), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().place(x=200, y=100, width=480, height=360)


    def clear_plot(self):
        """Metoda czyści canve"""
        self.plot.cla()
        self.canvas.draw()

    def draw_plot(self):
        """Metoda rysuje wykres"""
        x = AGenLibrary.list_x
        y = AGenLibrary.list_y
        try:
            self.plot.plot(x, y)
            self.canvas.draw()
        except Exception as e:
            print(e)

class LabelManager:
    """Klasa reprezentująca etykiety tekstowe aplikacji okienkowej"""
    def __init__(self, master, matrix_in):
        self.master = master

        self.label_p = tk.Label(master, text="P")
        self.label_pc = tk.Label(master, text="PC")
        self.label_pm = tk.Label(master, text="PM")
        self.label_ps = tk.Label(master, text="PS")
        self.label_iter = tk.Label(master, text="Podaj liczbę iteracji")
        self.label_legenda = tk.Label(master,
                                      text="P - Liczność populacji - domyślnie 100,\n"
                                           "PC - Liczba od 0 do 1 definiująca ile procent całej populacji należy do elity (w przypadku selekcji elitarnej)\n"
                                           "lub ile rodziców powstanie w procesie selekcji (pozostałe metody), - domyślnie 0.2\n"
                                           "PM - Liczba od 0 do 1 definiująca ile procent całej populacji ulegnie mutacji - domyślnie 0.01,\n"
                                           "PS - Liczba od 0 do 1 definiująca ile chromosomów danego osobnika ulegnie mutacji - domyślnie 0.05",
                                      font=("Arial", 12),
                                      justify=tk.LEFT)
        self.label_matrix_in='\n'.join(['\t'.join(map(str, row)) for row in matrix_in])
        self.label_matrix_description = tk.Label(master, text="Macierz preferencji studentów:")
        self.label_n = tk.Label(master, text="Liczba wierszy")
        self.label_m = tk.Label(master, text="Liczba kolumn")
        self.scrollable_label = self.create_scrollable_label(self.master, width=50, height=20)
        self.label_Probability_of_selection_model = tk.Label(master, text="Prawdopodobieństwo wyboru Metody selekcji")
        self.label_Probability_of_selection_elite = tk.Label(master, text="Prawdopodobieństwo wyboru selekcji Elitarnej")
        self.label_Probability_of_selection_rank = tk.Label(master, text="Prawdopodobieństwo wyboru selekcji Rankingowej")
        self.label_Probability_of_selection_roulette = tk.Label(master, text="Prawdopodobieństwo wyboru selekcji Ruletki")
        self.label_Probability_of_selection_tournament = tk.Label(master, text="Prawdopodobieństwo wyboru selekcji Turniejowej")
        self.test_matrix = tk.Label(master, text="Pobieranie Macierzy testowych\n będących w pliku test_matrix")



    def update_matrix_label(self, new_matrix):
        """ Metoda aktualizująca etykietę macierzy preferencji"""
        new_text = '\n'.join(['\t'.join(map(str, row)) for row in new_matrix])
        self.label_matrix_in=new_text
        self.update_scrollable_label()


    def place_labels(self):
        """Metoda odpowiadająca za rozmieszczenie etykiet w aplikacji okienkowej"""
        self.label_p.place(x=30, y=220)
        self.label_pc.place(x=30, y=280)
        self.label_pm.place(x=30, y=340)
        self.label_ps.place(x=30, y=400)
        self.label_iter.place(x=20, y=460)
        self.label_legenda.place(x=30, y=550)
        #self.label_matrix_in.place(x=800, y=130)
        self.scrollable_label.place(x=800, y=130)
        self.label_matrix_description.place(x=800, y=40)
        self.label_n.place(x=1050, y=40)
        self.label_m.place(x=1250, y=40)
        self.label_Probability_of_selection_model.place(x=1240, y=450)
        self.label_Probability_of_selection_elite.place(x=1240, y=500)
        self.label_Probability_of_selection_rank.place(x=1240, y=550)
        self.label_Probability_of_selection_roulette.place(x=1240, y=600)
        self.label_Probability_of_selection_tournament.place(x=1240, y=650)
        self.test_matrix.place(x=1270, y=200)

    def create_scrollable_label(self,parent, width, height):
        frame = tk.Frame(parent)
        text_widget = tk.Text(frame, wrap=tk.NONE, width=width, height=height)
        text_widget.insert(tk.END, self.label_matrix_in)
        text_widget.grid(row=0, column=0, sticky="nsew")

        # Suwak pionowy
        vscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        vscrollbar.grid(row=0, column=1, sticky="ns")

        # Suwak poziomy
        hscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text_widget.xview)
        hscrollbar.grid(row=1, column=0, sticky="ew")

        text_widget.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

        # Zablokowanie możliwości edycji tekstu
        text_widget.configure(state="disabled")

        return frame

    def update_scrollable_label(self):
        text_widget = self.scrollable_label.winfo_children()[0]
        text_widget.configure(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, self.label_matrix_in)
        text_widget.configure(state="disabled")

class ButtonManager:
    """Klasa odpowiedzialna za akcję w przypadku naciśnięcia przycisku"""
    def __init__(self, master, start_action, stop_action, update_action, entry_manager_instance, label_manager_instance,show_menu, welcome_page):
        self.master = master
        self.welcome_page=welcome_page
        self.label_manager=label_manager_instance
        self.entry_manager=entry_manager_instance
        self.start_button = tk.Button(master, text="Start", command=start_action)
        self.stop_button = tk.Button(master, text="Stop", command=stop_action)
        self.update_button = tk.Button(master, text="Wprowadź dane", command=lambda: update_action(self.entry_manager))
        self.create_matrix_button = tk.Button(master, text="Wygeneruj preferencje studentów", command=lambda:self._create_preference_matrix(self.label_manager, AGenLibrary.n, AGenLibrary.m))
        self.menu_button = tk.Button(master, text="Menu", bg='lightblue', fg='black', font=('Helvetica', 15, 'bold'), relief=tk.RAISED, borderwidth=2, command= lambda: show_menu(self.welcome_page.frame))
        self.test_matrix = tk.Button(master, text="Matrix_1_test", command=lambda: self._reload_matrix_txt("test_matrix.txt",self.label_manager))

    def place_buttons(self):
        """Metoda odpowiedzialna za rozmieszczenie przycisków"""
        self.start_button.place(x=20, y=40, width=100, height=25)
        self.stop_button.place(x=20, y=70, width=100, height=25)
        self.update_button.place(x=20, y=190, width=100, height=25)
        self.create_matrix_button.place(x=500, y=40, width=200, height=25)
        self.menu_button.place(x=80, y=670, width=220, height=37)
        self.test_matrix.place(x=1250, y=250, width=220, height=37)


    def _create_preference_matrix(self,label_manager, num_of_student, num_of_subject):
        """Metoda odpowiedzialna za wygenerowanie macierzy preferencji"""
        matrix = [0 for _ in range(num_of_student)]
        for i in range(num_of_student):
            matrix[i] = random.sample(range(1, num_of_subject+1), num_of_subject)
        AGenLibrary.MATRIX_IN=matrix
        label_manager.update_matrix_label(matrix)
    def _reload_matrix_txt(self,name_of_file,label_manager):
        matrix = []
        with open(name_of_file, 'r') as file:
            for line in file:
                verse = [int(element) for element in line.split()]
                matrix.append(verse)
        AGenLibrary.MATRIX_IN = matrix
        AGenLibrary.n = len(matrix)
        AGenLibrary.m = len(matrix[0])
        label_manager.update_matrix_label(matrix)



class EntryManager:
    """Manager danych wejściowych, dane wejściowe są tworzone i przechowywane w słowniku"""
    def __init__(self, master):
        self.master = master
        self.entries = {}

        self.entries['p'] = tk.Entry(master)
        self.entries['pc'] = tk.Entry(master)
        self.entries['pm'] = tk.Entry(master)
        self.entries['ps'] = tk.Entry(master)
        self.entries['iter'] = tk.Entry(master)
        self.entries['n'] = tk.Entry(master)
        self.entries['m'] = tk.Entry(master)
        self.entries['probability_elite'] = tk.Entry(master)
        self.entries['probability_rank'] = tk.Entry(master)
        self.entries['probability_roulette'] = tk.Entry(master)
        self.entries['probability_tournament'] = tk.Entry(master)

        self.entries['p'].place(x=20, y=250, width=100, height=25)
        self.entries['pc'].place(x=20, y=310, width=100, height=25)
        self.entries['pm'].place(x=20, y=370, width=100, height=25)
        self.entries['ps'].place(x=20, y=430, width=100, height=25)
        self.entries['iter'].place(x=20, y=490, width=100, height=25)
        self.entries['n'].place(x=1050, y=70, width=100, height=25)
        self.entries['m'].place(x=1250, y=70, width=100, height=25)
        self.entries['probability_elite'].place(x=1100, y=500, width=100, height=25)
        self.entries['probability_rank'].place(x=1100, y=550, width=100, height=25)
        self.entries['probability_roulette'].place(x=1100, y=600, width=100, height=25)
        self.entries['probability_tournament'].place(x=1100, y=650, width=100, height=25)

    def get_values(self):
        """Metoda zwracająca dane wejściowe w formie słownika - klucz: wejście"""
        return {key: entry.get() for key, entry in self.entries.items()}









