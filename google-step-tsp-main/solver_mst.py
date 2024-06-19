import sys
import numpy as np
from sklearn.cluster import KMeans
from common import print_tour, read_input
from unionFind import unionFind


def distance(city1, city2):
    return np.linalg.norm(np.array(city1) - np.array(city2))


def total_distance(tour, dist):
    return (
        sum(dist[tour[i], tour[i + 1]] for i in range(len(tour) - 1))
        + dist[tour[-1], tour[0]]
    )


def create_mst(dist, N):
    """Create a minimum spanning tree"""
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            edges.append((dist[i, j], i, j))
    edges.sort()
    uf = unionFind(N)
    mst = [[] for _ in range(N)]

    for w, u, v in edges:
        if not uf.same(u, v) and len(mst[u]) < 2 and len(mst[v]) < 2:
            mst[u].append(v)
            mst[v].append(u)
            uf.unite(u, v)

    one_edge_node = [i for i in range(N) if len(mst[i]) == 1]
    if len(one_edge_node) >= 2:
        mst[one_edge_node[0]].append(one_edge_node[1])
        mst[one_edge_node[1]].append(one_edge_node[0])

    return mst


def create_path(mst, N):
    """Create a path from the minimum spanning tree"""
    visited = set()
    current = 0
    path = [current]
    visited.add(current)

    while len(path) < N:
        next_node = next(n for n in mst[current] if n not in visited)
        visited.add(next_node)
        path.append(next_node)
        current = next_node

    return path


def nearest_neighbor(dist, N):
    """Creat a path by nearest neighbor heuristic"""
    start = 0
    tour = [start]
    unvisited = set(range(1, N))
    current = start

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current, city])
        unvisited.remove(next_city)
        tour.append(next_city)
        current = next_city

    return tour


def solve_cluster_tsp(cities, dist):
    N = len(cities)
    initial_tour = nearest_neighbor(dist, N)
    mst = create_mst(dist, N)
    mst_tour = create_path(mst, N)

    if total_distance(initial_tour, dist) < total_distance(mst_tour, dist):
        tour = initial_tour
    else:
        tour = mst_tour

    return tour


def two_opt(tour, dist):
    """2-opt algorithm to improve the solution"""
    N = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(N - 2):
            for j in range(i + 2, N):
                l1 = dist[tour[i]][tour[i + 1]]
                l2 = dist[tour[j]][tour[(j + 1) % N]]
                l3 = dist[tour[i]][tour[j]]
                l4 = dist[tour[i + 1]][tour[(j + 1) % N]]
                if l1 + l2 > l3 + l4:
                    tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])
                    improved = True
    return tour


def solve(cities):
    N = len(cities)
    cities = np.array(cities)
    dist = np.array(
        [[distance(cities[i], cities[j]) for j in range(N)] for i in range(N)]
    )

    # K-means clustering to divide the cities
    num_clusters = max(1, N // 100)
    kmeans = KMeans(n_clusters=num_clusters)
    labels = kmeans.fit_predict(cities)
    clusters = [np.where(labels == i)[0] for i in range(num_clusters)]

    # Solve TSP for each cluster
    cluster_tours = []
    for cluster in clusters:
        cluster_dist = dist[np.ix_(cluster, cluster)]
        cluster_tour = solve_cluster_tsp(cities[cluster], cluster_dist)
        cluster_tours.append([cluster[i] for i in cluster_tour])

    # Connect clusters
    cluster_centroids = kmeans.cluster_centers_
    cluster_distances = np.array(
        [
            [
                distance(cluster_centroids[i], cluster_centroids[j])
                for j in range(num_clusters)
            ]
            for i in range(num_clusters)
        ]
    )
    cluster_tour_order = solve_cluster_tsp(list(range(num_clusters)), cluster_distances)

    # Combine cluster tours
    final_tour = []
    for cluster_idx in cluster_tour_order:
        final_tour.extend(cluster_tours[cluster_idx])

    final_tour = two_opt(final_tour, dist)
    total_dist = total_distance(final_tour, dist)
    print(f"Total Distance: {total_dist}")

    return final_tour


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


    """
    Total Distance: 10954.096951088139
    Total Distance: 21783.799943343
    Total Distance: 42929.122677414736
    Total Distance: 85373.55021964287
    """
