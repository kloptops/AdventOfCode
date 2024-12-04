"""
--- Day 3: Mull It Over ---

"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

- xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

--- Part Two ---

As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?

"""

from util import *


def gobble_number(data, offset):
    """Gobble."""
    if not data[offset[0]].isdigit():
        return None

    number = ""
    while data[offset[0]].isdigit():
        number += data[offset[0]]
        offset[0] += 1

    return int(number)


def gobble_text(data, offset, text, skip_anyway=False):
    """Gobble gobble gobble."""
    # print(f"{data[offset[0]:len(text)]} != {text} == {data[offset[0]:len(text)] != text}")
    if data[offset[0]:offset[0]+len(text)] != text:
        if skip_anyway:
            offset[0] += len(text)
        return False

    offset[0] += len(text)
    return True


def process_a(data):
    total = 0
    offset = [0]
    while offset[0] < len(data):
        # print(f"{offset[0]}: {data[offset[0]:offset[0]+10]}")
        offset[0] = data.find('mul', offset[0])
        if offset[0] == -1:
            break

        offset[0] += 3

        if not gobble_text(data, offset, "("):
            continue

        number_a = gobble_number(data, offset)
        if not number_a:
            continue

        if not gobble_text(data, offset, ","):
            continue

        number_b = gobble_number(data, offset)
        if not number_b:
            continue

        if not gobble_text(data, offset, ")"):
            continue

        # print(f"mul({number_a},{number_b})")
        total += number_a * number_b

    return total


def process_b(data):
    total = 0
    offset = [0]
    while offset[0] < len(data):
        new_offset = data.find('don\'t()', offset[0])

        # This is okay.
        print(f"{data[offset[0]:new_offset]}")
        total += process_a(data[offset[0]:new_offset])
        if new_offset == -1:
            break

        # Disabled.
        offset[0] = new_offset + 7

        offset[0] = data.find('do()', offset[0])
        if offset[0] == -1:
            break

    return total


def process(data):
    total_a = 0
    total_b = 0

    total_a = process_a(data)
    total_b = process_b(data)

    return total_a, total_b


def main():
    data = '\n'.join(load_data('input_003.txt'))

    results = process(data)

    print(results[0], '==', 178538786)
    print(results[1], '==', None)


if __name__ == '__main__':
    main()
