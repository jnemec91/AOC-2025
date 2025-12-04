"""
Helps you optimize forklift workflow for rearanging rolls of paper.
"""
import os

class RollOfPaper:
    """
    Roll of paper
    
    Should have neighbours on each of eight directions as params.
    Should have method to check if four or less neighbours are rolls.
    """
    def __init__(self, idx : tuple) -> None:
        # index in grid
        # neighbours will be a list aranged like so:
        # top-left, top-middle, top-right, left, right, bottom-left, bottom-middle, bottom-right
        self.idx : tuple[int,int] = idx
        self.neighbours : list[str | RollOfPaper] = []
    
    def __repr__(self) -> str:
        return f'RollOfPaper{self.idx}'
    
    def __str__(self) -> str:
        return '#' if self.count_neighbour_rolls() < 4 else "@"
    
    def get_neighbours(self, grid : list[str]):
        """
        Gets neighbours from the grid.
        """
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
        
        # print(f'Neighbours({len(self.neighbours)}) for {repr(self)} are: {self.neighbours}')

        return self

    def count_neighbour_rolls(self) -> int:
        """
        counts number of rolls of paper in neighbours
        """
        count = 0
        for n in self.neighbours:
            if isinstance(n, RollOfPaper):
                count += 1
        # print(self, count)
        return count



def solve(grid : list[str]) -> int:
    for il, line in enumerate(grid):
        for ic, column in enumerate(line):
            if column  == '@':
                grid[il][ic] = RollOfPaper((ic, il))
    
    total_movable_rolls = 0
    for il, line in enumerate(grid):
        for ic, column in enumerate(line):
            if isinstance(column, RollOfPaper):
                column.get_neighbours(grid)

                if column.count_neighbour_rolls() < 4:
                    total_movable_rolls += 1

    for line in grid:
        print(" ".join([str(i) for i in line]))
    return total_movable_rolls


if __name__ == '__main__':
    for filename in ['test_input', 'input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data = [[j for j in i] for i in data]
        print(f'Solving {filename}.txt')
        print(f'Result for part one is: {solve(data)}')
        # print(f'Result for part two is: {solve_part_two(data)}\n')