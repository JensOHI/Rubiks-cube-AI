import numpy as np
from enum import Enum

class SubSolution(Enum):
    CROSS = 1
    #CORNER_DOWN = 2
    #CENTER_EDGE = 3
    F2L = 2

    def next(self):
        return SubSolution(self.value + 1)

def swap_char(char):
    if char.isupper():
        return char.lower()
    return char.upper()

def max_n_elements_index(lst, n):
    lst_copy = np.copy(lst)
    max_lst = []
    for i in range(n):
        idx = np.argmax(lst_copy)
        max_lst.append(idx + i)
        lst_copy = np.delete(lst_copy, idx)
    return max_lst

def convert_moves_to_prime_convention(moves):
    converted_moves = ""
    for move in moves:
        if move in ['X', 'x', 'Y', 'y', 'Z', 'z']:
            if move.islower():
                converted_moves += move + "'"
            else:
                converted_moves += move.lower()
        elif move.islower():
            converted_moves += move.upper()+"'"
        else:
            converted_moves += move
    return converted_moves


