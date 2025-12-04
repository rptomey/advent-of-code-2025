import sys
import time
# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    rolls = set()

    # First just get the stuff out of the file
    with open(file_name) as f:
        for y, line in enumerate(f):    # y corresponds to row index
            if line.strip():    # Ignore empty lines
                for x, char in enumerate(line.strip()): # x corresponds to column index
                    if char == "@":
                        rolls.add((x,y))
    
    return rolls

def roll_accessible(data, roll):
    # Define 8 neighboring coordinates like so...
    # a b c
    # d @ e
    # f g h
    x,y = roll
    a = (x-1, y-1)
    b = (x, y-1)
    c = (x+1, y-1)
    d = (x-1, y)
    e = (x+1, y)
    f = (x-1, y+1)
    g = (x, y+1)
    h = (x+1, y+1)

    # A roll is accessible if it's next to fewer than 4 other rolls
    neighboring_rolls = 0

    for neighbor in [a,b,c,d,e,f,g,h]:
        if neighbor in data:
            neighboring_rolls += 1
    
    return neighboring_rolls < 4


def part1(data):
    """Solve part 1."""
    total = 0
    
    # Just see how many rolls are accessible
    for roll in data:
        if roll_accessible(data, roll):
            total += 1

    return total

def part2(data):
    """Solve part 2."""
    total = 0
    # Initialize to a safe value that will allow the while loop to happen
    accessible = -1

    # In batches, remove the accessible rolls and count how many were in each batch
    while accessible != 0:
        accessible_rolls = []
        for roll in data:
            if roll_accessible(data, roll):
                accessible_rolls.append(roll)
        accessible = len(accessible_rolls)
        total += accessible
        for roll in accessible_rolls:
            data.remove(roll)

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