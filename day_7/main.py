import os
import time
from typing import Self

class Node:
    """
    Roll of paper
    
    Attrs: 
        idx: tuple[int, int] = index location in grid. Used to calculate neighbours in grid.
        neighbours: list[RollOfPaper | str] = list of neighbours in each of 8 neighnbouring fields
                    in grid.
    """
    def __init__(self, idx : tuple[int, int], start_node : bool = False) -> None:
        # neighbours will be a list aranged like so:
        # top-left, top-middle, top-right, left, right, bottom-left, bottom-middle, bottom-right
        self.idx : tuple[int,int] = idx
        self.neighbours : list[str | Node] = []
        self.has_beam = False
        self.is_splitter = False
        self.is_start_node = False

    def __repr__(self) -> str:
        return f'Node{self.idx}'

    def __str__(self) -> str:
        if self.is_start_node:
            return 'S'
        elif self.is_splitter:
            return '^'
        elif self.has_beam:
            return '|'
        else:
            return '.'

    def get_neighbours(self, grid : list[str]) -> Self:
        """
        Gets neighbours from the grid.
        Params:
            grid : list[list[str]] = 2D array, representing rancks with rolls of paper on them
        """
        self.neighbours = [] # reset neighbours
        directions : list[tuple[int, int]] = [
                (self.idx[0] - 1, self.idx[1] - 1), # top left
                (self.idx[0], self.idx[1] - 1), # top middle
                (self.idx[0] + 1, self.idx[1] - 1), # top right
                (self.idx[0] - 1, self.idx[1]), # left
                (self.idx[0] + 1, self.idx[1]), # right
                (self.idx[0] - 1, self.idx[1] + 1), # bottom left
                (self.idx[0], self.idx[1] + 1), # bottom middle
                (self.idx[0] + 1, self.idx[1] + 1), # bottom right
            ]

        for direction in directions:
            try:
                if direction[0] < 0 or direction[1] < 0:
                    raise IndexError
                self.neighbours.append(grid[direction[1]][direction[0]])

            except IndexError:
                self.neighbours.append('_')

        return self

def solve(grid):
    os.system('cls')
    start_node : None | Node = None
    # Convert initial grid to Node objects
    for il, line in enumerate(grid):
        for ic, column in enumerate(line):
            grid[il][ic] = Node((ic, il))
            if column == 'S':
                grid[il][ic].is_start_node = True
                start_node = grid[il][ic]
                start_node.has_beam = True

            elif column == '^':
                grid[il][ic].is_splitter = True

    # Get all neighbours
    for il, line in enumerate(grid):
        for ic, column in enumerate(line):
            if isinstance(column, Node):
                column.get_neighbours(grid)

    total_splitted : int = 0
    for il, line in enumerate(grid):
        os.system('cls')
        for ic, column in enumerate(line):
            if isinstance(column, Node):
                if column.has_beam and not column.is_splitter:
                    if isinstance(column.neighbours[6], Node):
                        column.neighbours[6].has_beam = True
                elif column.has_beam and column.is_splitter:
                    total_splitted += 1
                    left, right = column.neighbours[3], column.neighbours[4]
                    if isinstance(left, Node):
                        left.has_beam = True
                        if isinstance(left.neighbours[6], Node):
                            left.neighbours[6].has_beam = True
                    if isinstance(right, Node):
                        right.has_beam = True

        # draw the grid
        for line in grid:
            print("".join([str(i) for i in line]))
        print(f'Starting at Node: {repr(start_node)} Total splits: {total_splitted}')
        time.sleep(0.01)

    return total_splitted

if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data = [[j for j in i] for i in data]

        print(f'Solving {filename}.txt')
        solution : int = solve(data)
        print(f'Solution for part one is {solution}')