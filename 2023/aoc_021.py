"""
--- Day 21: Step Counter ---

You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid trip to Desert Island! It even helpfully drops you off near the gardener and his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.), and rocks (#). For example:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#...#..
    ....#.#....
    .##..S####.
    .##..#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........

The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take one step north, south, east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked O:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#...#..
    ....#O#....
    .##.OS####.
    .##..#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........

Then, he takes a second step. Since at this point he could be at either tile marked O, his second step would allow him to reach any garden plot that is one step north, south, east, or west of any tile that he could have reached after the first step:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#O..#..
    ....#.#....
    .##O.O####.
    .##.O#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........

After two steps, he could be at any of the tiles marked O above, including the starting position (either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#.O.#..
    ...O#O#....
    .##.OS####.
    .##O.#...#.
    ....O..##..
    .##.#.####.
    .##..##.##.
    ...........

He will continue like this until his steps for the day have been exhausted. After a total of 6 steps, he could reach any of the garden plots marked O:

    ...........
    .....###.#.
    .###.##.O#.
    .O#O#O.O#..
    O.O.#.#.O..
    .##O.O####.
    .##.O#O..#.
    .O.O.O.##..
    .##.#.####.
    .##O.##.##.
    ...........

In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to reach any of 16 garden plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?
"""
import collections

from util import *


class GardenMap(SpatialMap):
    def __init__(self):
        super().__init__()
        self.start_coord = None

    def print_map(self, visited_gardens=None):
        if visited_gardens is None:
            visited_gardens = []

        visit_map = {
            coord: 'O'
            for coord in visited_gardens}

        print("-" * self.max_x)
        for y in range(self.max_y):
            print(''.join(
                self.get_cell((x, y), visit_map.get((x, y), '.'))
                for x in range(self.max_x)))
        print("-" * self.max_x)
        print()


def load_map(in_data):
    garden_map = GardenMap()

    for y, line in enumerate(in_data):
        for x, char in enumerate(line.strip()):
            if char == '.':
                continue

            if char == '#':
                garden_map.set_cell((x, y), char)

            if char == 'S':
                garden_map.start_coord = (x, y)

    garden_map.print_map()

    return garden_map


def visit_gardens(garden_map, max_steps):

    stack = collections.deque([garden_map.start_coord])
    for step in range(max_steps):
        new_stack = collections.deque([])

        visited_steps = set()

        while len(stack) > 0:
            current_coord = stack.popleft()
            for new_coord in garden_map.iter_adjacent(current_coord):
                char = garden_map.get_cell(new_coord, None)

                # print(new_coord, char)

                if new_coord in visited_steps:
                    continue

                if char == '#':
                    continue

                visited_steps.add(new_coord)
                new_stack.append(new_coord)

        stack = new_stack

    garden_map.print_map(visited_steps)

    return len(visited_steps)


def process(garden_map):
    total_a = 0
    total_b = 0

    ## Do something here.
    total_a = visit_gardens(garden_map, 64)

    return total_a, total_b


def main():
    garden_map = load_map(load_data('input_021.txt'))

    results = process(garden_map)

    print(results[0], '==', None)
    print(results[1], '==', None)


if __name__ == '__main__':
    main()
