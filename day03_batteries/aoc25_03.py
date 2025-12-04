import sys
import time

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

def parse(file_name):
    """Parse input"""
    banks = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                # Convert string of digits into a list of integers to allow numerical comparison
                bank = [int(x) for x in list(line.strip())]
                banks.append(bank)
    
    return banks

def get_largest_joltage(bank, count):
    # This function uses a greedy approach: Pick the largest available digit 
    # for the current position, provided strictly enough digits remain to fill the rest.
    batteries = []
    min_index = 0

    # Continue until we have selected the required number of batteries
    while len(batteries) < count:
        # Calculate how many digits we need to reserve for future iterations
        positions_held = count - len(batteries) - 1

        # Slice the bank to start from the index after the previously selected battery
        bank = bank[min_index:]

        # Determine the search window. We cannot select a digit from the very end
        # if we still need to fill 'positions_held' slots after this one.
        if positions_held > 0:
            sub_bank = bank[0:-positions_held]
        else:
            # If this is the last digit we need, we can search the entire remainder
            sub_bank = bank[0:]

        # Greedy choice: Find the maximum digit within the valid search window
        battery = max(sub_bank)
        batteries.append(battery)

        # Update index to ensure the next selection appears *after* this one in the original list
        min_index = bank.index(battery)+1

    # Join the selected digits to form the final joltage number
    return int("".join(str(n) for n in batteries))

def part1(data):
    """Solve part 1."""
    total = 0

    for bank in data:
        # Calculate max joltage using exactly 2 batteries per bank
        total += get_largest_joltage(bank, 2)
    
    return total

def part2(data):
    """Solve part 2."""
    total = 0

    for bank in data:
        # Calculate max joltage using exactly 12 batteries per bank
        total += get_largest_joltage(bank, 12)
    
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