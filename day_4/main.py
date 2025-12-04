"""
Helps you optimize forklift workflow for rearanging rolls of paper.
"""
import os
from typing import Self
import pygame

class RollOfPaper:
    """
    Roll of paper
    
    Attrs: 
        idx: tuple[int, int] = index location in grid. Used to calculate neighbours in grid.
        neighbours: list[RollOfPaper | str] = list of neighbours in each of 8 neighnbouring fields
                    in grid.
    """
    def __init__(self, idx : tuple[int, int]) -> None:
        # neighbours will be a list aranged like so:
        # top-left, top-middle, top-right, left, right, bottom-left, bottom-middle, bottom-right
        self.idx : tuple[int,int] = idx
        self.neighbours : list[str | RollOfPaper] = []

    def __repr__(self) -> str:
        return f'RollOfPaper{self.idx}'

    def __str__(self) -> str:
        return '#' if self.count_neighbour_rolls() < 4 else "@"

    def get_neighbours(self, grid : list[str]) -> Self:
        """
        Gets neighbours from the grid.
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

    def count_neighbour_rolls(self) -> int:
        """
        counts number of rolls of paper in neighbours
        """
        count : int = 0
        for n in self.neighbours:
            if isinstance(n, RollOfPaper):
                count += 1

        return count



def solve(grid : list[list[str]], cell_size : int = 5) -> int:
    """
    Helps to solve mess in printing department by optimizing workflow for forklifts.
    """
    #pygame setup
    height : int = len(grid)
    width : int = len(grid[0])
    pygame.init() #pylint: disable=no-member
    pygame.display.set_caption("Advent of Code Day 4")
    screen : pygame.Surface = pygame.display.set_mode((width * cell_size, height * cell_size))
    animating : bool = True
    scroll_color : pygame.color = pygame.Color("white")
    empty_color : pygame.color = pygame.Color("darkblue")
    clock : pygame.time.Clock = pygame.time.Clock()

    # Convert initial grid to RollOfPaper objects
    for il, line in enumerate(grid):
        for ic, column in enumerate(line):
            if column  == '@':
                grid[il][ic] = RollOfPaper((ic, il))


    total_movable_rolls : None | int = None
    can_be_removed : int = 0
    first_part : int = 0

    while animating and (total_movable_rolls is None or total_movable_rolls > 0):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #pylint: disable=no-member
                animating = False
                pygame.quit() #pylint: disable=no-member
                return first_part, can_be_removed

        roll_count : int = 0
        to_remove : list[tuple[int, int]] = [] # list of coordinates to rewrite as '.'

        total_movable_rolls = 0

        # recalculate grid
        for il, line in enumerate(grid):
            for ic, column in enumerate(line):
                if isinstance(column, RollOfPaper):
                    column.get_neighbours(grid)
                    roll_count += 1
                    if column.count_neighbour_rolls() < 4:
                        total_movable_rolls += 1
                        to_remove.append((il, ic))

        # update the grid
        for coords in to_remove:
            grid[coords[0]][coords[1]] = '.'

        # draw the grid
        screen.fill(empty_color)
        for il, line in enumerate(grid):
            for ic, column in enumerate(line):
                if isinstance(column, RollOfPaper):
                    pygame.draw.rect(
                        screen, scroll_color, pygame.Rect(
                            ic * cell_size, il * cell_size, cell_size, cell_size
                            )
                        )
                else:
                    pygame.draw.rect(
                        screen, empty_color, pygame.Rect(
                            ic * cell_size, il * cell_size, cell_size, cell_size
                            )
                        )

        can_be_removed += total_movable_rolls
        if first_part == 0:
            first_part = total_movable_rolls

        pygame.display.flip()
        clock.tick(3)

    # Keep window open
    while animating:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #pylint: disable=no-member
                animating = False

    pygame.quit() #pylint: disable=no-member

    return first_part, can_be_removed


if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data = [[j for j in i] for i in data]

        print(f'Solving {filename}.txt')
        solution = solve(data, 15 if filename == 'test_input' else 7)
        print(f'Result for part one is: {solution[0]} and for second part {solution[1]}')
