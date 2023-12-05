"""
--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

"""
import sys

from util import *


class RangeMap():
    def __init__(self, from_name, to_name):
        self.from_name = from_name
        self.to_name = to_name
        self.ranges = []

    def dump_map(self):
        print(f"{self.from_name} to {self.to_name}:")
        for i, range_map in enumerate(self.ranges):
            print(f"  - {i}: {range_map[0]} .. {range_map[0] + range_map[2] - 1} -> {range_map[1]} .. {range_map[1] + range_map[2] - 1}")

    def add_range(self, to_start, from_start, size):
        for i, range_map in enumerate(self.ranges):
            if from_start < range_map[0]:
                self.ranges.insert(i, [from_start, to_start, size])
                break
        else:
            self.ranges.append([from_start, to_start, size])

    def do_map(self, in_value):
        for range_map in self.ranges:
            if in_value < range_map[0]:
                return in_value

            if in_value < (range_map[0] + range_map[2]):
                return (in_value - range_map[0] + range_map[1])

        return in_value


def load_maps(in_data):
    maps = {}
    seeds = []

    current_map = None

    for line in in_data:
        line = line.strip()
        if line == '':
            current_map = None
            continue

        if line.startswith('seeds:'):
            seeds = list(map(int, line.split(': ', 1)[-1].split(' ')))

        elif line.endswith(' map:'):
           from_name, to_name = line.split(' ', 1)[0].split('-to-', 1)
           current_map = RangeMap(from_name, to_name)
           maps[from_name] = current_map

        elif line[0].isdigit():
            current_map.add_range(*list(map(int, line.split(' ', 2))))

    return maps, seeds


def do_mapping(maps, from_map, to_map, in_seed):
    current_map = from_map
    current_seed = in_seed

    while current_map != to_map:
        # print(f"{current_map} {current_seed},", end=" ")
        current_seed = maps[current_map].do_map(current_seed)
        current_map = maps[current_map].to_name

    # print(f"{current_map} {current_seed}")
    return current_seed


def get_jobs(seeds, job_id, total_jobs):
    total_seeds = 0
    for seed, amount in zip(seeds[::2], seeds[1::2]):
        yield from range(seed + job_id, seed + amount, total_jobs)


def process(maps, seeds, job_id, total_jobs):
    total_a = 0
    total_b = 0

    if job_id is None:
        total_a = 1 << 64
        for i, seed in enumerate(seeds):
            location = do_mapping(maps, 'seed', 'location', seed)
            if location < total_a:
                total_a = location

    else:
        total_b = 1 << 64

        for seed in get_jobs(seeds, job_id, total_jobs):
            location = do_mapping(maps, 'seed', 'location', seed)
            if location < total_b:
                total_b = location

    return total_a, total_b


def main(argv):
    maps, seeds = load_maps(load_data('input_005.txt'))

    if len(argv) > 2:
        job_id = int(argv[1])
        total_jobs = int(argv[2])

    else:
        job_id = None
        total_jobs = None

    results = process(maps, seeds, job_id, total_jobs)

    if job_id is None:
        print(results[0], '==', 177942185)

    else:
        print(results[1], '==', 69841803)


if __name__ == '__main__':
    main(sys.argv)
