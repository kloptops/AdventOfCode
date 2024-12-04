"""
--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

    ..X...
    .SAMX.
    .A..A.
    XMAS.S
    .X....

The actual word search will be full of letters instead. For example:

    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

    ....XXMAS.
    .SAMXMS...
    ...S..A...
    ..A.A.MS.X
    XMASAMX.MM
    X.....XA.A
    S.S.S.S.SS
    .A.A.A.A.A
    ..M.M.M.MM
    .X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?

--- Part Two ---

The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

    M.S
    .A.
    M.S

Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

    .M.S......
    ..A..MSMS.
    .M.S.MAA..
    ..A.ASMSM.
    .M.S.M....
    ..........
    S.S.S.S.S.
    .A.A.A.A..
    M.M.M.M.M.
    ..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

"""

from collections import deque

from util import *


def check_word_1(word_map, coord):
    WORD = 'XMAS'
    NEXT_LETTER = {
        'X': 'M',
        'XM': 'A',
        'XMA': 'S',
        }

    total = 0
    coords = deque([])

    state = word_map.get_cell(coord)

    for direction in ALL_DIRECTIONS:
        a_coord = adj_coord(coord, direction)

        a_letter = word_map.get_cell(a_coord)
        if NEXT_LETTER[state] != a_letter:
            continue

        # print(f"  {a_coord}: {word_map.get_cell(a_coord)}")

        new_state = state + a_letter

        coords.append((a_coord, direction, new_state))

    while len(coords) > 0:
        coord, direction, state = coords.popleft()

        a_coord = adj_coord(coord, direction)

        a_letter = word_map.get_cell(a_coord)

        # print(f"    {a_coord}: {a_letter}")

        if NEXT_LETTER[state] != a_letter:
            continue

        new_state = state + a_letter

        if new_state == WORD:
            total += 1
            continue

        coords.append((a_coord, direction, new_state))

    return total


def check_word_2(word_map, coord):
    VALID_WORDS = ('MS', 'SM')

    WORD_1 = (
        word_map.get_cell(adj_coord(coord, NORTH_EAST), '') +
        word_map.get_cell(adj_coord(coord, SOUTH_WEST), ''))
    WORD_2 = (
        word_map.get_cell(adj_coord(coord, NORTH_WEST), '') +
        word_map.get_cell(adj_coord(coord, SOUTH_EAST), ''))

    if WORD_1 in VALID_WORDS and WORD_2 in VALID_WORDS:
        return 1

    return 0



def process(word_map):
    total_a = 0
    total_b = 0

    ## Do something here.
    coords = []
    for coord in word_map.cells:

        if word_map.get_cell(coord) == 'X':
            # print(f"{coord}: {word_map.get_cell(coord)}")
            total_a += check_word_1(word_map, coord)

        if word_map.get_cell(coord) == 'A':
            total_b += check_word_2(word_map, coord)

    return total_a, total_b


def main():
    data = list(load_data('input_004.txt'))

    word_map = SpatialMap()
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            word_map.set_cell((x, y), char)

    results = process(word_map)

    print(results[0], '==', 2593)
    print(results[1], '==', 1950)


if __name__ == '__main__':
    main()
