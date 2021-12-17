import random
import numpy as np
from numpy import core
from cube import Cube
from copy import deepcopy
from tqdm import tqdm
import os
import time

import utils
#https://ieeexplore-ieee-org.proxy1-bib.sdu.dk/abstract/document/9376564
# Paper: https://www-proquest-com.proxy3-bib.sdu.dk/docview/2150541241?accountid=14211&pq-origsite=summon
class GA:
	def __init__(self, pop_size=60, crossover_rate=0.1, iterations=100, chromosone_length=50, mutation_rate = 1/50, scramble = Cube().scramble(), filename = None):
		# Init
		self.pop_size = pop_size
		self.mutation_rate = mutation_rate
		self.crossover_rate = crossover_rate
		self.iterations = iterations
		self.chromosone_length = chromosone_length
		self.chromosone_length_start_value = self.chromosone_length
		self.possible_moves = ['u', 'U', 'f', 'F', 'l', 'L', 'r', 'R', 'd', 'D', 'b', 'B']
		self.init_population()
		self.scramble = scramble
		self.cube = Cube()
		self.cube.moves(self.scramble)
		print("Scramble:",self.scramble)
		self.child_cube = deepcopy(self.cube)
		self.isSolved = []
		self.numMoves = []
		self.expand_chromosone = 1
		self.current_solution = ""
		self.current_sub_problem = utils.SubSolution.CROSS
		self.filename = filename

	def init_population(self):
		# Initialise population
		self.population = []
		for i in range(self.pop_size):
			child = ''
			for j in range(self.chromosone_length):
				move = random.choice(self.possible_moves)
				while(j > 0 and move == utils.swap_char(child[-1])):
					move = random.choice(self.possible_moves)
				child += move
			self.population.append(child)
		#self.population = [''.join([random.choice(self.possible_moves) for j in range(self.chromosone_length)]) for i in range(self.pop_size)]

	def run(self):
		# Run the GA
		best_child = ''
		max_fitness = 0
		if self.filename:
			utils.write_csv_file(self.filename, ["max fitness", "best child"])
		for it in tqdm(range(self.iterations), desc="Running GA agent for scramble {}".format(self.scramble)):
			# Calculate fitness for population
			if it % 20 == 0:
				self.chromosone_length += self.expand_chromosone
				for i, pop in enumerate(self.population):
					for n in range(self.expand_chromosone):
						pop += random.choice(self.possible_moves)
					self.population[i] = pop
			child_fitness = self.fitness()
			max_fitness, best_child = utils.find_best_child(self.population, child_fitness)
			if self.filename:
				utils.write_csv_file(self.filename, [str(max_fitness), self.current_solution+ " + " +best_child])
			tqdm.write("Max fitness " + str(max_fitness) + " - " + self.current_solution + " + " +  best_child)
			
			# Dynamic mutation rate, depending on fitness
			#self.mutation_rate = 2.0/max_fitness
			
			new_sub_problem = False
			for i, s in enumerate(self.isSolved):
				if s and not new_sub_problem:
					tqdm.write(self.population[i][0:self.numMoves[i]+1] + " - " + str(i) + " - " + str(self.numMoves[i]+1))
					_, _ = self.cube.moves(self.population[i][0:self.numMoves[i]+1])
					self.current_solution += self.population[i][0:self.numMoves[i]+1]
					self.isSolved = []
					self.numMoves = []
					if self.current_sub_problem == utils.SubSolution.CORNER_DOWN:
						return self.current_solution, it
					self.current_sub_problem = self.current_sub_problem.next()
					self.cube.current_sub_problem = self.current_sub_problem
					self.child_cube.current_sub_problem = self.current_sub_problem
					self.chromosone_length = self.chromosone_length_start_value
					self.init_population()
					new_sub_problem = True
			if not new_sub_problem:
				# Evolve and save new population
				self.population = self.evolve(child_fitness)
		return self.current_solution + best_child, self.iterations
	
	def evolve(self, child_fitness):
		# Evolve
		# Selection (Tournament selection)
		selected = self.selection_roulette_wheel(child_fitness)
		np.random.shuffle(selected)
		self.population = selected
		selected_fitness = self.fitness()

		# Crossover
		crossover = self.crossover(selected)
		# Mutate
		mutate = self.mutate(crossover)

		self.population = mutate
		mutate_child_fitness = self.fitness()

		for i, (prev_child, new_child) in enumerate(zip(selected_fitness, mutate_child_fitness)):
			if new_child < prev_child:
				mutate[i] = selected[i]

		return mutate

	def selection_tournament(self, fitness, k=3):
		# Tournament selection
		# first random selection
		selected = []
		for i in range(self.pop_size):
			selection_ix = np.random.randint(self.pop_size)
			for ix in np.random.randint(0, self.pop_size, k-1):
				# check if better (e.g. perform a tournament)
				if fitness[ix] > fitness[selection_ix]:
					selection_ix = ix
			selected.append(self.population[selection_ix])
		return selected

	def selection_roulette_wheel(self, fitness):
		#Picking the 20% best players
		n = int(self.pop_size*0.2)
		selection_idx = utils.max_n_elements_index(fitness, n)
		selection = []
		for select in selection_idx:
			selection.append(self.population[select])
		selection = np.asarray(selection)

		# Rest of population is picked by roulette wheel and merged with the 20% best
		return np.concatenate((selection, random.choices(self.population, weights=fitness, k=self.pop_size-n)))


	def mutate(self, crossover):
		# Mutate
		mutate = []
		for c in crossover:
			for i, ch in enumerate(c):
				if np.random.rand() < self.mutation_rate:
					c_list = list(c)
					chr = c[i]
					while(chr==c[i] or ((i > 0 and i < len(c)-1) and (chr == utils.swap_char(c[i-1]) or chr == utils.swap_char(c[i+1]) or chr == c[i]))):
						chr = random.choice(self.possible_moves)
					c_list[i] = chr
					c = ''.join(c_list)
			mutate.append(c)
		return mutate

	def crossover(self, selected):
		# Crossover
		crossover = []
		for i in range(0, self.pop_size, 2):
			if np.random.rand() < self.crossover_rate:
				# select crossover point that is not on the end of the string
				pt = np.random.randint(1, self.chromosone_length-2)
				# perform crossover
				crossover.append(selected[i][:pt] + selected[i+1][pt:])
				crossover.append(selected[i+1][:pt] + selected[i][pt:])
			else:
				crossover.append(selected[i])
				crossover.append(selected[i+1])
		return crossover

	def fitness(self):
		# Calculate fitness
		child_fitness = []
		self.isSolved = []
		self.numMoves = []
		for child in self.population:
			self.child_cube.setState(self.cube.getState())
			solved, num_moves = self.child_cube.moves(child, detectSolved=True)
			self.isSolved.append(solved)
			self.numMoves.append(num_moves)
			child_fitness.append(self.child_cube.completeness())
		return child_fitness

