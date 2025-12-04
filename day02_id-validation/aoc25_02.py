import sys
import time
import re

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

def parse(file_name):
    """Parse input"""
    spans = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                for span in line.split(","):
                    span_list = span.split("-")
                    spans.append((int(span_list[0]), int(span_list[1])))
    
    return spans

def part1(data):
    """Solve part 1."""
    total = 0

    for span in data:
        for product_id in range(span[0], span[1]+1):
            if re.match(r"^(.+)\1$", str(product_id)):
                total += product_id
    
    return total

def part2(data):
    """Solve part 2."""
    total = 0

    for span in data:
        for product_id in range(span[0], span[1]+1):
            if re.match(r"^(.+)\1+$", str(product_id)):
                total += product_id
    
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