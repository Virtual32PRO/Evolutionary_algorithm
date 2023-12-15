import AG_setup as ag


def crossing(): #wstępne krzyżowanie
    r_c=ag.rows_columns()
    rows=r_c[0]
    columns=r_c[1]
    limits=r_c[2]
    original=ag.create_matrix(rows,columns)
    mask=ag.create_mask(rows,columns)
    parents=ag.starting_parents()
    p1=parents[0]
    p2=parents[1]
    child1=np.empty(rows,columns)
    child2=np.empty(rows,columns)
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
print(child1)



