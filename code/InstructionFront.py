import tkinter as tk
class Instruction:
    def __init__(self, master, on_continue):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.place(relwidth=1, relheight=1)

        self.welcome_label = tk.Label(self.frame, text="Instrukcja",
                                      bg='White', fg='blue', font=('Helvetica', 25, 'bold'))
        self.welcome_label.place(x=20, y=20, width=550, height=100)

        self.start_button = tk.Button(self.frame, text="Menu",
                                      bg='lightblue', fg='black', font=('Helvetica', 15, 'bold'),
                                      relief=tk.RAISED, borderwidth=2, command=on_continue)
        self.start_button.place(x=60, y=500, width=220, height=37)

    def show(self):
        self.frame.tkraise()
