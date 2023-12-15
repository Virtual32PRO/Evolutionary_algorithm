import AG_setup as ag
import numpy as np



def crossing(p1,p2): #krzyżowanie

    rows, columns=p1.shape
    mask=ag.create_mask(rows,columns)
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





