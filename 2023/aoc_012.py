"""
--- Day 12: Hot Springs ---

You finally reach the hot springs! You can see steam rising from secluded areas attached to the primary, ornate building.

As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot springs, weren't you?" You indicate that this definitely looks like hot springs to you.

"Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."

You look in the direction the researcher is pointing and suddenly notice the massive metal helixes towering overhead. "This way!"

It only takes you a few more steps to reach the main gate of the massive fenced-off area containing the springs. You go through the gate and into a small administrative building.

"Hello! What brings you to the hot springs today? Sorry they're not very hot right now; we're having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.

"Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, not until we get more lava to heat our forges. And our springs. The springs aren't very springy unless they're hot!"

"Say, could you go up and see why the lava stopped flowing? The springs are too cold for normal operation, but we should be able to find one springy enough to launch you up there!"

There's just one problem - many of the springs have fallen into disrepair, so they're not actually sure which springs would even be safe to use! Worse yet, their condition records of which springs are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged records.

In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

    #.#.### 1,1,3
    .#...#....###. 1,1,3
    .#.###.#.###### 1,3,1,6
    ####.#...#... 4,1,1
    #....######..#####. 1,6,5
    .###.##....# 3,2,1

However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:

    ???.### 1,1,3
    .??..??...?##. 1,1,3
    ?#?#?#?#?#?#?#? 1,3,1,6
    ????.#...#... 4,1,1
    ????.######..#####. 1,6,5
    ?###???????? 3,2,1

Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

    ?###???????? 3,2,1
    .###.##.#...
    .###.##..#..
    .###.##...#.
    .###.##....#
    .###..##.#..
    .###..##..#.
    .###..##...#
    .###...##.#.
    .###...##..#
    .###....##.#

In this example, the number of possible arrangements for each row is:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 4 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 1 arrangement
    ????.######..#####. 1,6,5 - 4 arrangements
    ?###???????? 3,2,1 - 10 arrangements

Adding all of the possible arrangement counts together produces a total of 21 arrangements.

For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?

"""
from util import *
import collections


def load_records(data):
    output1 = []
    output2 = []
    for line in data:
        code, broken = line.strip().split()
        broken = list(map(int, broken.split(',')))
        output1.append((code, broken))

        code2 = '?'.join((code, ) * 5)
        broken2 = broken * 5
        output2.append((code2, broken2))

    return output1, output2


def match_pattern(code, pattern):
    for c, p in zip(code, pattern):
        if c == '#' and p not in '#?':
            return False

        if c == '.' and p not in '.?':
            return False

    return True


def permutations(amount, size):
    stack = collections.deque((
        (i, [amount - i])
        for i in range(amount + 1)))

    while len(stack) > 0:
        i, items = stack.popleft()
        if i == 0:
            while len(items) < size:
                items.append(0)

            yield items
            continue

        if len(items) == size-1:
            items.append(i)
            yield items
            continue

        for j in range(i + 1):
            temp = items[:]
            temp.append(amount - j - sum(temp))
            stack.append((j, temp))


def make_codes(broken, max_len):
    items = list(map(lambda x: '#' * x, broken))
    extra_spaces = max_len - sum(broken) - len(broken) + 1

    for spaces in permutations(extra_spaces, (len(broken) + 1)):
        # print(broken, spaces)
        results = [
            '.' * spaces[0]
            ]

        for i, value in enumerate(items):
            if i > 0:
                results.append('.')
            results.append(value)
            results.append('.' * spaces[i + 1])

        yield ''.join(results)


def arrangementor(pattern, broken):
    total = 0

    for code in make_codes(broken, len(pattern)):
        if not match_pattern(code, pattern):
            continue

        # print(broken, code, pattern)

        total += 1

    return total


def process(data1, data2):
    total_a = 0
    total_b = 0

    for code, broken in data1:
        total_a += arrangementor(code, broken)

    # for code, broken in data2:
    #     total_b += arrangementor(code, broken)
    #     print(total_b)

    return total_a, total_b


def main():
    data1, data2 = load_records(load_data('input_012.txt'))

    results = process(data1, data2)

    print(results[0], '==', 7670)
    print(results[1], '==', None)


if __name__ == '__main__':
    main()
