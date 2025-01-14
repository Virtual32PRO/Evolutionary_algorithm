import tkinter as tk
from PIL import Image, ImageTk
class Welcome:
    def __init__(self, master, on_aplication, on_instruction, on_information):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.place(relwidth=1, relheight=1)

        #Sekcja pobierania obrazu i skalowania
        self.img = Image.open('obraz4.png')
        self.resized_img = self.img.resize((1600, 800), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.resized_img)
        self.background_label = tk.Label(self.frame, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        #Sekcja etykiet
        self.welcome_label = tk.Label(self.frame, text="Witaj w aplikacji\nTester Algorytmu Genetycznego",
                                      bg='White', fg='blue', font=('Helvetica', 25, 'bold'))


        #Sekcja przycisków
        self.start_button = tk.Button(self.frame, text="Start",
                                      bg='lightblue', fg='black', font=('Helvetica', 15, 'bold'),
                                      relief=tk.RAISED, borderwidth=2, command=on_aplication)

        self.welcome_button2 = tk.Button(self.frame, text="Instrukcja", bg='lightblue', fg='black',
                                         font=('Helvetica', 15, 'bold'),
                                         relief=tk.RAISED, borderwidth=2, command=on_instruction)

        self.welcome_button3 = tk.Button(self.frame, text="Informacje o aplikacji", bg='lightblue', fg='black',
                                         font=('Helvetica', 15, 'bold'),relief=tk.RAISED, borderwidth=2, command= on_information)

        #Sekcja lokalizacji przycisków i etykiet
        self.welcome_label.place(x=500, y=310, width=550, height=100)
        self.start_button.place(x=100, y=500, width=220, height=37)
        self.welcome_button2.place(x=100, y=550, width=220, height=37)
        self.welcome_button3.place(x=100, y=600, width=220, height=37)

    def show(self):
        self.frame.tkraise()