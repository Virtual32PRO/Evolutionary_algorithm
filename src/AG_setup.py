import random
import numpy as np

def rows_columns(): #losowe wybranie ilości uczniów, liczby przedmiotów i limitów w grupach
    rows=random.randint(50,120) #wybór zakresu liczby uczniów
    columns=random.randint(4,8) #wybór zakresu liczby przedmiotów
    limits = [random.randint(40, 80) for subject in range(columns)] #wybór zakresu limitu w grupach
    return rows,columns,limits


def create_matrix(rows,columns):
    matrix=np.empty(shape=(rows,columns))
    for i in range(rows):
        matrix[i]=random.sample(range(1,columns+1),columns) #wypisywanie tabeli z preferencjammi od 1 do liczby przedmiotów

    return matrix

def ideal_matrix(m):
    rows,columns=m.shape
    ideal_matrix=np.empty(shape=(rows,columns))
    subjects=round(columns/2)
    for i in range(rows):
        for j in range(columns):
            if m[i][j]>subjects:
                ideal_matrix[i][j]=1
            else:
                ideal_matrix[i][j]=0
    return ideal_matrix


def create_mask(rows,columns): #tworzenie maski z 0 i 1
    mask = np.random.randint(2, size=(rows, columns))
    return mask


def starting_parents(rows,columns):
    p1=create_matrix(rows,columns)
    p2=create_matrix(rows,columns)
    return p1,p2






