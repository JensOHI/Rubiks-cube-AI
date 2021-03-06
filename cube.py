import numpy as np
import copy
from random import randint, choice
import utils

UP = 0
LEFT = 1
FRONT = 2
RIGHT = 3
DOWN = 4
BACK = 5

FITNESS_CROSS_DOWN = 1
FITNESS_CROSS_EDGE = 1
FITNESS_DOWN_CORNER = 1
FITNESS_CENTER_EDGE = 1
FITNESS_F2L = 2

class Cube:
    def __init__(self):
        self.setupDicts()
        # Up, left, front, right, down, back
        self.cube = np.array([[i]*8 for i in self.cube_colors.keys()])
        #self.cube = np.array([[j for j in range(8)] for i in range(8)])
        self.current_sub_problem = utils.SubSolution.CROSS

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
        self.completeness_dict = {
                            utils.SubSolution.CROSS: 8,
                            utils.SubSolution.CORNER_DOWN: 12,
                            #utils.SubSolution.CENTER_EDGE: 16,
                            #utils.SubSolution.F2L: 16
        }
        #Orange is down
        self.cross_indexs = [[4, 1, 2, 5], [4, 3, 3, 5], [4, 5, 5, 5], [4, 7, 1, 5]]
        self.down_indexs = [[4, 0, 1, 4, 2, 6], [4, 2, 2, 4, 3, 6], [4, 4, 3, 4, 5, 6], [4, 6, 5, 4, 1, 6]]
        self.center_edge_indexs = [[1, 3, 2, 7], [2, 3, 3, 7], [3, 3, 5, 7], [5, 3, 1, 7]]


    def moves(self, keys, detectSolved=False):
        for i, key in enumerate(keys):
            self.makeMove(key)
            #if self.isSolved() and detectSolved:
            if self.completeness() >= self.completeness_dict.get(self.current_sub_problem) and detectSolved:
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
        if self.current_sub_problem == utils.SubSolution.CROSS:
            return self.completeness_cross()
        elif self.current_sub_problem == utils.SubSolution.CORNER_DOWN:
            return self.completeness_corner_down()
        return 0
        '''elif self.current_sub_problem == utils.SubSolution.CENTER_EDGE:
            return self.completeness_center_edge()
        elif self.current_sub_problem == utils.SubSolution.F2L:
            return self.completeness_f2l()'''
        
    
    def completeness_cross(self):
        complete = 0
        for idx in self.cross_indexs:
            if self.cube[idx[0]][idx[1]] == idx[0]:
                complete += FITNESS_CROSS_DOWN
                if self.cube[idx[2]][idx[3]] == idx[2]:
                    complete += FITNESS_CROSS_EDGE
        return complete

    def completeness_corner_down(self):
        complete = self.completeness_cross()
        for idx in self.down_indexs:
            if self.cube[idx[0]][idx[1]] == idx[0] and self.cube[idx[2]][idx[3]] == idx[2] and self.cube[idx[4]][idx[5]] == idx[4]:
                complete += FITNESS_DOWN_CORNER
        return complete
    
    def completeness_center_edge(self):
        complete = self.completeness_corner_down()
        for idx in self.center_edge_indexs:
            if self.cube[idx[0]][idx[1]] == idx[0] and self.cube[idx[2]][idx[3]] == idx[2]:
                complete += FITNESS_CENTER_EDGE
        return complete

    def completeness_f2l(self):
        complete = self.completeness_cross()
        for idx_cd, idx_ce in zip(self.down_indexs, self.center_edge_indexs):
            if self.cube[idx_cd[0]][idx_cd[1]] == idx_cd[0] and self.cube[idx_cd[2]][idx_cd[3]] == idx_cd[2] and self.cube[idx_cd[4]][idx_cd[5]] == idx_cd[4] and self.cube[idx_ce[0]][idx_ce[1]] == idx_ce[0] and self.cube[idx_ce[2]][idx_ce[3]] == idx_ce[2]:
                complete += FITNESS_F2L
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