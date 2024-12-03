"""
--- Day 2: Red-Nosed Reports ---

Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9

This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

- 7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
- 1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
- 9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
- 1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
- 8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
- 1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

- 7 6 4 2 1: Safe without removing any level.
- 1 2 7 8 9: Unsafe regardless of which level is removed.
- 9 7 6 2 1: Unsafe regardless of which level is removed.
- 1 3 2 4 5: Safe by removing the second level, 3.
- 8 6 4 4 1: Safe by removing the third level, 4.
- 1 3 6 7 9: Safe without removing any level.

Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?

"""

from util import *

def impossible_doubles(items):
    """
    This quick check rules out impossible combos.
    """
    return (len(items) - len(set(items))) > 1

BUFFER=""
def print_buff(text, end="\n"):
    global BUFFER
    BUFFER += text + end

def dump_buff():
    global BUFFER
    print(BUFFER)
    BUFFER=""

def clear_buff():
    global BUFFER
    BUFFER=""

def detect_changes(items, min_diff, max_diff, do_try=False):
    direction = None
    last_item = items[0]

    print_buff(f"- {items=}", end="")
    for i, item in enumerate(items[1:], 1):
        diff = item - last_item

        if abs(diff) <= min_diff:
            # print(f"Min diff: {abs(diff)=} <= {min_diff=}")
            print_buff(f" min diff {abs(diff)}")
            if do_try:
                # Part 2
                if i == 1 and detect_changes(items[1:], min_diff, max_diff):
                    return True

                elif i == len(items)-1 and detect_changes(items[:i], min_diff, max_diff):
                    return True

                elif detect_changes(items[:i-1] + items[i:], min_diff, max_diff):
                    return True

                return detect_changes(items[:i] + items[i+1:], min_diff, max_diff)

            return False

        if abs(diff) >= max_diff:
            # print(f"Max diff: {abs(diff)=} >= {max_diff}")
            print_buff(f" max diff {abs(diff)}")
            if do_try:
                # Part 2
                if i == 1 and detect_changes(items[1:], min_diff, max_diff):
                    return True

                elif i == len(items)-1 and detect_changes(items[:i], min_diff, max_diff):
                    return True

                elif detect_changes(items[:i-1] + items[i:], min_diff, max_diff):
                    return True

                return detect_changes(items[:i] + items[i+1:], min_diff, max_diff)

            return False

        if direction is not None and (
                (direction < 0 and diff > 0) or
                (direction > 0 and diff < 0)):
            # print(f"Different direction {direction=}: {diff}")
            print_buff(f" direction {diff} vs {direction}")
            if do_try:
                # Part 2
                if i == 1 and detect_changes(items[1:], min_diff, max_diff):
                    return True

                elif i == 2 and detect_changes(items[1:], min_diff, max_diff):
                    return True

                elif i == len(items)-1 and detect_changes(items[:i], min_diff, max_diff):
                    return True

                elif detect_changes(items[:i-1] + items[i:], min_diff, max_diff):
                    return True

                return detect_changes(items[:i] + items[i+1:], min_diff, max_diff)

            return False

        direction = diff
        last_item = item

    print_buff("")

    return True


def process(data):
    total_a = 0
    total_b = 0

    ## Do something here.
    for report in data:
        # These are impossible to be true.
        if impossible_doubles(report):
            continue

        print_buff(f"=======")
        if detect_changes(report, 0, 4):
            total_a += 1
            total_b += 1
            print_buff("TRUE")
            clear_buff()
            # dump_buff()
            continue
        elif detect_changes(report, 0, 4, True):
            total_b += 1
            print_buff("TRUE")
            clear_buff()
            # dump_buff()
            continue

        print_buff("FALSE")
        dump_buff()

    return total_a, total_b


def main():
    data = [
        tuple(int(x) for x in line.split(' '))
        for line in load_data('input_002.txt')]

    results = process(data)

    print(results[0], '==', 407)
    print(results[1], '>=', 455)


if __name__ == '__main__':
    main()
