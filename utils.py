import numpy as np
from enum import Enum

# https://robertovaccari.com/blog/2020_07_07_genetic_rubik/
rotations = ["X", "x", "Y", "y", "YY", "XX"]

orientations = ["Z", "z", "ZZ"]

permutations = [
    "flbruRuBLFRUrU",
    "FRBLUlUbrfluLu",
    "UUBUUbRRFrfUUfUUFr",
    "UURUUrFFLflUUlUULf",
    "uBBDDlFFDDBBru",
    "UBBDDRFFDDBBLU",
    "drDRRuRBBLulBBURR",
    "DLdLLUlBBrURBBuLL",
    "rUlUURuLrUlUURuLu",
    "LuRUUlUrLuRUUlUrU",
    "fUBuFUbu",
    "FubUfuBU",
    "lUULrFFR",
    "rUURlBBL",
    "MMUMMUUMMUMM"
]

permutations_range = [0, len(permutations)]
orientations_range = [len(permutations), len(permutations) + len(orientations)]
rotations_range = [len(permutations) + len(orientations), len(permutations) + len(orientations) + len(rotations)]


def convert_index_to_moves(idxs):
    moves = ""
    for idx in idxs:
        if idx < permutations_range[1]:
            moves += permutations[idx]
        elif idx >= orientations_range[0] and idx < orientations_range[1]:
            moves += orientations[idx - orientations_range[0]]
        elif idx >= rotations_range[0] and idx < rotations_range[1]:
            moves += rotations[idx - rotations_range[0]]
        else:
            raise ValueError("Convert index to moves out of range.")

    return moves

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

def get_random_move():
    # Return either permutaion, rotation or orientation
    prob = np.random.randint(0,100)
    if prob < 60:
        return np.random.randint(permutations_range[0],permutations_range[1])
    elif prob >= 60 and prob < 80:
        return np.random.randint(orientations_range[0], orientations_range[1])
    else:
        return np.random.randint(rotations_range[0], rotations_range[1])

def get_shortest_solution(sol1, sol2):
    return sol1 if len(convert_index_to_moves(sol1)) < len(convert_index_to_moves(sol2)) else sol2