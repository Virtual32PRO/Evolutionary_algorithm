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
    child=np.empty(rows,columns)
    for i in range(rows):
        for j in range(columns):
            if mask[i][j]==0 and p1[i][j]>p2[i][j]:
                child[i][j]=p2[i][j]
            else:
                child[i][j] = p1[i][j]



