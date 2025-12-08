import sys
import time
import re
import copy

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse_1(file_name):
    """Parse input"""
    data = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                values = re.findall(r"(\d+|\*|\+)", line)
                if values[0] not in ["*", "+"]:
                    values = [int(n) for n in values]
                data.append(values)
    
    return data

def parse_2(file_name):
    """Parse input"""
    data = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                data.append(list(line.strip("\n")))
    
    return data

def part1(data):
    """Solve part 1."""
    total = 0
    equation_count = len(data[0])
    numbers = data[:-1]     # Everything up to the last row in the input is numbers
    row_count = len(numbers)
    operators = data[-1]    # The last row, however, is mathematical operators

    for i in range(equation_count):
        subtotal = numbers[0][i]
        operator = operators[i]
        for j in range(1,row_count):
            if operator == "*":
                subtotal *= numbers[j][i]
            else:
                subtotal += numbers[j][i]
        total += subtotal

    return total

def part2(data):
    """Solve part 2."""
    total = 0
    number_lines = data[:-1]
    row_count = len(number_lines)
    operator_line = data[-1]
    line_length = len(operator_line)
    operator_indices = []
    for index, operator in enumerate(operator_line):
        if operator in ["*", "+"]:
            operator_indices.append(index)
    equation_index_spans = []
    for i in range(len(operator_indices[:-1])):
        low = operator_indices[i]
        high = operator_indices[i+1] - 2
        equation_index_spans.append((low, high))
    equation_index_spans.append((operator_indices[-1], line_length-1))
    for i in range(len(operator_indices)):
        operator_index = operator_indices[i]
        operator = operator_line[operator_index]
        span = equation_index_spans[i]
        numbers = []
        for j in range(span[0],span[1]+1):
            temp = []
            for k in range(row_count):
                temp.append(number_lines[k][j])
            numbers.append(int("".join(temp)))
        subtotal = numbers[0]
        for n in numbers[1:]:
            if operator == "*":
                subtotal *= n
            else:
                subtotal += n
        total += subtotal

    return total

def solve(puzzle_input_1, puzzle_input_2):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input_1)
    solution2 = part2(puzzle_input_2)

    return solution1, solution2

if __name__ == "__main__":
    time_start = time.perf_counter()
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input_1 = parse_1(path)
        puzzle_input_2 = parse_2(path)
        solutions = solve(puzzle_input_1, puzzle_input_2)
        print("\n".join(str(solution) for solution in solutions))
        print(f"Solved in {time.perf_counter()-time_start:.5f} seconds")