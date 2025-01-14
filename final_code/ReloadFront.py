import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import AGenLibrary


class Reload:
    def __init__(self, master, on_continue):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.place(relwidth=1, relheight=1)

        # Sekcja pobierania obrazu i skalowania
        self.img = Image.open('obraz5.png')
        self.resized_img = self.img.resize((1600, 800), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.resized_img)
        self.background_label = tk.Label(self.frame, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        #Sekcja etykiet
        self.welcome_label = tk.Label(self.frame, text="ładowanie",
                                      bg='White', fg='blue', font=('Helvetica', 25, 'bold'))
        self.status_label = tk.Label(self.frame, text="0%")

        #Sekcja przycisków
        self.start_button = tk.Button(self.frame, text="Stop",
                                      bg='lightblue', fg='black', font=('Helvetica', 15, 'bold'),
                                      relief=tk.RAISED, borderwidth=2, command=on_continue)


        #zmienna śledząca postęp i pasek zadań
        self.progress = tk.DoubleVar(self.frame)

        self.progressbar = ttk.Progressbar(self.frame, orient='horizontal',
                                           length=300, mode='determinate',
                                           variable=self.progress)

        # Sekcja lokalizacji przycisków i etykiet
        self.welcome_label.place(x=650, y=380, width=200, height=50)
        self.start_button.place(x=200, y=545, width=220, height=37)
        self.progressbar.place(x=600, y=450)
        self.status_label.place(x=730, y=480)

        self.update_progress()  # Rozpoczęcie aktualizacji paska postępu

    def update_progress(self):
        if AGenLibrary.num_of_iteration-1 < AGenLibrary.MAX_ITERATION:
            new_value = int((AGenLibrary.num_of_iteration/(AGenLibrary.MAX_ITERATION-1))*100)
            self.progress.set(new_value)
            self.status_label.config(text=f"{int(new_value)}%")
            self.master.after(100, self.update_progress)
    def show(self):
        self.frame.tkraise()

