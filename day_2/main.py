"""
This script helps Elves to find invalid IDs in their gift shop computer.
"""
import os
import re

def solve(ranges: list[str]) -> int:
    """
    Finds invalid IDs in input.
    """
    # half of number - other halg should be zero
    result = 0
    for r in ranges:
        r = r.split('-')
        for i in range(int(r[0]), int(r[1])+1):
            if len(str(i))%2 == 0:
                middle = int(len(f'{i}')/2)
                if int(f'{i}'[0:middle]) - int(f'{i}'[middle::]) == 0:
                    result += i

    return result

def solve_part_two(ranges: list[str]) -> int:
    """
    Finds more invalid IDs in input.
    """
    result = 0
    for r in ranges:
        r = r.split('-')
        for i in range(int(r[0]), int(r[1])+1):
            if re.match(r'^(\d+)(\1){1,}$', f'{i}'):
                result += i

    return result


if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().split(',')
        print(f'Solving {filename}.txt')
        print(f'Result for part one is: {solve(data)}')
        print(f'Result for part two is: {solve_part_two(data)}\n')
