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
"""
Attempt 1 & 2 revolved around creating codes and matching them against the pattern.

Attempt 1 was way too optimistic

Attempt 2 took a bit of fiddling, but was too slow on patterns with billions of combinations, and required lots of ram.

Both of these attempts used queues and not recursion, they got out of hand.

Attemp 3 i took a different approach, this time i focused on the pattern.
This time is usees recursion to try both . & # for any occurrence of ?, we cache the results by "hashing" the pattern.

The hash is just a simplified version of the pattern. "#......#" should be the same as "#....#" as long as the pattern is complete.

Currently it takes a few minutes on my MBP with python3.11, and 20 or so seconds with pypy3.10. GOOD ENOUGH.
"""


import collections
import functools
import json

from util import *


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

############################################################
## Attempt 1, too slow
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


def make_codes(pattern, broken):
    ## This is too slow. :/

    max_len = len(pattern)
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

############################################################
## Attempt 2, too slow
def make_codes2(pattern, broken):
    ## This is still too slow. :(

    max_len = len(pattern)
    items = list(map(lambda x: '#' * x, broken))
    extra_spaces = max_len - sum(broken) - len(broken) + 1
    size = (len(broken) + 1)

    stack = collections.deque((
        (i, (extra_spaces - i), 0, '.' * (extra_spaces - i))
        for i in range(extra_spaces + 1)))

    counter = 0
    while len(stack) > 0:
        i, val, itx, new_code = stack.popleft()
        counter += 1

        if not match_pattern(new_code, pattern):
            continue

        if (counter % 100_000) == 0:
            print(f"{counter:,d}, {len(stack):,d}, {extra_spaces}, {i}, {val}, {itx} / {len(items)}, {new_code}, {pattern}, {broken}")

        if i == 0:
            while itx < size-1:
                if itx > 0:
                    new_code += '.'

                new_code += items[itx]
                itx += 1

            if not match_pattern(new_code, pattern):
                continue

            yield (0, new_code)
            continue

        if itx == size-1:
            continue

        if itx > 0:
            new_code += '.'

        new_code += items[itx]

        for j in range(i + 1):
            if (itx + 1) == (size - 1) and j != 0:
                continue

            temp = new_code + ('.' * (extra_spaces - j - val))

            if not match_pattern(temp, pattern):
                continue

            # print((j, val + j, itx))
            stack.append((j, extra_spaces - j, itx + 1, temp))

## Used in both attempt 1 and 2
def arrangementor(pattern, broken):
    total = 0

    try:
        for ct, code in make_codes2(pattern, broken):
            # print(ct, code, pattern, broken)
            if not match_pattern(code, pattern):
                continue

            # print(broken, code, pattern)

            total += 1

    except:
        return 0

    return total


############################################################
## Attempt 3, not super fast, but seems to work
@functools.lru_cache
def count_broken(pattern):
    output = []
    count = 0

    for c in pattern:
        if c == '.' and count > 0:
            output.append(count)
            count = 0
            continue

        if c == '#':
            count += 1

    if count > 0:
        output.append(count)

    return output


def hash_pattern(pattern):
    new_pattern = ''

    for c in pattern:
        if c == '.':
            if not new_pattern.endswith('.'):
                new_pattern += c

        else:
            new_pattern += c

    return new_pattern


arrangementor2_cache = {}
def arrangementor2(pattern, broken):
    h_pattern = hash_pattern(pattern)
    if h_pattern in arrangementor2_cache:
        return arrangementor2_cache[h_pattern]

    if '?' not in pattern:
        # pattern is complete, lets see if it matches
        if count_broken(h_pattern) == broken:
            arrangementor2_cache[h_pattern] = 1
            return 1

        else:
            arrangementor2_cache[h_pattern] = 0
            return 0

    # Split our pattern at the first ?
    l_pattern, r_pattern = pattern.split('?', 1)

    # Optimisation, count the broken springs and compare to the broken record.
    l_broken = count_broken(l_pattern)
    # If the left hand side of our pattern doesnt match the expected broken record, we can skip trying any further
    # We dont count the last broken count as it might be in progress.
    if len(l_broken) > 1 and l_broken[:-1] != broken[:(len(l_broken)-1)]:
        # Skip this line of thinking
        arrangementor2_cache[h_pattern] = 0
        return 0

    # Now calculate it as if the ? was a .
    result = arrangementor2(l_pattern + '.' + r_pattern, broken)

    # Then calculate if the ? was a #
    result += arrangementor2(l_pattern + '#' + r_pattern, broken)

    # Cache it
    arrangementor2_cache[h_pattern] = result
    return result


def process(data1, data2):
    total_a = 0
    total_b = 0

    for i, (code, broken) in enumerate(data1):
        arrangementor2_cache.clear()
        arrangements = arrangementor2(code, broken)
        print(i, code, broken, arrangements)
        total_a += arrangements

    for i, (code, broken) in enumerate(data2):
        arrangementor2_cache.clear()
        arrangements = arrangementor2(code, broken)
        print(i, code, broken, arrangements)
        total_b += arrangements

    return total_a, total_b


def main():
    data1, data2 = load_records(load_data('input_012.txt'))

    results = process(data1, data2)

    print(results[0], '==', 7_670)
    print(results[1], '==', 157_383_940_585_037)


if __name__ == '__main__':
    main()
