import random

def generate_binary_list(length, forbidden_positions):
    ones_count = 3
    allowed_positions = [i for i in range(length) if i not in forbidden_positions]

    if len(allowed_positions) < ones_count:
        raise ValueError("Zbyt mało dostępnych pozycji dla jednynek.")

    random_ones_positions = random.sample(allowed_positions, ones_count)
    binary_list = [1 if i in random_ones_positions else 0 for i in range(length)]

    return binary_list

# Przykład użycia
length_of_list = 10
forbidden_positions = [2, 5, 8]

try:
    result_list = generate_binary_list(length_of_list, forbidden_positions)
    print(result_list)
except ValueError as e:
    print(e)
