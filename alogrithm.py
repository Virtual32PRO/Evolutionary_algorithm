import AG_setup.py


def crossing():
    r_c=rows_columns()
    rows=r_c[0]
    columns=r_c[1]
    limits=r_c[2]
    original=create_matrix(rows,columns)
    mask=create_mask(rows,columns)
    parents=starting_parents()
    p1=parents[0]
    p2=parents[1]
    child1=np.empty(rows,columns)
    child2=np.empty(rows,columns)
    for i in range(rows):
        for j in range(columns):
            if mask[i][j]==0 and p1[i][j]>p2[i][j]:
                child1[i][j]=p2[i][j]
                child2[i][j] = p1[i][j]
            else:
                child1[i][j] = p1[i][j]
                child2[i][j] = p1[i][j]
    return child1,child2





