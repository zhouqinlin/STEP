import sys
from common import print_tour, read_input
from unionFind import unionFind


def distance(city1, city2):
    return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5


def total_distance(tour, dist):
    return (
        sum(dist[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
        + dist[tour[-1]][tour[0]]
    )


# Create a minimum spanning tree
def create_mst(dist, N):
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            edges.append((dist[i][j], i, j))
    edges.sort()
    uf = unionFind(N)
    mst = [[] for i in range(N)]

    for i in range(len(edges)):
        w, u, v = edges[i]
        # Not to create a cycle and not to have more than 2 edges
        if not uf.same(u, v) and len(mst[u]) < 2 and len(mst[v]) < 2:
            mst[u].append(v)
            mst[v].append(u)
            uf.unite(u, v)

    # Connect the two nodes with only one edge
    one_edge_node = []
    for i in range(N):
        if len(mst[i]) == 1:
            one_edge_node.append(i)

    # Check if there are two nodes with only one edge
    if len(one_edge_node) >= 2:
        mst[one_edge_node[0]].append(one_edge_node[1])
        mst[one_edge_node[1]].append(one_edge_node[0])

    return mst


# Create a path from the minimum spanning tree
def create_path(mst, N):
    visited = set()
    current = 0
    path = [current]
    visited.add(current)

    while len(path) < N:
        next_node = mst[current][0]
        if next_node in visited:
            next_node = mst[current][1]
        visited.add(next_node)
        path.append(next_node)
        current = next_node

    return path


# 2-opt algorithm to improve the solution
def two_opt(tour, dist):
    N = len(tour)
    while True:
        count = 0
        for i in range(N - 2):
            for j in range(i + 2, N):
                l1 = dist[tour[i]][tour[i + 1]]
                l2 = dist[tour[j]][tour[(j + 1) % N]]
                l3 = dist[tour[i]][tour[j]]
                l4 = dist[tour[i + 1]][tour[(j + 1) % N]]
                if l1 + l2 > l3 + l4:
                    tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])
                    count += 1
        if count == 0:
            break
    return tour


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    mst = create_mst(dist, N)
    tour = create_path(mst, N)
    tour = two_opt(tour, dist)
    
    total_dist = total_distance(tour, dist)
    print(f"Total Distance: {total_dist}")

    return tour


if __name__ == "__main__":
    # assert len(sys.argv) > 1
    # tour = solve(read_input(sys.argv[1]))

    filename = "input_4.csv"
    tour = solve(read_input(filename))
    filename = "input_5.csv"
    tour = solve(read_input(filename))
    filename = "input_6.csv"
    tour = solve(read_input(filename))
    filename = "input_7.csv"
    tour = solve(read_input(filename))

    '''
    Total Distance: 3832.2900939051997
    Total Distance: 21287.28683474821
    Total Distance: 41821.48026306776
    Total Distance: 82675.98182265929
    '''