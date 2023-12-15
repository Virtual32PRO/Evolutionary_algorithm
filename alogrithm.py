import AG_setup as ag
import numpy as np


def crossing(): #wstępne krzyżowanie
    r_c=ag.rows_columns()
    rows=r_c[0]
    columns=r_c[1]
    mask=ag.create_mask(rows,columns)
    parents=ag.starting_parents(rows,columns)
    p1=parents[0]
    p2=parents[1]
    child1=np.empty(shape=(rows,columns))
    child2=np.empty(shape=(rows,columns))
    for i in range(rows):
        for j in range(columns):
            if mask[i][j]==0 and p1[i][j]>p2[i][j]: #jeżeli maska to 0 to bierze tego z mniejszą wartością
                child1[i][j]=p2[i][j]
                child2[i][j] = p1[i][j]
            else:
                child1[i][j] = p1[i][j]
                child2[i][j] = p1[i][j]
    return child1,child2

children=crossing()
child1=children[0]
child2=children[1]
print(child1)
print(child2)



