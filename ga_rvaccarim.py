from cube import Cube
import numpy as np
from copy import deepcopy
import utils
from tqdm import tqdm
class GA:
    def __init__(self, pop_size=500, iterations=300, max_resets=10, elitetism=50):
        self.population_size = pop_size
        self.iterations = iterations
        self.max_resets = max_resets
        self.elitetism = elitetism

        self.possible_moves = ['u', 'U', 'f', 'F', 'l', 'L', 'r', 'R', 'd', 'D', 'b', 'B']

        #Scramble
        self.scramble = Cube().scramble()#"dBBDDLLuLrFLLRRuLLbLdBBRRbRFUURBBflBBLLRFFl"#Cube().scramble()
    

    def solve(self):
        for resets in range(0, self.max_resets):
            self.children = []

            for pop in range(0,self.population_size):
                cube = Cube()
                cube.moves(self.scramble)
                cube.applied_moves = ""

                cube.move(np.random.choice(self.possible_moves))
                cube.move(np.random.choice(self.possible_moves))
                self.children.append(cube)
            
            for generation in tqdm(range(0, self.iterations), desc="Solving for scramble: "+utils.convert_moves_to_prime_convention(self.scramble)):
                fitness = [child.completeness() for child in self.children]
                self.children, fitness =  zip(*reversed(sorted(zip(self.children, fitness), key=lambda pair: pair[1])))
                
                if generation % 20 == 0:
                    tqdm.write("Generation: "+str(generation))
                    tqdm.write("Best solution so far: "+utils.convert_moves_to_prime_convention(self.children[0].applied_moves))
                    tqdm.write("Fitness: "+str(fitness[0]))

                for i, child in enumerate(self.children):
                    if fitness[i] >= 54:
                        print("Solved")
                        print(self.scramble)
                        print(utils.convert_moves_to_prime_convention(child.applied_moves))
                        return True
                    

                    if i > self.elitetism:
                        child = deepcopy(self.children[np.random.randint(0,self.elitetism)])
                        evolution_type = np.random.randint(0,6)
         

                        if evolution_type == 0:
                            child.moves(self.__rnd_permutation())
                        elif evolution_type == 1:
                            child.moves(self.__rnd_permutation())
                            child.moves(self.__rnd_permutation())
                        elif evolution_type == 2:
                            child.moves(self.__rnd_full_rotation())
                            child.moves(self.__rnd_permutation())
                        elif evolution_type == 3:
                            child.moves(self.__rnd_orientation())
                            child.moves(self.__rnd_permutation())
                        elif evolution_type == 4:
                            child.moves(self.__rnd_full_rotation())
                            child.moves(self.__rnd_orientation())
                            child.moves(self.__rnd_permutation())
                        elif evolution_type == 5:
                            child.moves(self.__rnd_orientation())
                            child.moves(self.__rnd_full_rotation())
                            child.moves(self.__rnd_permutation())

    def __rnd_full_rotation(self):
        return np.random.choice(utils.rotations)
    
    def __rnd_orientation(self):
        return np.random.choice(utils.orientations)
    
    def __rnd_permutation(self):
        return np.random.choice(utils.permutations)





if __name__ == "__main__":
    ga = GA()
    ga.solve()
