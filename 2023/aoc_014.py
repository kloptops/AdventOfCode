"""
--- Day 14: Parabolic Reflector Dish ---

You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....

Start by tilting the lever so all of the rocks will slide north as far as they will go:

    OOOO.#.O..
    OO..#....#
    OO..O##..O
    O..#.OO...
    ........#.
    ..#....#.#
    ..O..#.O.O
    ..O.......
    #....###..
    #....#....

You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

    OOOO.#.O.. 10
    OO..#....#  9
    OO..O##..O  8
    O..#.OO...  7
    ........#.  6
    ..#....#.#  5
    ..O..#.O.O  4
    ..O.......  3
    #....###..  2
    #....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?
"""

from util import *
import hashlib


NORTH = ( 0, -1)
EAST  = (+1,  0)
SOUTH = ( 0, +1)
WEST  = (-1,  0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
REV_DIRECTIONS = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
    }


def adj_coord(coord, adj):
    return (coord[0] + adj[0], coord[1] + adj[1])


def in_parabola(parabola, max_size, coord):
    if not (0 <= coord[0] < max_size[0]):
        return False

    if not (0 <= coord[1] < max_size[1]):
        return False

    return True


def iter_direction(parabola, max_size, coord, direction):
    while True:
        coord = adj_coord(coord, direction)

        if not in_parabola(parabola, max_size, coord):
            return

        yield coord


def map_iter_direction(parabola, max_size, direction):
    if direction == NORTH:
        for y in range(max_size[1]):
            for x in range(max_size[0]):
                yield (x, y)

    elif direction == SOUTH:
        for y in range(max_size[1]-1, -1, -1):
            for x in range(max_size[0]):
                yield (x, y)

    elif direction == EAST:
        for x in range(max_size[0]-1, -1, -1):
            for y in range(max_size[1]):
                yield (x, y)

    else: # direction == 
        for x in range(max_size[0]):
            for y in range(max_size[1]):
                yield (x, y)


def print_map(parabola, max_size):
    print("-" * max_size[0])
    for y in range(max_size[1]):
        print(''.join(
            parabola.get((x, y), '.')
            for x in range(max_size[0])))
    print("-" * max_size[0])
    print()


def load_parabola(in_data):
    parabola_map = {}

    for y, line in enumerate(in_data):
        for x, char in enumerate(line.strip()):
            if char != '.':
                parabola_map[(x, y)] = char

        max_x = x + 1

    max_y = y + 1

    return parabola_map, (max_x, max_y)


def parabola_hash(parabola):
    md5sum = hashlib.md5()
    md5sum.update(str(tuple(sorted(parabola.keys()))).encode('utf-8'))
    return md5sum.hexdigest()


def roll_direction(parabola, max_size, direction):
    for coord in map_iter_direction(parabola, max_size, direction):
        char = parabola.get(coord, None)
        if char == 'O':
            new_coord = coord

            for next_coord in iter_direction(parabola, max_size, coord, direction):
                if next_coord in parabola:
                    break

                new_coord = next_coord

            del parabola[coord]
            parabola[new_coord] = char


def calc_weight(parabola, max_size):
    total = 0
    for coord in map_iter_direction(parabola, max_size, NORTH):
        if parabola.get(coord) == 'O':
            total += max_size[1] - coord[1]

    return total


def process(parabola, max_size):
    total_a = 0
    total_b = 0

    # print_map(parabola, max_size)
    ## Do something here.
    roll_direction(parabola, max_size, NORTH)

    # print_map(parabola, max_size)

    total_a = calc_weight(parabola, max_size)

    roll_direction(parabola, max_size, NORTH)
    roll_direction(parabola, max_size, WEST)
    roll_direction(parabola, max_size, SOUTH)
    roll_direction(parabola, max_size, EAST)

    hash_map = {}

    cycle = 1
    cycle_diff = None

    phash = parabola_hash(parabola)
    hash_map[phash] = cycle

    while cycle < 1_000_000_000:
        roll_direction(parabola, max_size, NORTH)
        roll_direction(parabola, max_size, WEST)
        roll_direction(parabola, max_size, SOUTH)
        roll_direction(parabola, max_size, EAST)
        cycle += 1

        phash = parabola_hash(parabola)
        if phash in hash_map:
            cycle_diff = cycle - hash_map[phash]
            break

        hash_map[phash] = cycle

    while (cycle + cycle_diff) < 1_000_000_000:
        cycle += cycle_diff


    while cycle < 1_000_000_000:
        roll_direction(parabola, max_size, NORTH)
        roll_direction(parabola, max_size, WEST)
        roll_direction(parabola, max_size, SOUTH)
        roll_direction(parabola, max_size, EAST)
        cycle += 1

    total_b = calc_weight(parabola, max_size)

    return total_a, total_b


def main():
    parabola, max_size = load_parabola(load_data('input_014.txt'))

    results = process(parabola, max_size)

    print(results[0], '==', 106990)
    print(results[1], '==', 100531)


if __name__ == '__main__':
    main()
