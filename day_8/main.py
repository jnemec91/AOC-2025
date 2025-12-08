"""
Solves light connection of junction boxes
"""

import os
import math
import time
from typing import Self

class Point:
    """
    Represents point in 3D space.
    """
    def __init__(self, x,y,z):
        self.x : int = x
        self.y : int = y
        self.z : int = z
        self.distances : dict[float, Point] = {}
        self.in_circuit : Circuit = None

    def __str__(self) -> str:
        return f'Point{self.x, self.y, self.z}'

    def __repr__(self) -> str:
        return f'Point{self.x, self.y, self.z}'

    def calculate_distance(self, point) -> Self:
        """
        Calculates distance to another point using euclidian distance formula.
        """
        p1, p2, p3 = point.x, point.y, point.z
        q1, q2, q3 = self.x, self.y, self.z

        distance = round(math.sqrt((p1 - q1)**2 + (p2 - q2)**2 + (p3 - q3)**2), 3)

        self.distances[distance] = point

        return self

    def get_closest(self) -> int | None:
        """
        Returns shortest distance to neighbour or none if nothing is in distances dict.
        """
        keys : list[float] = [i for i in self.distances]

        if len(keys) == 0:
            return None

        return min(keys)

class Circuit:
    """
    Represents set of points. 
    """
    def __init__(self) -> None:
        self.points : list[Point] = []

    def __repr__(self) -> str:
        return f'Circuit_l_{len(self.points)}{[str(i) for i in self.points]}\n'

def solve(points : list[list[int]]) -> list[Circuit]:
    """
    Connects circuits.
    """
    start : time.time = time.time()
    circuits : list[Circuit] =  []

    for i, point in enumerate(points):
        points[i] = Point(*point)

    for point in points:
        for other_point in points:
            if point != other_point:
                point.calculate_distance(other_point)


    for iteration in range(0, 1000):
        if math.floor(iteration/10)%1 == 0:
            os.system('cls')
            print(f'Progress: { math.floor(iteration/10) * '■' }{(100-math.floor(iteration/10)) *' '} {math.floor(iteration/10)}% running: {round((time.time() - start), 2)}s') #pylint:disable=C0301

        smallest_distance : float | None = None
        smallest_distance_points : tuple[Point] | None = None    

        for point in points:
            point_smallest = point.get_closest()
            if point_smallest is None:
                continue

            if smallest_distance is None:
                smallest_distance = point.get_closest()
                smallest_distance_points = point, point.distances[point.get_closest()]

            if  point_smallest < smallest_distance:
                smallest_distance = point.get_closest()
                smallest_distance_points = point, point.distances[point.get_closest()]


        if smallest_distance_points[0].in_circuit is None and smallest_distance_points[1].in_circuit is None: #pylint:disable=C0301
            c = Circuit()
            for i in smallest_distance_points:
                c.points.append(i)
                i.in_circuit = c
            circuits.append(c)

        elif smallest_distance_points[0].in_circuit is not None and smallest_distance_points[1].in_circuit is None: #pylint:disable=C0301
            c = smallest_distance_points[0].in_circuit
            c.points.append(smallest_distance_points[1])
            smallest_distance_points[1].in_circuit = c

        elif smallest_distance_points[1].in_circuit is not None and smallest_distance_points[0].in_circuit is None: #pylint:disable=C0301
            c = smallest_distance_points[1].in_circuit
            c.points.append(smallest_distance_points[0])
            smallest_distance_points[0].in_circuit = c

        elif smallest_distance_points[0].in_circuit is not None and smallest_distance_points[1].in_circuit is not None: #pylint:disable=C0301
            circuit1 = smallest_distance_points[0].in_circuit
            circuit2 = smallest_distance_points[1].in_circuit

            if circuit1 != circuit2:
                for point in circuit2.points:
                    circuit1.points.append(point)
                    point.in_circuit = circuit1
                circuits.remove(circuit2)

        for i in smallest_distance_points:
            i.distances.pop(smallest_distance)

    for point in points:
        if point.in_circuit is None:
            c = Circuit()
            c.points.append(point)
            circuits.append(c)

    return circuits

if __name__ == '__main__':
    os.system('cls')
    for filename in ['input']:
        with open(
        os.path.join(os.path.dirname(__file__), 'inputs', f'{filename}.txt'), 'r', encoding='UTF-8'
        ) as file:
            data = file.read().splitlines()
            data = [[int(a) for a in i.split(',')] for i in data]

            cc = solve(data)
            cc.sort(key=lambda x: len(x.points), reverse=True)

            total = len(cc[0].points) * len(cc[1].points) * len(cc[2].points)
            print(f'Result for part 1 is: {total}')
