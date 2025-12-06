"""
Solves cephalophod math homework.
"""
import os

def solve(problem_data : list[list[str]]) -> int:
    """formats and evals the problems"""
    operations : list[str] = problem_data[-1]
    numbers : list[list[str]] = problem_data[:-1]

    total : int = 0
    for i,o in enumerate(operations):
        problem : list[str] = []
        for n in numbers:
            problem.append(n[i])

        total += eval(f'{o}'.join(problem)) # pylint: disable=W0123

    return total

if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data = [i.split() for i in data]

        print(f'Solving {filename}.txt')
        solution = solve(data)
        print(f'Result for part one is: {solution}')
