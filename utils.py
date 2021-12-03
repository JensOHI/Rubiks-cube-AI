import numpy as np
from enum import Enum
import glob
import os

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

def find_best_child(population, fitness):
    max_fitness = np.max(fitness)
    if fitness.count(max_fitness) > 1:
        idxs = np.where(fitness == max_fitness)[0]
        childs = np.asarray(population)[idxs]
        true_childs = [convert_index_to_moves(child) for child in childs]
        childs, true_childs = zip(*sorted(zip(childs, true_childs), key=lambda x: len(x[1])))
        return max_fitness, childs[0] 
    return max_fitness, population[fitness.index(max_fitness)]

def write_csv_file(filename, data):
    with open(filename, 'a') as file:
        file.writelines(','.join(data)+"\n")

def list_filenames_completed(folder):
    for name in glob.glob(folder + '/*'):
        with open(name, 'r') as file:
            lines = file.readlines()
        for line in lines[1:-1]:
            if int(line[:2]) >= 54:
                print(name)

if __name__ == "__main__":
    print(convert_moves_to_prime_convention('EByDYDYYybDSeEzZzmUX'))
    print(convert_moves_to_prime_convention('zfUBuFUbuFRBLUlUbrfluLuzLuRUUlUrLuRUUlUrUFRBLUlUbrfluLuFubUfuBULuRUUlUrLuRUUlUrUzdrDRRuRBBLulBBURRZZxUBBDDRFFDDBBLUZZDLdLLUlBBrURBBuLLuBBDDlFFDDBBruUURUUrFFLflUUlUULfFRBLUlUbrfluLuxyUBBDDRFFDDBBLUZrUlUURuLrUlUURuLulUULrFFRXYFubUfuBUrUlUURuLrUlUURuLuFubUfuBUUUBUUbRRFrfUUfUUFrXrUURlBBLUBBDDRFFDDBBLUyXXFRBLUlUbrfluLuzuBBDDlFFDDBBruDLdLLUlBBrURBBuLLUBBDDRFFDDBBLUDLdLLUlBBrURBBuLL'))
    #cr_mr_path = os.path.join("tests", "cr-"+str(0.5)+"_mr-"+str(0.5))
    #list_filenames_completed(cr_mr_path)