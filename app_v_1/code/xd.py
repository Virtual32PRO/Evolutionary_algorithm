import random

def generate_random_binary_list(length, bad_addresses, good_addresses):
    #length=len(matrix[0])
    i=1
    result=[]
    while i!=0:
        result = [0 for _ in range(length)]
        address = random.sample(range(length), 3)
        for x in address:
            result[x] = 1
        for j in range(length):
            if result[bad_addresses[0]]==0 or result[bad_addresses[1]]==0 or result[good_addresses[0]]==result[good_addresses[1]]:
                i-=1
    return result

length=8
b=[0,7]
g=[1,5]

print(generate_random_binary_list(length,b,g))


