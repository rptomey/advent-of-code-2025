import sys
import os
import time
import re
import copy

# Add the parent directory to sys.path so we can find aoc_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import my helper functions, if needed
from aoc_utils.span_methods import merge_spans
from aoc_utils.distance_methods import point_to_point_distance as p_dist

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                levels = re.split(r"\s+", line.strip())
                report = [int(x) for x in levels]
                data.append(report)
    
    return data

def part1(data):
    """Solve part 1."""
    pass

def part2(data):
    """Solve part 2."""
    pass

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    time_start = time.perf_counter()
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print(f"Solved in {time.perf_counter()-time_start:.5f} seconds")