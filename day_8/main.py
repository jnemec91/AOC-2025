#pylint:disable=W0621
"""
Solves light connection of junction boxes. 
"""

import os
import math
import time

class DSU:
    """
    Disjoint Set Union.
    https://www.geeksforgeeks.org/dsa/introduction-to-disjoint-set-data-structure-or-union-find-algorithm/
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.circuits = n

    def find(self, x):
        """Find root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union two sets by rank."""
        root_x, root_y = self.find(x), self.find(y)
        if root_x != root_y:

            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            self.circuits -= 1
            return True
        return False

    def get_circuits_count(self):
        """Get number of connected circuits."""
        return self.circuits

    def get_circuit_sizes(self):
        """Get sizes of all circuits."""
        circuit_size = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            circuit_size[root] = circuit_size.get(root, 0) + 1
        return list(circuit_size.values())


def solve(points : list[list[int]],
          part_two : bool = True,
          iterations : int = 0) -> tuple[list[int], tuple[int, int]]:
    """
    Solves connection of junction boxes using DSU.
    """
    start : time.time = time.time()
    n = len(points)
    dsu = DSU(n)
    last_connected = None

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
            edges.append((distance, i, j))

    edges.sort()

    iteration = 0
    for _, i, j in edges:
        iteration += 1
        if dsu.union(i, j):
            last_connected = (i, j)
            circuits = dsu.get_circuits_count()

            if circuits == 1:
                break

            if not part_two:
                if iteration == iterations:
                    break

    bcs = dsu.get_circuit_sizes()
    bcs.sort(reverse=True)

    print(f'finshed in {round(time.time() - start, 2)}s')
    return bcs, last_connected


if __name__ == '__main__':
    os.system('cls')
    for filename in ['test_input', 'input']:
        print(f'Solving {filename}.txt')
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data = [[int(a) for a in i.split(',')] for i in data]
            for part in [False,True]:
                print(f'Solving {"part one" if not part else "part two"}.')
                if not part:
                    ITERATIONS = 10 if filename == 'test_input' else 1000
                    circuit_sizes, last_connected = solve(data, part, ITERATIONS)

                    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
                    print(f'Biggest three circuits multiplied after {ITERATIONS} = {result}.\n')
                else:
                    circuit_sizes, last_connected = solve(data)

                    if last_connected:
                        i, j = last_connected
                        print(f'Last two points x values multiplied = {data[i][0]*data[j][0]}.\n')
