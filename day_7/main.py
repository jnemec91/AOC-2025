"""
Solve problems with tachyon manifolds
"""

import os
# import time
from typing import Self

class Node:
    """
    Attrs: 
        idx: tuple[int, int] = index location in grid. Used to calculate neighbours in grid.
        neighbours: list[Node | str] = list of neighbours in each of 8 neighnbouring fields
                    in grid.
    """
    def __init__(self, idx : tuple[int, int], is_start_node : bool = False) -> None:
        # neighbours will be a list aranged like so:
        # top-left, top-middle, top-right, left, right, bottom-left, bottom-middle, bottom-right
        self.idx : tuple[int,int] = idx
        self.neighbours : list[str | Node] = []
        self.has_beam = False
        self.is_splitter = False
        self.is_start_node = is_start_node

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

def convert_to_nodes(grid : list[list[str]]) -> tuple[list[list[Node]], Node]:
    """
    Converts list of strings from input to the list of nodes.
    """
    start_node : Node | None = None
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

    return grid, start_node

def solve(grid : list[list[str]]) -> int:
    """
    Solves how light moves thru tachyon manifolds.
    """
    grid, _ = convert_to_nodes(grid)

    total_splitted : int = 0
    for line in grid:
        for column in line:
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
        # os.system('cls')
        # for line in grid:
        #     print("".join([str(i) for i in line]))
        # print(f'Total splits: {total_splitted}')
        # time.sleep(0.01)

    return total_splitted

def solve_part_two(grid: list[list[str]]) -> int:
    """
    finds all possible paths for light to take in tachyon manifolds.
    """
    grid, start_node = convert_to_nodes(grid)

    memo : dict[tuple[int, int], int] = {}

    def go_down(node : Node | str) -> int:
        """
        goes down the paths recursively and caches results of visited paths.
        """
        if not isinstance(node, Node):
            return 0

        if node.idx in memo:
            return memo[node.idx]

        if not node.has_beam:
            node.has_beam = True

        total_paths : int = 0

        if node.is_splitter:
            left, right = node.neighbours[3], node.neighbours[4]
            total_paths += go_down(left) + go_down(right) + 1

        else:
            total_paths = go_down(node.neighbours[6])

        # draw the grid
        # os.system('cls')
        # for line in grid:
        #     print("".join([str(i) for i in line]))
        # print(f'Possible paths: {total_paths +1}, Start node: {repr(start_node)}')
        # print(f'Cached values for {len(memo)} nodes.')
        # time.sleep(0.01)

        memo[node.idx] = total_paths

        return total_paths

    possible_paths = go_down(start_node) + 1 # +1 for starting node

    return possible_paths


if __name__ == '__main__':
    os.system('cls')
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data_part_1 = [[j for j in i] for i in data]
            data_part_2 = [[j for j in i] for i in data]

            print(f'Solving {filename}.txt')
            print(f'Solution for part one is {solve(data_part_1)}')
            print(f'Solution for part two is {solve_part_two(data_part_2)}\n')
