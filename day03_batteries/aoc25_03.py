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
                bank = [int(x) for x in list(line.strip())]
                banks.append(bank)
    
    return banks

def get_largest_joltage(bank, count):
    batteries = []
    min_index = 0

    while len(batteries) < count:
        positions_held = count - len(batteries) - 1
        bank = bank[min_index:]
        if positions_held > 0:
            sub_bank = bank[0:-positions_held]
        else:
            sub_bank = bank[0:]
        battery = max(sub_bank)
        batteries.append(battery)
        min_index = bank.index(battery)+1

    return int("".join(str(n) for n in batteries))

def part1(data):
    """Solve part 1."""
    total = 0

    for bank in data:
        total += get_largest_joltage(bank, 2)
    
    return total

def part2(data):
    """Solve part 2."""
    total = 0

    for bank in data:
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