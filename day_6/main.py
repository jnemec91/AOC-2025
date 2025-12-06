"""
Solves cephalophod math homework.
"""
import os

def part_two_formater(problem_data : list[str]) -> list[tuple]:
    """
        Arranges numbers in lists by the cephalophod rules.
    """

    all_data : list[tuple[str]]= []

    for i in range(len(problem_data[0])): # expecting all lines to be same lenght
        column_chars : list[str] = []
        for line in problem_data:
            if i < len(line):
                column_chars.append(line[i])

        all_data.append(tuple(column_chars))

    return all_data


def solve(problem_data : list[list[str]]) -> int:
    """
        Formats and evals the problems
    """
    operations : list[str] = problem_data[-1]
    numbers : list[list[str]] = problem_data[:-1]

    total : int = 0
    for i,o in enumerate(operations):
        problem : list[str] = []
        for n in numbers:
            problem.append(n[i])
        total += eval(f'{o}'.join(problem)) # pylint: disable=W0123

    return total

def solve_part_two(problem_data : list[str]) -> int:
    """
        Solves part two of cephalopods math homework
    """
    total : int = 0
    all_data : list[tuple[str]] = part_two_formater(problem_data)

    current_numbers : list[str] = []
    current_operation : None | str = None

    for column_tuple in all_data:
        if all(char == ' ' for char in column_tuple):
            if current_numbers and current_operation:
                total += eval(f'{current_operation}'.join(current_numbers)) # pylint:disable=W0123
                current_numbers = []
                current_operation = None
        else:
            number_chars : tuple[str] = column_tuple[:-1]
            op_char : str = column_tuple[-1]

            current_numbers.append(' '.join(number_chars).replace(' ', ''))

            if op_char != ' ':
                current_operation = op_char

    if current_numbers and current_operation:
        total += eval(f'{current_operation}'.join(current_numbers)) # pylint:disable=W0123

    return total

if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data : list[str] = file.read().splitlines()
            data_splitted : list[list[str]] = [i.split() for i in data]

        print(f'Solving {filename}.txt')

        print(f'Result for part one is: {solve(data_splitted)}')
        print(f'Result for part two is: {solve_part_two(data)}')