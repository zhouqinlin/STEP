from common import format_tour, read_input

import solver_greedy
import solver_random
import solver_mst

CHALLENGES = 8


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        for solver, name in ((solver_random, 'random'), (solver_greedy, 'greedy'), (solver_mst, 'mst')):
            tour = solver.solve(cities)
            with open(f'sample/{name}_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    generate_sample_output()
