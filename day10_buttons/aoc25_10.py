import sys
import os
import time
import re
import z3
from collections import deque

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
                goal = tuple([False if char == "." else True for char in re.findall(r"\[.+\]", line)[0].strip("[").strip("]")])
                buttons_raw = re.findall(r"\]\s(.+)\s\{", line)[0]
                buttons = [tuple(map(int, m.split(','))) for m in re.findall(r'\(([^)]+)\)', buttons_raw)]
                joltage = re.findall(r"\{.+\}", line)[0]
                data.append((goal, buttons, joltage))
    
    return data

def find_min_presses(goal, buttons):
    # Setup the start representing the state of the lights as a tuple because lists cannot be put in a set (i.e., `visited`)
    # Starting state is all False (lights all off)
    start_state = tuple([False] * len(goal))
    
    # Set up a queue that stores (current_light_configuration, number_of_presses_to_get_here)
    queue = deque([(start_state, 0)])

    # Create a set that prevents us from checking the same state twice and getting stuck in an infinite loop
    visited = set()
    visited.add(start_state)

    while queue:
        # Pop the oldest item from the queue (FIFO)
        current_state, presses = queue.popleft()

        # Check if the state of the lights matches our goal
        if current_state == goal:
            return presses
        
        # Try pressing all of the buttons
        for button in buttons:
            # Make a new state based on what this button did
            # Convert to list temporarily so we can modify, then back to tuple for storage
            new_state_list = list(current_state)

            for light_index in button:
                # Because we used a boolean, toggling a light just means setting it to `not` itself
                new_state_list[light_index] = not new_state_list[light_index]
            
            new_state = tuple(new_state_list)

            # If we haven't seen this configuration before, add it to the queue
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, presses + 1))

    return -1   # Should not happen

def part1(data):
    """Solve part 1."""
    total = 0

    for machine in data:
        goal = machine[0]
        buttons = machine[1]
        total += find_min_presses(goal, buttons)

    return total

def solve_with_z3(buttons, joltage_goal):
    # Initialize the Optimizer
    # Use Optimize() instead of Solver() because we want the fewest possible presses
    optimizer = z3.Optimize()

    # Define variables
    # One integer per button
    # Store in a list to access them by index
    press_counts = [z3.Int(f"b_{i}") for i in range(len(buttons))]

    # Add basic contraints (cannot press a button negative times)
    for p in press_counts:
        optimizer.add(p >= 0)

    # Add system contraints (i.e., the equations)
    num_counters = len(joltage_goal)

    for counter_idx in range(num_counters):
        # Find which buttons affect THIS specific counter
        # If button 'i' has 'counter_idx' in its tuple, we include it in the sum.
        vars_affecting_this_counter = []

        for button_idx, affected_counters in enumerate(buttons):
            if counter_idx in affected_counters:
                vars_affecting_this_counter.append(press_counts[button_idx])
        
        # The sum of presses for these specific buttons must equal the goal for this counter
        # z3.Sum() sums up the z3 variables
        optimizer.add(z3.Sum(vars_affecting_this_counter) == joltage_goal[counter_idx])

    # Set the object (minimize total number of button presses)
    optimizer.minimize(z3.Sum(press_counts))

    # Run the Solver with all of these settings
    if optimizer.check() == z3.sat:
        # Solution found
        model = optimizer.model()

        # Calculate the total presses from the model results
        total_presses = sum(model[p].as_long() for p in press_counts)
        return total_presses
    else:
        # Impossible result
        return 0

def part2(data):
    """Solve part 2."""
    total = 0

    for machine in data:
        buttons = machine[1]
        joltage_goal = [int(n) for n in re.findall(r"\d+", machine[2])]
        total += solve_with_z3(buttons, joltage_goal)

    return total

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