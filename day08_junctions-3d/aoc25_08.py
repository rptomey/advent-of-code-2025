import sys
import os
import time
import re
import networkx as nx
import itertools
from functools import reduce

# Add the parent directory to sys.path so we can find aoc_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aoc_utils.distance_methods import point_to_point_distance as p_dist

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

def parse(file_name):
    """Parse input"""
    data = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                coords = re.findall(r"\d+", line)
                point = tuple([int(x) for x in coords])
                data.append(point)
    
    return data

def try_add_edge(graph, union_find, node_a, node_b, distance):
    # Only adds an edge if they're not already somehow connected through the graph
    # Returning a T/F value facilitates keeping track of the last connections made for part 2
    if union_find[node_a] != union_find[node_b]:
        union_find.union(node_a, node_b)
        graph.add_edge(node_a, node_b, weight=distance)
        return True
    else:
        return False

def part1(data, path):
    """Solve part 1."""
    G = nx.Graph()
    uf = nx.utils.UnionFind()
    
    # Build a graph with all nodes
    G.add_nodes_from(data)

    # Figure out all of the possible connections
    possible_edges = []

    for node_a, node_b in itertools.combinations(data, 2):
        dist = p_dist(node_a, node_b)
        possible_edges.append((dist, node_a, node_b))

    # Sort possible edges by distance (smallest to largest)
    possible_edges.sort(key=lambda x: x[0])

    # Handle only the top N edges (10 for example, 1000 for real input)
    if path == "example.txt":
        top_n_edges = possible_edges[:10]
    elif path == "input.txt":
        top_n_edges = possible_edges[:1000]

    for dist, a, b in top_n_edges:
        try_add_edge(G, uf, a, b, dist)

    # Analyze the circuits and sort them by length
    circuits = list(nx.connected_components(G))
    circuit_sizes = [len(c) for c in circuits]
    circuit_sizes.sort(reverse=True)

    top_3_circuits = circuit_sizes[:3]
    print(f"Top 3 circuit sizes: {top_3_circuits}")

    result = reduce(lambda x, y: x * y, top_3_circuits)

    return result

def part2(data):
    """Solve part 2."""
    G = nx.Graph()
    uf = nx.utils.UnionFind()
    
    # Build a graph with all nodes
    G.add_nodes_from(data)

    # Figure out all of the possible connections
    possible_edges = []

    for node_a, node_b in itertools.combinations(data, 2):
        dist = p_dist(node_a, node_b)
        possible_edges.append((dist, node_a, node_b))

    # Sort possible edges by distance (smallest to largest)
    possible_edges.sort(key=lambda x: x[0])

    # Keep track of which connection just happened while attempting to connect all possible edges
    last_2_connections = []

    for dist, a, b in possible_edges:
        edge_added = try_add_edge(G, uf, a, b, dist)
        if edge_added:
            last_2_connections = [a, b]

    # Multiply the X coordinate from each of the last 2 connections for the answer
    result = reduce(lambda x, y: x[0] * y[0], last_2_connections)

    return result

def solve(puzzle_input, path):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input, path)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    time_start = time.perf_counter()
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input, path)
        print("\n".join(str(solution) for solution in solutions))
        print(f"Solved in {time.perf_counter()-time_start:.5f} seconds")