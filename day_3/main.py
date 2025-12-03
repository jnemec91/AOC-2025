"""
Picks the right batteries from bank.
"""

import os

def solve(banks: list[str]) -> int:
    """
    Helps you to pick best batteries in the bank
    """
    total : int = 0
    for i in banks:
        il : list = [int(j) for j in i]
        max_val : int = max(il)
        max_a : None | int = None
        max_b : None | int = None

        sublist_a : list = il[:il.index(max_val)]
        sublist_b : list = il[il.index(max_val)+1:]
        
        if len(sublist_a) > 0:
            max_a = max(sublist_a)
        if len(sublist_b) > 0:
            max_b = max(sublist_b)
        
        if max_b is None:
            total += int(f'{max_a}{max_val}')
            # print(f'adding {max_a}{max_val}')
        else:
            total += int(f'{max_val}{max_b}')
            # print(f'adding {max_val}{max_b}')

    return total





if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
        print(f'Solving {filename}.txt')
        print(f'Result for part one is: {solve(data)}')