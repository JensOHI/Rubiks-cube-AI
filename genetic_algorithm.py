import random
import numpy as np
from numpy import core
from cube import Cube
from copy import deepcopy
from tqdm import tqdm
import time
import os
from multiprocessing import Pool

import utils
#https://ieeexplore-ieee-org.proxy1-bib.sdu.dk/abstract/document/9376564
# Paper: https://www-proquest-com.proxy3-bib.sdu.dk/docview/2150541241?accountid=14211&pq-origsite=summon
class GA:
	def __init__(self, pop_size=60, crossover_rate=0.1, iterations=100, chromosone_length=1, mutation_rate = 1/50, scramble = Cube().scramble(), filename = None):
		# Init
		self.pop_size = pop_size
		self.mutation_rate = mutation_rate
		self.crossover_rate = crossover_rate
		self.iterations = iterations
		self.chromosone_length = chromosone_length
		self.num_extra_moves = 2
		self.init_population()
		self.scramble = scramble
		self.cube = Cube()
		self.cube.moves(scramble)
		self.child_cube = deepcopy(self.cube)
		self.filename = filename
		self.max_fitness_list = []

	def init_population(self):
		# Initialise population
		self.population = []
		for i in range(self.pop_size):
			child = []
			for j in range(self.chromosone_length):
				child.append(utils.get_random_move())
			self.population.append(child)
		

	def run(self):
		# Run the GA
		best_child = []
		max_fitness = 0
		self.max_fitness_list.append(max_fitness)
		if self.filename:
			utils.write_csv_file(self.filename, ["max fitness", "best child"])
		#for it in tqdm(range(self.iterations), desc="Running GA agent for scramble {}".format(utils.convert_moves_to_prime_convention(self.scramble))):
		for it in range(self.iterations):
			# Calculate fitness for population
			child_fitness = self.fitness(self.population)
			max_fitness, best_child = utils.find_best_child(self.population, child_fitness)
			if max_fitness > self.max_fitness_list[-1]:
				self.max_fitness_list = [max_fitness]
				self.num_extra_moves = 2
			else:
				self.max_fitness_list.append(max_fitness)
			if len(self.max_fitness_list) >= 20 and len(self.max_fitness_list) < 30:
				self.num_extra_moves = 3
			elif len(self.max_fitness_list) >= 30 and len(self.max_fitness_list) < 40:
				self.num_extra_moves = 4
			elif len(self.max_fitness_list) >= 40 and len(self.max_fitness_list) < 50:
				self.num_extra_moves = 5
			elif len(self.max_fitness_list) >= 50:
				self.num_extra_moves = 6
			if self.filename:
				utils.write_csv_file(self.filename, [str(max_fitness), utils.convert_index_to_moves(best_child)])
			#if it % 1 == 0:
			#	tqdm.write('Num extra moves added: ' + str(self.num_extra_moves))
			#	tqdm.write("Max fitness: " + str(max_fitness))
			#	tqdm.write("Best child: " + utils.convert_moves_to_prime_convention(utils.convert_index_to_moves(best_child)))
			if max_fitness >= 54:
				return utils.convert_index_to_moves(best_child), it
			# Evolve and save new population
			self.population = self.evolve(child_fitness)
		return utils.convert_index_to_moves(best_child), self.iterations
	
	def evolve(self, child_fitness):
		# Evolve
		# Selection (Tournament selection)
		selected = self.selection_roulette_wheel(child_fitness, self.population)
		#selected = self.population
		#print([utils.convert_moves_to_prime_convention(utils.convert_index_to_moves(child)) for child in selected])
		#print("Length: ", [len(utils.convert_index_to_moves(child)) for child in selected])
		#print("Fitness: ", self.fitness(selected))
		# Add random move
		extra_move = deepcopy(selected)
		extra_move = [child + [utils.get_random_move() for i in range(self.num_extra_moves)] for child in extra_move]
		best_children = self.evaluate(selected, extra_move)

		# Crossover
		crossover = self.crossover(best_children)
		best_children = self.evaluate(best_children, crossover)
		
		# Mutate
		mutate = self.mutate(best_children)
		best_children = self.evaluate(best_children, mutate)

		return best_children

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

	def selection_roulette_wheel(self, fitness, pop):
		#Picking the 20% best players
		n = int(self.pop_size*0.2)
		selection_idx = utils.max_n_elements_index(fitness, n)
		selection = []
		for select in selection_idx:
			selection.append(pop[select])
		#selection = np.asarray(selection)

		# Rest of population is picked by roulette wheel and merged with the 20% best
		choices = random.choices(pop, weights=fitness, k=self.pop_size-n)
		return_pop = selection
		for choice in choices:
			return_pop.append(choice)
		np.random.shuffle(return_pop)
		return return_pop

	def crossover(self, selected):
		# Crossover
		crossover = []
		for i in range(0, self.pop_size, 2):
			if np.random.rand() < self.crossover_rate:
				# select crossover point that is not on the end of the string
				#pt = np.random.randint(1, self.chromosone_length-2)
				pt1 = int(len(selected[i])/2)
				pt2 = int(len(selected[i+1])/2)
				# perform crossover
				#crossover.append(np.hstack((selected[i][:pt], selected[i+1][pt:])))
				#crossover.append(np.hstack((selected[i+1][:pt], selected[i][pt:])))
				crossover.append(selected[i][:pt1] + selected[i+1][pt2:])
				crossover.append(selected[i+1][:pt2] + selected[i][pt1:])
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
					c = utils.get_random_move()
			mutate.append(child)
		return mutate

	def fitness(self, pop):
		# Calculate fitness
		child_fitness = []
		for child in pop:
			#self.child_cube.setState(self.cube.getState())
			self.child_cube = deepcopy(self.cube)
			self.child_cube.moves_idx(child, detectSolved=True)
			child_fitness.append(self.child_cube.completeness())
		return child_fitness

	def evaluate(self, pop1, pop2):
		# Evaluates two population children wise. Returns the best children from each population
		new_pop = []
		fitness_pop1 = self.fitness(pop1)
		fitness_pop2 = self.fitness(pop2)
		for i in range(len(fitness_pop1)):
			if fitness_pop1[i] > fitness_pop2[i]:
				new_pop.append(pop1[i])
			elif fitness_pop1[i] < fitness_pop2[i]:
				new_pop.append(pop2[i])
			else:
				# Same fitness, return shortest
				new_pop.append(utils.get_shortest_solution(pop1[i], pop2[i]))
		return new_pop

