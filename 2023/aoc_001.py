"""
--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

Your puzzle answer was 54927.

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

Your puzzle answer was 54581.
"""

from util import *


def first_digit(text):
    for i, c in enumerate(text):
        if c.isdigit():
            return c, i

    return '', 0

def last_digit(text):
    for i, c in enumerate(text[::-1], 1):
        if c.isdigit():
            return c, len(text) - i

    return '', 0


def find_words(text):
    words = {
        'one':   '1',
        'two':   '2',
        'three': '3',
        'four':  '4',
        'five':  '5',
        'six':   '6',
        'seven': '7',
        'eight': '8',
        'nine':  '9',
        }

    first_offset = len(text)
    first_word = ''
    last_offset = 0
    last_word = ''

    for word in words:
        if word in text:
            foffset = text.index(word)
            loffset = text.rindex(word)

            if foffset < first_offset:
                first_offset = foffset
                first_word = word

            if loffset > last_offset:
                last_offset = loffset
                last_word = word

    words[''] = 0

    return (words[first_word], first_offset), (words[last_word], last_offset)


def process(data):
    total_a = 0
    total_b = 0

    for line in data:
        fdigit = first_digit(line)
        ldigit = last_digit(line)

        total_a += int(fdigit[0] + ldigit[0])

        fword, lword = find_words(line)
        # print(f"{line} = {fdigit}, {fword}, {ldigit}, {lword}")

        if fdigit[1] > fword[1]:
            fdigit = fword

        if ldigit[1] < lword[1]:
            ldigit = lword

        total_b += int(fdigit[0] + ldigit[0])

    return total_a, total_b


def main():
    data = list(load_data('input_001.txt'))

    results = process(data)
    print(results[0], '==', 54927)
    print(results[1], '==', 54581)


if __name__ == '__main__':
    main()
