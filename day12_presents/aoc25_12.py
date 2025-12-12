import sys
import time
import re

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

def parse(file_name):
    """Parse input"""
    data = {
        "boxes": {},
        "trees": []
    }

    # First just get the stuff out of the file
    with open(file_name) as f:
        mode = "boxes"
        box_idx = 0
        box_area = 0

        for line in f:
            if mode == "boxes":
                if line.strip() == "---":   # slightly modified input for easier parsing
                    mode = "trees"
                if line != "\n":
                    box_area += len(re.findall(r"#", line))
                else:
                    data["boxes"][box_idx] = box_area
                    box_idx += 1
                    box_area = 0
            else:
                if line != "\n":
                    tree_dimensions = [int(n) for n in re.findall(r"\d+", line.split(":")[0])]
                    trea_area = tree_dimensions[0] * tree_dimensions[1]
                    box_counts = [int(n) for n in re.findall(r"\d+", line.split(":")[1])]
                    data["trees"].append((trea_area, box_counts))
    
    return data

def part1(data):
    """Solve part 1."""
    # Comparing the simple area of the tree to the summed area of the combined presents doesn't
    # work for the example input, but it does work for the real input, lmao.
    boxes = data["boxes"]
    trees = data["trees"]
    total = 0

    for tree in trees:
        max_area = tree[0]
        present_area = 0
        for box_idx, present_count in enumerate(tree[1]):
            present_area += boxes[box_idx] * present_count
        if max_area >= present_area:
            total += 1

    return total

def part2(data):
    """Solve part 2."""
    return "There is no part 2. Tada!"

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