if __name__ == "__main__":
	#for i in range(10):
	#	utils.write_csv_file("scrambles.txt", [Cube().scramble()])
	scrambles = []
	with open("scrambles.txt", 'r') as file:
		for line in file.readlines():
			scrambles.append(line[:-1])

	TEST_FOLDER = "tests"
	if not os.path.exists(TEST_FOLDER):
		os.mkdir(TEST_FOLDER)
	crossover_rates = [0.5]
	mutation_rates = [0.5]
	for crossover_rate in crossover_rates:
		for mutation_rate in mutation_rates:
			cr_mr_path =os.path.join(TEST_FOLDER, "cr-"+str(crossover_rate)+"_mr-"+str(mutation_rate))
			if not os.path.exists(cr_mr_path):
				os.mkdir(cr_mr_path)
			for i, scramble in enumerate(scrambles):
				for test_scramble in range(30):
					filename = os.path.join(cr_mr_path,"test_"+str(i)+"_"+str(test_scramble)+".csv")
					ga = GA(pop_size=100, chromosone_length=5, crossover_rate=crossover_rate, mutation_rate=mutation_rate, iterations=350, scramble=scramble, filename=filename)
					start_time = time.time()
					best_solution, num_of_generation = ga.run()
					completion_time = time.time() - start_time
					utils.write_csv_file(filename, ["Completion time", "Solution", "Generations", "Scramble"])
					utils.write_csv_file(filename, [str(completion_time), best_solution, str(num_of_generation), scramble])

	'''
	ga = GA(pop_size=100, chromosone_length=5, crossover_rate=0.5, mutation_rate=1/3, iterations=9000)
	print(ga.run())
	'''
