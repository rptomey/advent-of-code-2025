import sys
import time
import re
import copy
from collections import defaultdict

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = {
        "start": [],
        "splitters": []
    }

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                chars = list(line.strip())
                if "S" in chars:
                    data["start"].append(chars.index("S"))
                else:
                    indices = [i for i, val in enumerate(line) if val == "^"]
                    if len(indices) > 0:
                        data["splitters"].append(indices)
    
    return data

def part1(data):
    """Solve part 1."""
    total = 0
    beams = set(data["start"])
    splitters = data["splitters"]

    for row in splitters:
        temp_beams = copy.deepcopy(beams)
        for splitter in row:
            if splitter in beams:
                temp_beams.remove(splitter)
                temp_beams.add(splitter-1)
                temp_beams.add(splitter+1)
                total += 1
        beams = temp_beams

    return total

def part2(data):
    """Solve part 2."""
    # Initialize: A dictionary of { column_index: count_of_particles }
    # We start with 1 particle at the start index.
    beam_counts = defaultdict(int)
    for start_pos in data["start"]:
        beam_counts[start_pos] = 1

    splitters = data["splitters"]

    # Process row by row
    for row_indices in splitters:
        # Create a FRESH dictionary for the next row. 
        # We don't want to keep history, only where they land next.
        new_counts = defaultdict(int)
        
        # Iterate through where the beams ARE, not where the splitters are.
        for col, count in beam_counts.items():
            
            if col in row_indices:
                # HIT A SPLITTER:
                # The entire pile of particles ('count') splits left and right.
                new_counts[col - 1] += count
                new_counts[col + 1] += count
            else:
                # EMPTY SPACE:
                # The entire pile of particles falls straight down.
                new_counts[col] += count
        
        # Update the state for the next iteration
        beam_counts = new_counts
    
    return sum(beam_counts.values())


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