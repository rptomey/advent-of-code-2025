import sys
import time
import re
import networkx as nx
import functools

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

@functools.cache
def count_paths(graph, current_node, found_fft, found_dac):
    # Check if we've reached the target
    if current_node == "out":
        # Only count this path if we found both required nodes
        return 1 if found_fft and found_dac else 0
    
    # Update state for current node and see if we're currently at a required node
    new_fft = found_fft or (current_node == "fft")
    new_dac = found_dac or (current_node == "dac")

    # Sum up all valid paths from neighbors
    total_valid = 0
    for neighbor in graph.successors(current_node):
        total_valid += count_paths(graph, neighbor, new_fft, new_dac)

    return total_valid

def part2(graph):
    """Solve part 2."""
    # Unfortunately, there are way too many paths to handle with networkx
    # so we have to use DFS (depth first search) with memoization.

    return count_paths(graph, "svr", False, False)

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