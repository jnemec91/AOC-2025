#pylint: disable=W0123
"""
solution to day one challenge of AOC25
"""
import os

class DialSolver:
    """
    Solution for the locked safe dial.

    Init Args:
        instructions: list[str] = pass instructions to dial solver to open a safe. L means left
                      on dial, right meansR means right on dial and number after letter means
                      clicks.

        start: int = starting point on the dial.
    """

    def __init__(self, instructions: list[str], start: int) -> None:
        self.instructions: list[str] = instructions
        self.number: int = start

        # password is number of times dial points at zero
        self.password: int = 0
        self.second_try: int = 0

    def solve(self) -> int:
        """
        solves the dial of elf safe.
        """
        for i in self.instructions:
            n = eval(f"{self.number}{'-' if i[0] == 'L' else '+'}{i[1::]}")%100

            if n == 0:
                self.password += 1

            self.number = n



        return self.password


if __name__ == '__main__':
    with open(
    os.path.join(os.path.dirname(__file__), 'inputs', 'input.txt'), 'r', encoding='UTF-8'
    ) as file:
        data = file.read()

    ds = DialSolver(data.splitlines(), 50)
    solution = ds.solve()
    print(f'Example solution for the first part is {solution}.')