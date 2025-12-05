import sys
import time

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = {
        "spans": set(),
        "ingredients": set()
    }

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                numbers = line.strip().split("-")
                if len(numbers) == 1:
                    data["ingredients"].add(int(numbers[0]))
                else:
                    data["spans"].add((int(numbers[0]), int(numbers[1])))
    
    return data

def part1(data):
    """Solve part 1."""
    total = 0

    spans = data["spans"]
    ingredients = data["ingredients"]

    for ingredient in ingredients:
        for span in spans:
            if ingredient in range(span[0], span[1]+1):
                total += 1
                break   # No need to check all the spans once we've found a matching span

    return total

def part2(data):
    """Solve part 2."""
    # Sort the spans by their lowest number
    spans = sorted(data["spans"], key=lambda x: x[0])

    # Set for holding new merged spans built from span overlap
    merged_spans = set()

    # Initialize span comparison with the first one in the list
    current_start, current_end = spans[0]

    # For all remaining spans, check for overlap
    for span in spans[1:]:
        next_start, next_end = span
        if next_start <= (current_end + 1):
            # Keep building the merged span
            current_end = max(current_end, next_end)
        else:
            # Save the merged span and start the next one
            merged_spans.add((current_start, current_end))
            current_start, current_end = next_start, next_end
    
    # When we run out of spans to compare, we still have one waiting to be saved
    merged_spans.add((current_start, current_end))

    # Since the ranges are inclusive, remember the +1 after subtraction
    return sum(span[1] - span[0] + 1 for span in merged_spans)

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