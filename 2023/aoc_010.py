"""
--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

    .....
    .F-7.
    .|.|.
    .L-J.
    .....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

    .....
    .S-7.
    .|.|.
    .L-J.
    .....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

    -L|F7
    7S-7|
    L|7||
    -L-J|
    L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

    7-F7-
    .FJ|7
    SJLL7
    |F--J
    LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

    .....
    .S-7.
    .|.|.
    .L-J.
    .....

You can count the distance each tile in the loop is from the starting point like this:

    .....
    .012.
    .1.3.
    .234.
    .....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...

Here are the distances for each tile on that loop:

    ..45.
    .236.
    01.78
    14567
    23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

    ...........
    .S-------7.
    .|F-----7|.
    .||.....||.
    .||.....||.
    .|L-7.F-J|.
    .|..|.|..|.
    .L--J.L--J.
    ...........

The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

    ...........
    .S-------7.
    .|F-----7|.
    .||OOOOO||.
    .||OOOOO||.
    .|L-7OF-J|.
    .|II|O|II|.
    .L--JOL--J.
    .....O.....

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

    ..........
    .S------7.
    .|F----7|.
    .||OOOO||.
    .||OOOO||.
    .|L-7F-J|.
    .|II||II|.
    .L--JL--J.
    ..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

    .F----7F7F7F7F-7....
    .|F--7||||||||FJ....
    .||.FJ||||||||L7....
    FJL7L7LJLJ||LJ.L-7..
    L--J.L7...LJS7F-7L7.
    ....F-J..F7FJ|L7L7L7
    ....L7.F7||L7|.L7L7|
    .....|FJLJ|FJ|F7|.LJ
    ....FJL-7.||.||||...
    ....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

    OF----7F7F7F7F-7OOOO
    O|F--7||||||||FJOOOO
    O||OFJ||||||||L7OOOO
    FJL7L7LJLJ||LJIL-7OO
    L--JOL7IIILJS7F-7L7O
    OOOOF-JIIF7FJ|L7L7L7
    OOOOL7IF7||L7|IL7L7|
    OOOOO|FJLJ|FJ|F7|OLJ
    OOOOFJL-7O||O||||OOO
    OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

    FF7FSF7F7F7F7F7F---7
    L|LJ||||||||||||F--J
    FL-7LJLJ||||||LJL-77
    F--JF--7||LJLJ7F7FJ-
    L---JF-JLJ.||-FJLJJ7
    |F|F-JF---7F7-L7L|7|
    |FFJF7L7F-JF7|JL---7
    7-L-JL7||F7|L7F-7F7|
    L.L7LFJ|||||FJL7||LJ
    L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

    FF7FSF7F7F7F7F7F---7
    L|LJ||||||||||||F--J
    FL-7LJLJ||||||LJL-77
    F--JF--7||LJLJIF7FJ-
    L---JF-JLJIIIIFJLJJ7
    |F|F-JF---7IIIL7L|7|
    |FFJF7L7F-JF7IIL---7
    7-L-JL7||F7|L7F-7F7|
    L.L7LFJ|||||FJL7||LJ
    L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?


"""
from util import *
import collections

