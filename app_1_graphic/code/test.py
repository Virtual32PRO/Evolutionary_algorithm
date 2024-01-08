import main
import pytest
import AGenLibrary

m=main.create_matrix(100,10)
good_address=[0,1,0,0,0,1,0,0,0,0]

bad_address=[0,0,1,1,0,0,0,0,0,0]


def test_matrix_bad_subjects():
    for i in range (100):
        assert m[i]!=bad_address

def test_matrix_good_subjects():
    for i in range (100):
        assert m[i]==good_address


def test_limit():
    #Element=AGenLibrary.Element()
    matrix=main.ScheduleMatrix(m)
    assert matrix.check_group_limits(m)==1

print(test_limit())
print(test_matrix_bad_subjects())









