"""
Picks the right batteries from bank.
"""

import os
from itertools import combinations

def solve(banks: list[str]) -> int:
    """
    Helps you to pick best batteries in the bank
    """
    total : int = 0
    for i in banks:
        il : list[int] = [int(j) for j in i]
        max_val : int = max(il)
        max_a : None | int = None
        max_b : None | int = None

        sublist_a : list[int] = il[:il.index(max_val)]
        sublist_b : list[int] = il[il.index(max_val)+1:]
        
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


def solve_part_two(banks : list[str]) -> int:
    """
    Helps you find 12 batteries for best joltage.
    """
    total : int = 0

    def recursive_search(battery_bank : str, number : str = "") -> str:
        """
        Calculates frame of search in battery bank and searches for best battery,
        then drops the rest. Repeats self until 12 digit number is produced.

        Args:
            battery_bank : str = string of digits describing batteries in the bank
                                length needs to be 12 or more, otherwise fnc returns
                                the number.

            number : str = empty string by default, is populated by biggest digits in
                           battery bank and returned in the end.

        """

        if len(number) >= 12 or len(battery_bank) == 0:
            return number
        
        digits_needed = 12 - len(number)
        if len(battery_bank) == digits_needed:
            return number + battery_bank
        
        cursor_length : int = len(battery_bank) - digits_needed + 1

        frame_max : str = max(battery_bank[:cursor_length])
        number += frame_max
        battery_bank = battery_bank[battery_bank.index(frame_max) + 1:]

        return recursive_search(battery_bank, number)

    
    for bank in banks:
        total += int(recursive_search(bank))

    return total

        


if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
        print(f'Solving {filename}.txt')
        print(f'Result for part one is: {solve(data)}')
        print(f'Solving {filename}.txt')
        print(f'Result for part two is: {solve_part_two(data)}')        