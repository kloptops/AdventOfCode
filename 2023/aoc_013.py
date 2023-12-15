"""
--- Day 13: Point of Incidence ---

With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.

    #...##..#
    #....#..#
    ..##..###
    #####.##.
    #####.##.
    ..##..###
    #....#..#

To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

    123456789
        ><   
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.
        ><   
    123456789

In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

    1 #...##..# 1
    2 #....#..# 2
    3 ..##..### 3
    4v#####.##.v4
    5^#####.##.^5
    6 ..##..### 6
    7 #....#..# 7

This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

"""
from util import *


def load_maps(data):
    current_map = []
    maps = [current_map]

    for line in data:
        line=line.strip()

        if line == '':
            current_map = []
            maps.append(current_map)
            continue

        current_map.append(line)

    return maps


def map_rotate(current_map):
    new_map = []

    for x in range(len(current_map[0])):
        new_map.append(''.join(
            current_map[y][x]
            for y in range(len(current_map))))

    return new_map


def check_symmetry(i, text):
    a, b = text[:i], text[i:]
    # print(a, b)
    min_len = min(len(a), len(b))
    print(f"{a[-min_len:]} == {b[:min_len]}")
    return a[-min_len:] == b[:min_len][::-1]


def symmetry_iter(text):
    for i in range(1, len(text)):
        if check_symmetry(i, text):
            yield i


def find_symmetry(current_map):
    for i in symmetry_iter(current_map[0]):
        for line in current_map:
            if not check_symmetry(i, line):
                break

        else:
            return i


def find_symmetry_smudge(current_map):
    for line in current_map:
        for i in symmetry_iter(line):
            bad_rows = 0
            for line in current_map:
                if not check_symmetry(i, line):
                    if bad_rows == 0:
                        bad_rows += 1

                    if bad_rows == 1:
                        bad_rows += 1
                        break

            if bad_rows == 1:
                return i

    current_map = map_rotate(current_map)

    for line in current_map:
        for i in symmetry_iter(line):
            bad_rows = 0
            for line in current_map:
                if not check_symmetry(i, line):
                    if bad_rows == 0:
                        bad_rows += 1

                    if bad_rows == 1:
                        break

            if bad_rows == 1:
                return i


def process(data):
    total_a = 0
    total_b = 0

    ## Do something here.
    for i, current_map in enumerate(data):
        symmetry = find_symmetry(current_map)

        if symmetry is None:

            symmetry = find_symmetry(map_rotate(current_map))
            symmetry *= 100

        total_a += symmetry

        symmetry2 = find_symmetry_smudge(current_map)
        total_b += symmetry2

    return total_a, total_b


def main():
    data = load_maps(load_data('input_013.txt'))

    results = process(data)

    print(results[0], '==', 33975)
    print(results[1], '==', None)


if __name__ == '__main__':
    main()
