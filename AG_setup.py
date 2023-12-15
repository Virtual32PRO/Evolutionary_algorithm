import random
import numpy as np

def rows_columns(): #losowe wybranie ilości uczniów, liczby przedmiotów i limitów w grupach
    rows=random.randint(50,120)
    columns=random.randint(4,8)
    limits = [random.randint(40, 80) for subject in range(columns)]
    return rows,columns,limits


def create_matrix(rows,columns):
    matrix=[]
    for i in range(rows):
        ok=random.sample(range(1,columns+1),columns) #wypisywanie tabeli z preferencjammi od 1 do liczby przedmiotów
        matrix.append(ok)
    return matrix


def create_mask(rows,columns): #tworzenie maski z 0 i 1
    mask = np.random.randint(2, size=(rows, columns))
    return mask


def starting_parents(rows,columns):
    p1=create_matrix(rows,columns)
    p2=create_matrix(rows,columns)
    return p1,p2








