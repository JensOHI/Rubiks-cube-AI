import numpy as np
from enum import Enum

class SubSolution(Enum):
    CROSS = 1
    CORNER_DOWN = 2
    #CENTER_EDGE = 3
    #F2L = 2

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

def find_best_child(population, fitness):
    max_fitness = np.max(fitness)
    if fitness.count(max_fitness) > 1:
        idxs = np.where(fitness == max_fitness)[0]
        childs = np.asarray(population)[idxs]
        return max_fitness, sorted(childs)[0]
    return max_fitness, population[fitness.index(max_fitness)]

def write_csv_file(filename, data):
    with open(filename, 'a') as file:
        file.writelines(','.join(data)+"\n")
