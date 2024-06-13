import random
import math
import numpy as np
from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(tour, dist):
    return sum(dist[tour[i]][tour[i+1]] for i in range(len(tour)-1)) + dist[tour[-1]][tour[0]]

def create_initial_population(pop_size, num_cities, dist):
    population = []
    for _ in range(pop_size):
        tour = list(range(num_cities))
        random.shuffle(tour)
        population.append([total_distance(tour, dist), tour])
    return population


def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]

    # Fill the child with the remaining cities
    j = 0
    for i in range(size):
        if child[i] is None:
            while parent2[j] in child:
                j += 1 
            child[i] = parent2[j]
    return child

def mutate(tour, mutation_rate=0.1):
    for i in range(len(tour)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(tour)-1)
            tour[i], tour[j] = tour[j], tour[i]
    return tour

def evolve_population(population, dist, mutation_rate=0.1):
    fitness_values = np.array([1 / p[0] for p in population])
    total_fitness = np.sum(fitness_values)
    selection_probs = fitness_values / total_fitness
    new_population = []
    for _ in range(len(population)):
        parents_idx = np.random.choice(len(population), size=2, p=selection_probs)
        parent1, parent2 = population[parents_idx[0]][1], population[parents_idx[1]][1]
        
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate)
        new_population.append([total_distance(child, dist), child])
    return new_population

def genetic_algorithm(cities, dist):
    num_cities = len(cities)
    pop_size = max(100, 5 * num_cities)
    generations = num_cities * 10
    stagnation_limit = 10
    mutation_rate = 0.05 if num_cities > 50 else 0.1
    
    population = create_initial_population(pop_size, num_cities, dist)
    best_tour = min(population, key=lambda x: x[0])
    best_distance = best_tour[0]
    stagnation_count = 0

    for generation in range(generations):
        population = evolve_population(population, dist, mutation_rate)
        current_best = min(population, key=lambda x: x[0])
        current_best_distance = current_best[0]
        #print(current_best_distance)

        if current_best_distance < best_distance:
            best_tour = current_best
            best_distance = current_best_distance
            stagnation_count = 0
        elif current_best_distance == best_distance:
            stagnation_count += 1

        print(f'Generation {generation}: Best Distance = {best_distance}')

def solve(cities):
    N = len(cities)

    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    best_tour = genetic_algorithm(cities, dist)
    return best_tour



if __name__ == '__main__':
    '''
    filename = 'input_1.csv'
    cities = read_input(filename)
    tour = solve(cities)
    #print_tour(tour)
    filename = 'input_2.csv'
    cities = read_input(filename)
    tour = solve(cities)
    #print_tour(tour)
    filename = 'input_3.csv'
    cities = read_input(filename)
    tour = solve(cities)
    #print_tour(tour)        
    '''

    #filename = 'input_5.csv'
    #cities = read_input(filename)
    #tour5 = solve(cities)

    filename = 'input_6.csv'
    cities = read_input(filename)
    tour6 = solve(cities)
    
    print(tour5)
    print(tour6)