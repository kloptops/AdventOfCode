"""
--- Day 17: Clumsy Crucible ---

The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.

For example:

    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533

Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

    2>>34^>>>1323
    32v>>>35v5623
    32552456v>>54
    3446585845v52
    4546657867v>6
    14385987984v4
    44578769877v6
    36378779796v>
    465496798688v
    456467998645v
    12246868655<v
    25465488877v5
    43226746555v>

This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, what is the least heat loss it can incur?

--- Part Two ---

The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory. Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end). However, it will eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

    2>>>>>>>>1323
    32154535v5623
    32552456v4254
    34465858v5452
    45466578v>>>>
    143859879845v
    445787698776v
    363787797965v
    465496798688v
    456467998645v
    122468686556v
    254654888773v
    432267465553v

In the above example, an ultra crucible would incur the minimum possible heat loss of 94.

Here's another example:

    111111111111
    999999999991
    999999999991
    999999999991
    999999999991

Sadly, an ultra crucible would need to take an unfortunate path like this one:

    1>>>>>>>1111
    9999999v9991
    9999999v9991
    9999999v9991
    9999999v>>>>

This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, what is the least heat loss it can incur?

"""
import heapq

from util import *

DIR_REP = {
    NORTH: '^',
    EAST:  '>',
    SOUTH: 'v',
    WEST:  '<',
    }

POSSIBLE_DIRECTIONS = {
    NORTH: ( EAST,  WEST),
    EAST:  (NORTH, SOUTH),
    SOUTH: ( EAST,  WEST),
    WEST:  (NORTH, SOUTH),
    }


class HeatMap(SpatialMap):
    def __init__(self):
        super().__init__()
        self.heat_level = {}

    def print_map(self):
        print("-" * self.max_x)
        for y in range(self.max_y):
            print(''.join(
                str(self.get_cell((x, y)))
                for x in range(self.max_x)))
        print("-" * self.max_x)
        print()

    def print_heat(self):
        print("-" * self.max_x)
        for y in range(self.max_y):
            print(','.join(
                f"{self.heat_level[(x, y)]:3d}"
                for x in range(self.max_x)))
        print("-" * self.max_x)
        print()


def load_map(in_data):
    heat_map = HeatMap()

    for y, line in enumerate(in_data):
        for x, char in enumerate(line.strip()):
            heat_map.set_cell((x, y), int(char))

    heat_map.print_map()

    return heat_map


def iter_directions(heat_map, coord, direction, steps, min_steps, max_steps, path):
    # Choose either continue direction for a maximum of X steps
    if steps < max_steps:
        next_coord = adj_coord(coord, direction)
        if heat_map.valid_coord(next_coord):
            yield (next_coord, steps + 1, direction)

    # Or turn 90 degrees to our current direction.
    if steps >= min_steps:
        for next_direction in POSSIBLE_DIRECTIONS[direction]:
            next_coord = adj_coord(coord, next_direction)
            if heat_map.valid_coord(next_coord):
                yield (next_coord, 1, next_direction)


def dijkstra(heat_map, start_coord, min_steps, max_steps):
    # A textbook dijkstra algorithm modified
    # It will only allow a maximum of max_steps in any direction and turning 90 degrees to the current direction
    end_coord = (heat_map.max_x-1, heat_map.max_y-1)
    visited = set()

    priority_queue = [
        (0, (0, 0), SOUTH, 1, ''),
        (0, (0, 0),  EAST, 1, ''),
        ]

    heat_map.path_map = {}
    heat_map.heat_level = {
        coord: 1<<64
        for coord in heat_map.cells.keys()
        }

    heat_map.heat_level[start_coord] = 0

    while len(priority_queue) > 0:
        current_heat, current_coord, current_direction, current_steps, current_path = heapq.heappop(priority_queue)

        if (current_coord, current_direction, current_steps) in visited and current_heat >= heat_map.heat_level[current_coord]:
            continue

        visited.add((current_coord, current_direction, current_steps))

        # if current_heat > heat_map.heat_level[current_coord]:
        #     continue

        for (next_coord, next_steps, next_direction) in iter_directions(
                heat_map, current_coord, current_direction, current_steps, min_steps, max_steps, current_path):

            next_heat = current_heat + heat_map.get_cell(next_coord)

            next_path = current_path + DIR_REP[next_direction]

            if next_coord == end_coord and current_steps < min_steps:
                continue

            if next_heat < heat_map.heat_level[next_coord]:
                heat_map.heat_level[next_coord] = next_heat
                heat_map.path_map[next_coord] = next_path

            heapq.heappush(priority_queue, (next_heat, next_coord, next_direction, next_steps, next_path))

    heat_map.print_heat()
    print(heat_map.path_map[end_coord])

    return heat_map.heat_level[end_coord]


def process(heat_map):
    total_a = 0
    total_b = 0

    ## Do something here.
    total_a = dijkstra(heat_map, (0, 0), 0, 3)
    total_b = dijkstra(heat_map, (0, 0), 4, 10)

    return total_a, total_b


def main():
    heat_map = load_map(load_data('input_017.txt'))

    results = process(heat_map)

    print(results[0], '!=', 788, 834)
    print(results[1], '==', None)


if __name__ == '__main__':
    main()
