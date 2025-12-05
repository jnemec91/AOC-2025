"""
Helps find fresh ingredients in cafeteria kitchen
"""
import os

def format_ranges(ranges : list[str]) -> list[tuple[int,int]]:
    """
    Formats a list of strings into list of tuples with two numbers.
    """
    formated_ranges : list[tuple[int, int]] = []

    for i in ranges:
        fresh_range = i.split('-')
        formated_ranges.append((int(fresh_range[0]), int(fresh_range[1])))    

    return formated_ranges

def commbine_overlaps(ranges : list[tuple[int, int]]) -> list[tuple[int,int]]:
    """
    Combines overlaping ranges in ranges list to one.
    """
    try:
        ranges.sort()
        merged : list[tuple[int, int]] = [ranges[0]]

        for current in ranges[1:]:
            last_merged = merged[-1]
            if current[0] <= last_merged[1] + 1:
                merged[-1] = (last_merged[0], max(last_merged[1], current[1]))
            else:
                merged.append(current)

        return merged

    except IndexError:
        return []
    except ValueError:
        return []

def solve(fresh_ranges : list[str], available_ids : list [str]) -> int:
    """
    finds if ids are in fresh ranges
    """
    ranges = format_ranges(fresh_ranges)
    combined_ranges = commbine_overlaps(ranges)

    fresh : int = 0
    for i in available_ids:
        for j in combined_ranges:
            if int(i) in range(j[0], j[1]+1):
                fresh += 1
                break

    return fresh

def solve_part_two(ranges : list[str]) -> int:
    """
    counts all numbers in all ranges.
    """
    ranges = format_ranges(ranges)
    combined_ranges = commbine_overlaps(ranges)

    total_fresh : int = 0
    for i in combined_ranges:
        total_fresh += (i[1]+1)-i[0]

    return total_fresh

def solve_redit_challenge(fresh_ranges : list[str], available_ids : list [str]) -> int:
    """
    finds all of items that are in two or more ranges. Based on post:
    https://www.reddit.com/r/adventofcode/comments/1peyw7w/2025_day_5_part_3_superfresh_ingredients/
    """
    ranges = format_ranges(fresh_ranges)

    fresh : int = 0
    for i in available_ids:
        found_in_ranges : int = 0
        for j in ranges:
            if int(i) in range(j[0], j[1]+1):
                found_in_ranges += 1

                if found_in_ranges >= 2:
                    fresh += 1

    return fresh

if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().split('\n\n')
            input_ranges = data[0].split('\n')
            input_ids = data[1].split('\n')

        print(f'Solving {filename}.txt')
        print(f'Result for part one is: {solve(input_ranges, input_ids)}')
        print(f'Result for part two is: {solve_part_two(input_ranges)}')
        print(f'Result for redit challenge is: {solve_redit_challenge(input_ranges, input_ids)}')
