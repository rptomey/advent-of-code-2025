import sys
import time

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

def parse(file_name):
    """Parse input"""
    rotations = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                rotation = (line[0], int(line[1:]))
                rotations.append(rotation)
    
    return rotations

def rotate_dial(position, rotation):
    direction = rotation[0]
    amount = rotation[1]

    if direction == "R":
        position += amount
    else:
        position -= amount

    # Python's % operator actually uses a wrapping behavior for negatives
    # e.g., -5 % 100 becomes 95
    return position % 100

def part1(data):
    """Solve part 1."""
    zeroes = 0
    position = 50

    for rotation in data:
        position = rotate_dial(position, rotation)
        if position == 0:
            zeroes += 1
    
    return zeroes

def part2(data):
    """Solve part 2."""
    zeroes = 0
    position = 50

    for rotation in data:
        direction = rotation[0]
        amount = rotation[1]

        # Add full rotations
        zeroes += amount // 100

        # Check other movements for whether they would pass 0
        remainder = amount % 100
        if direction == "R":
            if position + remainder >= 100:
                zeroes += 1
        else:
            if position > 0 and position - remainder <= 0:
                zeroes += 1
        
        # Still need the new position
        position = rotate_dial(position, rotation)

    return zeroes

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