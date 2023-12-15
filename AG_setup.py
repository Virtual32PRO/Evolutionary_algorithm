import random
import numpy

def rows_columns():
    rows=random.randint(50,120)
    columns=random.randint(4,8)
    for i in range(0,columns):
        limits[i]=random.randint(40,80)
    return rows,columns,limits


def create_matrix(rows,columns):
    matrix=np.empty(rows,columns)
    for i in range(rows):
        matrix[i]=random.sample(range(1,columns),columns)
    return matrix


def create_mask(rows,columns):
    if type(rows) or type(columns) != int:
        return NULL
    else:
        mask=np.empty(rows,columns)
        for i in range(0,rows):
            for j in range(columns):
                mask[i][j]=random.randint(0,1)
    return mask




