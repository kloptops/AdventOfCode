"""
--- Day 11: Cosmic Expansion ---

You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

    ...#......
    .......#..
    #.........
    ..........
    ......#...
    .#........
    .........#
    ..........
    .......#..
    #...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

       v  v  v
     ...#......
     .......#..
     #.........
    >..........<
     ......#...
     .#........
     .........#
    >..........<
     .......#..
     #...#.....
       ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

    ....#........
    .........#...
    #............
    .............
    .............
    ........#....
    .#...........
    ............#
    .............
    .............
    .........#...
    #....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

    ....1........
    .........2...
    3............
    .............
    .............
    ........4....
    .5...........
    ............6
    .............
    .............
    .........7...
    8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

    ....1........
    .........2...
    3............
    .............
    .............
    ........4....
    .5...........
    .##.........6
    ..##.........
    ...##........
    ....##...7...
    8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

"""
from util import *


def manhattan_distance(coord_a, coord_b):
    return (
        abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1]))


def load_galaxy(in_data):
    galaxy_id = 0
    galaxy_map = {}

    for y, line in enumerate(in_data):
        for x, char in enumerate(line.strip()):
            if char == '#':
                galaxy_map[(x, y)] = galaxy_id
                galaxy_id += 1
        max_x = x
    max_y = y

    galaxy_map['max_x'] = max_x + 1
    galaxy_map['max_y'] = max_y + 1

    return galaxy_map


def iter_coords(galaxy_map):
    return [
        coord
        for coord in galaxy_map.keys()
        if not isinstance(coord, str)]


def iter_col(galaxy_map, x):
    return [
        (x, y)
        for y in range(galaxy_map['max_y'])
        if (x, y) in galaxy_map]


def iter_row(galaxy_map, y):
    return [
        (x, y)
        for x in range(galaxy_map['max_x'])
        if (x, y) in galaxy_map]


def expand_universe(galaxy_map, amount=1):
    expand_y = []
    new_y = 0
    for y in range(galaxy_map['max_y']):
        if len(iter_row(galaxy_map, y)) == 0:
            new_y += amount

        expand_y.append(new_y)
        new_y += 1

    expand_x = []
    new_x = 0
    for x in range(galaxy_map['max_x']):
        if len(iter_col(galaxy_map, x)) == 0:
            new_x += amount

        expand_x.append(new_x)
        new_x += 1

    # print(expand_x)
    # print(expand_y)
    new_galaxy_map = {}
    for coord, galaxy_id in galaxy_map.items():
        if isinstance(coord, str):
            continue

        new_coord = expand_x[coord[0]], expand_y[coord[1]]
        new_galaxy_map[new_coord] = galaxy_id

    new_galaxy_map['max_x'] = expand_x[-1] + 1
    new_galaxy_map['max_y'] = expand_y[-1] + 1

    return new_galaxy_map


def coord_ctx(coord_a, coord_b):
    if coord_a > coord_b:
        return (coord_b, coord_a)

    return (coord_a, coord_b)


def calc_distances(galaxy_map):
    distances = {}
    total_distance = 0
    galaxy_coords = iter_coords(galaxy_map)

    for a, coord_a in enumerate(galaxy_coords):
        for b, coord_b in enumerate(galaxy_coords[a+1:], a+1):
            # print(f"{a} vs {b} -> {coord_a} vs {coord_b}")

            distance = manhattan_distance(coord_a, coord_b)
            distances[coord_ctx(coord_a, coord_b)] = distance
            # print(f"{coord_a}, {coord_b}: {distance}")
            total_distance += distance

    return total_distance


def process(galaxy_map):
    total_a = 0
    total_b = 0

    ## Do something here.
    galaxy_a = expand_universe(galaxy_map)

    total_a = calc_distances(galaxy_a)

    ## Do something here.
    galaxy_b = expand_universe(galaxy_map, 999_999)

    total_b = calc_distances(galaxy_b)

    return total_a, total_b


def main():
    galaxy_map = load_galaxy(load_data('input_011.txt'))

    results = process(galaxy_map)

    print(results[0], '==', 9805264)
    print(results[1], '==', 779032247216)


if __name__ == '__main__':
    main()
