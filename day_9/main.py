"""
Solves Movie Theater floor tiles puzzle.
"""

import os
from itertools import combinations

def solve(points : list[tuple[int,int]]) -> int:
    """
    finds biggest rectangle between two points in input
    """
    # Creating a set to store the points for efficient lookup
    point_set = set(map(tuple, points))
    possible_rects = combinations(point_set, 2)
    max_area = 0

    for rect in possible_rects:
        # determine other two points
        x1,y1 = rect[0]
        x2, y2 = rect[1]
        rect = ((x1,y1), (x2, y1), (x2,y2), (x1, y2))

        # calculate area
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        area = width * height

        if area > max_area:
            max_area = area

    return max_area


if __name__ == '__main__':
    os.system('cls')
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data_part_1 = [[int(j) for j in i.split(',')] for i in data]

            print(f'Solving {filename}.txt')
            print(f'Solution for part one is {solve(data_part_1)}.\n')
