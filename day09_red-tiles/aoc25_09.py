import sys
import time
import re
import itertools
from shapely.geometry import Polygon, box

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

def parse(file_name):
    """Parse input"""
    data = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                coords = re.findall(r"\d+", line)
                point = tuple([int(x) for x in coords])
                data.append(point)
    
    return data

def rect_area(point_a, point_b):
    width = abs(point_a[0] - point_b[0]) + 1
    height = abs(point_a[1] - point_b[1]) + 1
    return width * height

def part1(data):
    """Solve part 1."""
    largest_area = 0

    rect_areas = []

    for tile_a, tile_b in itertools.combinations(data, 2):
        area = rect_area(tile_a, tile_b)
        rect_areas.append((tile_a, tile_b, area))
        if area > largest_area:
            largest_area = area

    return largest_area, rect_areas

def part2(data, rect_areas):
    """Solve part 2."""
    polygon = Polygon(data)
    largest_area = 0

    rect_areas = sorted(rect_areas, reverse=True, key=lambda x: x[2])

    for rect_area in rect_areas:
        tile_a = rect_area[0]
        tile_b = rect_area[1]
        x1, x2 = sorted([tile_a[0], tile_b[0]])
        y1, y2 = sorted([tile_a[1], tile_b[1]])
        rectangle = box(minx=x1, miny=y1, maxx=x2, maxy=y2)
        if polygon.covers(rectangle):
            largest_area = rect_area[2]
            break
    
    return largest_area

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1, rect_areas = part1(puzzle_input)
    solution2 = part2(puzzle_input, rect_areas)

    return solution1, solution2

if __name__ == "__main__":
    time_start = time.perf_counter()
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print(f"Solved in {time.perf_counter()-time_start:.5f} seconds")