NORTH = ( 0, -1)
EAST  = (+1,  0)
SOUTH = ( 0, +1)
WEST  = (-1,  0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
DIRS = 'NESW'
DIR_REV = {
    'NS': '|',
    'EW': '-',
    'NE': 'L',
    'SW': '7',
    'ES': 'F',
    'NW': 'J',
    }

DIR_MAP = {
    '|': (NORTH, SOUTH),
    '-': (EAST, WEST),
    'F': (EAST, SOUTH),
    '7': (SOUTH, WEST),
    'L': (NORTH, EAST),
    'J': (NORTH, WEST),
    }


def calc_direction(coord, new_direction, max_coord):
    if not (0 <= (coord[0] + new_direction[0]) < max_coord[0]):
        return None

    if not (0 <= (coord[1] + new_direction[1]) < max_coord[1]):
        return None

    return (coord[0] + new_direction[0]), (coord[1] + new_direction[1])


def build_graph(data):
    data = list(map(str.strip, data))

    max_coord = (len(data), len(data[0]))

    graph = {
        'start': None,
        'max': max_coord,
        }

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '.':
                continue

            elif char == 'S':
                graph['start'] = (x, y)
                continue

            coord = (x, y)
            graph[coord] = []
            for direction in DIR_MAP[char]:
                new_coord = calc_direction(coord, direction, max_coord)

                graph[coord].append(new_coord)

            graph[coord].append(char)

    return graph


def check_connection(graph, coord_a, coord_b, forward=False):
    if not forward and coord_a not in graph:
        return False

    if coord_b not in graph:
        return False

    if not forward and coord_b not in graph[coord_a]:
        return False

    if coord_a not in graph[coord_b]:
        return False

    return True


def get_next(graph, prev_coord, curr_coord):
    moves = graph[curr_coord]

    if moves[0] == prev_coord:
        return moves[1]

    return moves[0]


def process(graph):
    total_a = 0
    total_b = 0

    queue = collections.deque()

    all_visited = set()
    all_visited.add(graph['start'])

    # Find start directions
    start_code = ''
    start_dirs = []
    for thread_id, (direction, dir_code) in enumerate(zip(DIRECTIONS, DIRS)):
        curr_coord = graph['start']
        next_coord = calc_direction(curr_coord, direction, graph['max'])
        if next_coord not in graph:
            continue

        if not check_connection(graph, curr_coord, next_coord, forward=True):
            # Dead end, scratch it
            continue

        start_code = start_code + dir_code
        all_visited.add(next_coord)
        start_dirs.append(next_coord)

        queue.append(
            (thread_id, curr_coord, next_coord, 1))

    print(start_code, DIR_REV[start_code])
    start_dirs.append(DIR_REV[start_code])
    graph[graph['start']] = start_dirs

    while len(queue) > 0:
        thread_id, prev_coord, curr_coord, curr_steps = queue.popleft()
        next_coord = get_next(graph, prev_coord, curr_coord)
        print(f"{thread_id}: {curr_coord} -> {next_coord} ({curr_steps})")

        if next_coord is None:
            continue

        all_visited.add(curr_coord)

        if not check_connection(graph, curr_coord, next_coord):
            # Dead end, scratch it
            continue

        if next_coord in all_visited:
            # End?
            if total_a < curr_steps:
                total_a = curr_steps

            continue

        curr_steps += 1

        queue.append((
            thread_id, curr_coord, next_coord, curr_steps))

    """
    Simple line crossing algorithm, if we cross a line it means we toggle being inside/outside
    Since we know which cells are a part of our loop from above we can just iterate over the whole map
    Since we can be "running along" a pipe, we just need to see if its an S bend or a U turn
    S bend will mean we are swapping inside/outside the loop, U turn means we stay in the same state
    """
    for y in range(graph['max'][1]):
        outside = False
        start = None

        for x in range(graph['max'][0]):
            coord = (x, y)
            cell = graph.get(coord, [0, 0, '.'])[2]

            if coord in all_visited:
                # -> F--J S-Bend
                # -> L--7 S-Bend
                # -> L--J U-Turn
                # -> F--7 U-Turn

                if cell in '-':
                    # Follow pipe
                    continue

                if cell in '|':
                    # Swap inside
                    outside = not outside
                    continue

                if cell in 'FL':
                    # Start pipe
                    start = graph[coord][2]
                    continue

                if cell == '7':
                    if start == 'L':
                        # S-bend
                        outside = not outside

                    start = None
                    continue

                if cell == 'J':
                    if start == 'F':
                        # S-bend
                        outside = not outside

                    start = None
                    continue

                continue

            # print(coord, cell, outside)

            if outside:
                total_b += 1

    return total_a, total_b


def main():
    graph = build_graph(load_data('input_010.txt'))

    # print(graph)
    results = process(graph)

    print(results[0], '==', 6823)
    print(results[1], '==', 415)


if __name__ == '__main__':
    main()