def run_multiprocessing(args):
	# args = [crossover_rate, mutation_rate, cr_mr_path, i, scramble, test_scramble]
	crossover_rate = args[0]
	mutation_rate = args[1]
	cr_mr_path = args[2]
	i = args[3]
	scramble = args[4]
	test_scramble = args[5]
	filename = os.path.join(cr_mr_path,"test_"+str(i)+"_"+str(test_scramble)+".csv")
	ga = GA(pop_size=100, chromosone_length=1, crossover_rate=crossover_rate, mutation_rate=mutation_rate, iterations=10, scramble=scramble, filename=filename)
	start_time = time.time()
	best_solution, num_of_generation = ga.run()
	completion_time = time.time() - start_time
	utils.write_csv_file(filename, ["Completion time", "Solution", "Generations", "Scramble"])
	utils.write_csv_file(filename, [str(completion_time), best_solution, str(num_of_generation), scramble])

if __name__ == "__main__":
	# Loading the 10 scrambles.
	'''
	for i in range(10):
		utils.write_csv_file("scrambles.txt", [Cube().scramble()])	
	'''	
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
				with Pool(os.cpu_count()-1) as pool:
					pool.map(run_multiprocessing, [[crossover_rate, mutation_rate, cr_mr_path, i, scramble, test_scramble] for test_scramble in range(30)])
				#for test_scramble in range(30):
				#	filename = os.path.join(cr_mr_path,"test_"+str(i)+"_"+str(test_scramble)+".csv")
				#	ga = GA(pop_size=100, chromosone_length=1, crossover_rate=crossover_rate, mutation_rate=mutation_rate, iterations=300, scramble=scramble, filename=filename)
				#	start_time = time.time()
				#	best_solution, num_of_generation = ga.run()
				#	completion_time = time.time() - start_time
				#	utils.write_csv_file(filename, ["Completion time", "Solution", "Generations", "Scramble"])
				#	utils.write_csv_file(filename, [str(completion_time), best_solution, str(num_of_generation), scramble])
