r'''
--- Day 16: The Floor Will Be Lava ---

With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

    .|...\....
    |.-.\.....
    .....|-...
    ........|.
    ..........
    .........\
    ..../.\\..
    .-.-/..|..
    .|....-|.\
    ..//.|....

The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

    >|<<<\....
    |v-.\^....
    .v...|->>>
    .v...v^.|.
    .v...v^...
    .v...v^..\
    .v../2\\..
    <->-/vv|..
    .|<<<2-|.\
    .v//.|.v..

Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

    ######....
    .#...#....
    .#...#####
    .#...##...
    .#...##...
    .#...##...
    .#..####..
    ########..
    .#######..
    .#...#.#..

Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?

--- Part Two ---

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

    .|<2<\....
    |v-v\^....
    .v.v.|->>>
    .v.v.v^.|.
    .v.v.v^...
    .v.v.v^..\
    .v.v/2\\..
    <-2-/vv|..
    .|<<<2-|.\
    .v//.|.v..

Using this configuration, 51 tiles are energized:

    .#####....
    .#.#.#....
    .#.#.#####
    .#.#.##...
    .#.#.##...
    .#.#.##...
    .#.#####..
    ########..
    .#######..
    .#...#.#..

Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?

'''

import collections

from util import *

class LaserMap(SpatialMap):

    def print_map(self):
        print("-" * self.max_x)
        for y in range(self.max_y):
            print(''.join(
                self.get_cell((x, y), '.')
                for x in range(self.max_x)))
        print("-" * self.max_x)
        print()

    def print_visited(self):
        print("-" * self.max_x)
        for y in range(self.max_y):
            print(''.join(
                (x, y) in self.visited_cells and '#' or '.'
                for x in range(self.max_x)))
        print("-" * self.max_x)
        print()


def load_map(in_data):
    laser_map = LaserMap()

    for y, line in enumerate(in_data):
        for x, char in enumerate(line.strip()):
            if char != '.':
                laser_map.set_cell((x, y), char)

    laser_map.print_map()

    return laser_map


def shoot_laser(laser_map, start_coord, start_direction):
    DIR_NAME = {
        NORTH: '^',
        EAST: '>',
        SOUTH: 'v',
        WEST: '<',
        }

    DIRECTION_MAP = {
        (EAST, '/'): (NORTH, ),
        (EAST, '\\'): (SOUTH, ),
        (EAST, '|'): (NORTH, SOUTH),
        (EAST, '-'): (EAST, ),

        (WEST, '/'): (SOUTH, ),
        (WEST, '\\'): (NORTH, ),
        (WEST, '|'): (NORTH, SOUTH),
        (WEST, '-'): (WEST, ),

        (NORTH, '/'): (EAST, ),
        (NORTH, '\\'): (WEST, ),
        (NORTH, '-'): (EAST, WEST),
        (NORTH, '|'): (NORTH, ),

        (SOUTH, '/'): (WEST, ),
        (SOUTH, '\\'): (EAST, ),
        (SOUTH, '-'): (EAST, WEST),
        (SOUTH, '|'): (SOUTH, ),
        }

    stack = collections.deque(
        ((start_coord, start_direction),))

    done_dir = set()

    while len(stack) > 0:
        coord, direction = stack.popleft()
        # print(len(stack), len(laser_map.visited_cells), coord, DIR_NAME[direction])
        laser_map.visit_cell(coord)

        char = laser_map.get_cell(coord, '.')
        if char != '.':
            a_dirs = DIRECTION_MAP[(direction, char)]
            for a_dir in a_dirs:
                a_coord = adj_coord(coord, a_dir)

                if (a_coord, a_dir) in done_dir:
                    continue

                done_dir.add((a_coord, a_dir))

                if laser_map.valid_coord(a_coord):
                    stack.append((a_coord, a_dir))

            continue

        for new_coord in laser_map.iter_direction(coord, direction):
            char = laser_map.get_cell(new_coord, '.')
            laser_map.visit_cell(new_coord)
            if char == '.':
                continue

            a_dirs = DIRECTION_MAP[(direction, char)]
            for a_dir in a_dirs:
                a_coord = adj_coord(new_coord, a_dir)

                if (a_coord, a_dir) in done_dir:
                    continue

                done_dir.add((a_coord, a_dir))

                if laser_map.valid_coord(a_coord):
                    stack.append((a_coord, a_dir))

            break

    # laser_map.print_visited()

    return len(laser_map.visited_cells)


def process(laser_map):
    total_a = 0
    total_b = 0

    ## Do something here.
    total_a = shoot_laser(laser_map, (0, 0), EAST)

    for x in range(laser_map.max_x):
        laser_map.clear_visited()
        temp_score = shoot_laser(laser_map, (x, 0), SOUTH)
        if temp_score > total_b:
            total_b = temp_score

        laser_map.clear_visited()
        temp_score = shoot_laser(laser_map, (x, laser_map.max_y-1), NORTH)
        if temp_score > total_b:
            total_b = temp_score

    for y in range(laser_map.max_y):
        laser_map.clear_visited()
        temp_score = shoot_laser(laser_map, (0, y), EAST)
        if temp_score > total_b:
            total_b = temp_score

        laser_map.clear_visited()
        temp_score = shoot_laser(laser_map, (laser_map.max_y-1, y), WEST)
        if temp_score > total_b:
            total_b = temp_score

    return total_a, total_b


def main():
    laser_map = load_map(load_data('input_016.txt'))

    results = process(laser_map)

    print(results[0], '==', 6816)
    print(results[1], '==', 8163)


if __name__ == '__main__':
    main()
