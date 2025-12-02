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
    with open(
    os.path.join(os.path.dirname(__file__), 'inputs', 'input.txt'), 'r', encoding='UTF-8'
    ) as file:
        data = file.read().split(',')

    print(solve(data))
    print(solve_part_two(data))