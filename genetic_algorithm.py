import random
import numpy as np
from numpy import core
from cube import Cube
from copy import deepcopy
from tqdm import tqdm
import time

import utils
#https://ieeexplore-ieee-org.proxy1-bib.sdu.dk/abstract/document/9376564
# Paper: https://www-proquest-com.proxy3-bib.sdu.dk/docview/2150541241?accountid=14211&pq-origsite=summon
class GA:
	def __init__(self, pop_size=60, crossover_rate=0.1, iterations=100, chromosone_length=50, mutation_rate = 1/50):
		# Init
		self.pop_size = pop_size
		self.mutation_rate = mutation_rate
		self.crossover_rate = crossover_rate
		self.iterations = iterations
		self.chromosone_length = chromosone_length
		self.chromosone_length_start_value = self.chromosone_length
		self.possible_moves = range(0,len(utils.permutations))
		self.init_population()
		self.cube = Cube()
		self.scramble = self.cube.scramble()
		self.child_cube = deepcopy(self.cube)
		self.isSolved = []
		self.numMoves = []
		self.expand_chromosone = 1

	def init_population(self):
		# Initialise population
		self.population = []
		for i in range(self.pop_size):
			child = []
			for j in range(self.chromosone_length):
				child.append(random.choice(self.possible_moves))
			self.population.append(child)
		

	def run(self):
		# Run the GA
		best_child = []
		max_fitness = 0


		for it in tqdm(range(self.iterations), desc="Running GA agent for scramble {}".format(self.scramble)):
			for i in range(len(self.population)):
				self.population[i] = list(self.population[i])
			for child in self.population:
				child.extend([np.random.choice(self.possible_moves)])
			# Calculate fitness for population
			child_fitness = self.fitness()
			max_fitness = np.max(child_fitness)
			best_child = self.population[child_fitness.index(max_fitness)]
			
			
			# Dynamic mutation rate, depending on fitness
			#self.mutation_rate = 2.0/max_fitness
			
			for i, s in enumerate(self.isSolved):
				if s:
					return utils.convert_index_to_moves(self.population[i][0:self.numMoves[i]+1])
			# Evolve and save new population
			self.population = self.evolve(child_fitness)
		return utils.convert_index_to_moves(best_child)
	
	def evolve(self, child_fitness):
		# Evolve
		# Selection (Tournament selection)
		selected = self.selection_roulette_wheel(child_fitness)
		np.random.shuffle(selected)
		'''
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
		'''
		return selected

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

	def crossover(self, selected):
		# Crossover
		crossover = []
		for i in range(0, self.pop_size, 2):
			if np.random.rand() < self.crossover_rate:
				# select crossover point that is not on the end of the string
				pt = np.random.randint(1, self.chromosone_length-2)
				# perform crossover
				crossover.append(np.hstack((selected[i][:pt], selected[i+1][pt:])))
				crossover.append(np.hstack((selected[i+1][:pt], selected[i][pt:])))
			else:
				crossover.append(selected[i])
				crossover.append(selected[i+1])
		return crossover
		
	def mutate(self, crossover):
		# Mutate
		mutate = []
		for child in crossover:
			for c in child:
				if np.random.rand() < self.mutation_rate:
					c = random.choice(self.possible_moves)
			mutate.append(child)
		return mutate

	

	def fitness(self):
		# Calculate fitness
		child_fitness = []
		self.isSolved = []
		self.numMoves = []		
		for child in self.population:
			self.child_cube.setState(self.cube.getState())
			solved, num_moves = self.child_cube.moves_idx(child, detectSolved=True)
			self.isSolved.append(solved)
			self.numMoves.append(num_moves)
			child_fitness.append(self.child_cube.completeness())
		return child_fitness

if __name__ == "__main__":
	ga = GA(pop_size=100, chromosone_length=5, crossover_rate=0.5, mutation_rate=1/3, iterations=9000)
	print(ga.run())
