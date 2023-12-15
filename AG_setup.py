import random

def rows_columns():
    rows=random.randint(50,120)
    columns=random.randint(4,8)
    for i in range(0,columns):
        limits[i]=random.randint(40,80)
    return rows,columns,limits

def create_mask(rows ,columns):
    if type(rows) or type(columns)  