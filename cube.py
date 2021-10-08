import numpy as np
import copy
from random import randint, choice

UP = 0
LEFT = 1
FRONT = 2
RIGHT = 3
DOWN = 4
BACK = 5

class Cube:
    def __init__(self):
        self.setupDicts()
        # Up, left, front, right, down, back
        self.cube = np.array([[i]*8 for i in self.cube_colors.keys()])
        #self.cube = np.array([[j for j in range(8)] for i in range(8)])

    def setupDicts(self):
        self.cube_colors = {0: 'red',
                            1: 'blue',
                            2: 'white',
                            3: 'green',
                            4: 'orange',
                            5: 'yellow'}
        self.move_order = { 'F': [FRONT, DOWN, LEFT, UP, RIGHT],
                            'L': [LEFT, DOWN, BACK, UP, FRONT],
                            'B': [BACK, DOWN, RIGHT, UP, LEFT],
                            'R': [RIGHT, DOWN, FRONT, UP, BACK],
                            'U': [UP, FRONT, LEFT, BACK, RIGHT],
                            'D': [DOWN, BACK, LEFT, FRONT, RIGHT],
                            'f': [FRONT, DOWN, RIGHT, UP, LEFT],
                            'l': [LEFT, DOWN, FRONT, UP, BACK],
                            'b': [BACK, DOWN, LEFT, UP, RIGHT],
                            'r': [RIGHT, DOWN, BACK, UP, FRONT],
                            'u': [UP, FRONT, RIGHT, BACK, LEFT],
                            'd': [DOWN, BACK, RIGHT, FRONT, LEFT]}
        self.idx_list = {   'F': [[0,1,2], [2,3,4],[4,5,6],[6,7,0]],
                            'L': [[6,7,0],[2,3,4],[6,7,0],[6,7,0]],
                            'B': [[4,5,6],[2,3,4],[0,1,2],[6,7,0]],
                            'R': [[2,3,4],[2,3,4],[2,3,4],[6,7,0]],
                            'U': [[0,1,2],[0,1,2],[0,1,2],[0,1,2]],
                            'D': [[4,5,6],[4,5,6],[4,5,6],[4,5,6]],
                            'f': [[0,1,2],[6,7,0],[4,5,6],[2,3,4]],
                            'l': [[6,7,0],[6,7,0],[6,7,0],[2,3,4]],
                            'b': [[4,5,6],[6,7,0],[0,1,2],[2,3,4]],
                            'r': [[2,3,4],[6,7,0],[2,3,4],[2,3,4]],
                            'u': [[0,1,2],[0,1,2],[0,1,2],[0,1,2]],
                            'd': [[4,5,6],[4,5,6],[4,5,6],[4,5,6]]}

    def moves(self, keys, detectSolved=False):
        for i, key in enumerate(keys):
            self.makeMove(key)
            if self.isSolved() and detectSolved:
                return True, i
        return False, -1
    
    def makeMove(self, key):
        order = self.move_order.get(key)
        idx_list = self.idx_list.get(key)
        tmp_cube = copy.deepcopy(self.cube)
        tmp_cube[order[0]] = np.roll(self.cube[order[0]], 2 if key.isupper() else -2)
        for i, face in enumerate(order[1:-1]):
            tmp_cube[order[i+2]][idx_list[i+1]] = self.cube[face][idx_list[i]]
        tmp_cube[order[1]][idx_list[0]] = self.cube[order[-1]][idx_list[-1]]
        self.cube = copy.deepcopy(tmp_cube)

    def scramble(self):
        moves = ''
        for i in range(randint(20, 40)):
            move = choice(list(self.move_order.keys()))
            moves += move
        self.moves(moves)
        return moves

    def isSolved(self):
        for i,face in enumerate(self.cube):
            result = np.all(face == i)
            if not result:
                return False
        return True

    def printCube(self):
        m = np.empty((12,9),dtype=str)
        m.fill(' ')
        tmp_m = []
        for face in self.cube:
            tmp = np.array(([face[0],face[1],face[2]],[face[7],-1,face[3]],[face[6],face[5],face[4]]))
            tmp_tmp = np.empty_like(tmp,dtype=str)
            for i, row in enumerate(tmp):
                for j, element in enumerate(row):
                    tmp_tmp[i][j] = self.cube_colors.get(element, " ")
            tmp_m.append(tmp_tmp)
        m[0:3,3:6] = tmp_m[0]
        m[3:6,0:3] = tmp_m[1]
        m[3:6,3:6] = tmp_m[2]
        m[3:6,6:] = tmp_m[3]
        m[6:9,3:6] = tmp_m[4]
        m[9:,3:6] = tmp_m[5]
        print(m)

    def completeness(self):
        complete = 0
        for i, row in enumerate(self.cube):
            complete += np.count_nonzero(row == i)
        return complete

    def setState(self, state):
        self.cube = state

    def getState(self):
        return self.cube


def main():
    cube = Cube()
    #moves = cube.scramble()
    cube.moves('bBrURUbdUdRfFdbRBULRLbURBLuBfuuFlfdUuU',detectSolved=True)
    print(cube.completeness())
    #cube.printCube()
    #cube.moves(moves)
    #cube.moves(moves[::-1].swapcase())
    #print(cube.completeness())
    cube.printCube()

if __name__ == "__main__":
    main()