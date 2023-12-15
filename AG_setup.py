import random
import numpy

def rows_columns(): #losowe wybranie ilości uczniów, liczby przedmiotów i limitów w grupach
    rows=random.randint(50,120)
    columns=random.randint(4,8)
    for i in range(0,columns):
        limits[i]=random.randint(40,80)
    return rows,columns,limits


def create_matrix(rows,columns):
    matrix=np.empty(rows,columns)
    for i in range(rows):
        matrix[i]=random.sample(range(1,columns),columns) #wypisywanie tabeli z preferencjammi od 1 do liczby przedmiotów
    return matrix


def create_mask(rows,columns): #tworzenie maski z 0 i 1
    if type(rows) or type(columns) != int:
        return NULL
    else:
        mask=np.empty(rows,columns)
        for i in range(0,rows):
            for j in range(columns):
                mask[i][j]=random.randint(0,1)
    return mask


def starting_parents(row,columns):
    p1=create_matrix(rows,columns)
    p2=create_matrix(rows,columns)
    return p1,p2




