import random
import numpy as np
from cube import Cube
from copy import deepcopy
from tqdm import tqdm

# Paper: https://www-proquest-com.proxy3-bib.sdu.dk/docview/2150541241?accountid=14211&pq-origsite=summon
class GA:
	def __init__(self, pop_size=60, crossover_rate=0.1, iterations=100, chromosone_length=50, mutation_rate=1/50):
		# Init
		self.pop_size = pop_size
		self.mutation_rate = mutation_rate
		self.crossover_rate = crossover_rate
		self.iterations = iterations
		self.chromosone_length = chromosone_length
		self.possible_moves = ['u', 'U', 'f', 'F', 'l', 'L', 'r', 'R', 'd', 'D', 'b', 'B']
		self.init_population()
		self.cube = Cube()
		scramble = self.cube.scramble()
		print(scramble)
		self.child_cube = deepcopy(self.cube)
		self.isSolved = []
		self.numMoves = []

	def init_population(self):
		# Initialise population
		self.population = [''.join([random.choice(self.possible_moves) for j in range(self.chromosone_length)]) for i in range(self.pop_size)]

	def run(self):
		# Run the GA
		best_child = ''
		max_fitness = 0
		for it in tqdm(range(self.iterations)):
			# Calculate fitness for population
			child_fitness = self.fitness()
			max_fitness = np.max(child_fitness)
			best_child = self.population[child_fitness.index(max_fitness)]
			for i, s in enumerate(self.isSolved):
				if s:
					return self.population[i], self.numMoves[i]
			# Evolve
			mutate = self.evolve(child_fitness)
			# Save new population
			self.population = mutate
		return best_child, -1
	
	def evolve(self, child_fitness):
		# Evolve
		# Selection (Tournament selection)
		selected = self.selection(child_fitness)
		# Crossover
		crossover = self.crossover(selected)
		# Mutate
		return self.mutate(crossover)

	def selection(self, fitness, k=3):
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

	def mutate(self, crossover):
		# Mutate
		mutate = []
		for c in crossover:
			for i, ch in enumerate(c):
				if np.random.rand() < self.mutation_rate:
					c_list = list(c)
					chr = c[i]
					while(chr==c[i]):
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
		for child in self.population:
			self.child_cube.setState(self.cube.getState())
			solved, num_moves = self.child_cube.moves(child, detectSolved=True)
			self.isSolved.append(solved)
			self.numMoves.append(num_moves)
			child_fitness.append(self.child_cube.completeness())
		return child_fitness

if __name__ == "__main__":
	ga = GA(pop_size=100, iterations=9000)
	solution, num_moves = ga.run()
	print(solution)
	print(num_moves)