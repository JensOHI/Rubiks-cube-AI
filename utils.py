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

def convert_index_to_moves(idxs):
    moves = ""
    for idx in idxs:
        moves += permutations[idx]
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


