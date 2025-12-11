import sys
import os
import time
import re
import networkx as nx

# Add the parent directory to sys.path so we can find aoc_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import my helper functions, if needed
from aoc_utils.search_methods import dfs

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

def parse(file_name):
    """Parse input"""
    data = {}

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                details = line.split(":")
                device = details[0]
                outputs = re.findall(r"\w+", details[1])
                data[device] = outputs
    
    return data

def part1(data):
    """Solve part 1."""
    G = nx.DiGraph()

    for node in data.keys():
        for out in data[node]:
            G.add_edge(node, out)

    paths = list(nx.all_simple_paths(G, source="you", target="out"))

    return len(paths), G

def part2(graph):
    """Solve part 2."""
    # Unfortunately, there are way too many paths to handle with networkx
    # so we have to use DFS (depth first search) with memoization.

    # Define logic for finding neighbors (also keeping track of fft/dac touch in the path)
    def get_neighbors(state):
        node, has_fft, has_dac = state
        next_states = []

        if node in graph:
            for neighbor in graph.successors(node):
                new_fft = has_fft or (neighbor == "fft")
                new_dac = has_dac or (neighbor == "dac")
                next_states.append((neighbor, new_fft, new_dac))
        
        return next_states
    
    # Define logic that tells the search when the goal is hit
    def is_goal(state):
        node, has_fft, has_dac = state
        return node == "out" and has_fft and has_dac
    
    # Define start state for DFS (start node, whether fft reached, whether dac reached)
    initial_state = ("svr", False, False)

    return dfs(start_state=initial_state, get_neighbors=get_neighbors, is_goal=is_goal, count_mode=True)

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1, graph = part1(puzzle_input)
    solution2 = part2(graph)

    return solution1, solution2

if __name__ == "__main__":
    time_start = time.perf_counter()
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print(f"Solved in {time.perf_counter()-time_start:.5f} seconds")