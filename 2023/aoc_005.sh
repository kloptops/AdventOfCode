#!/bin/bash

pypy3 aoc_005.py 0 > output_0.log &
process_0=$!
pypy3 aoc_005.py 1 > output_1.log &
process_1=$!
pypy3 aoc_005.py 2 > output_2.log &
process_2=$!
pypy3 aoc_005.py 3 > output_3.log &
process_3=$!
pypy3 aoc_005.py 4 > output_4.log &
process_4=$!
pypy3 aoc_005.py 5 > output_5.log &
process_5=$!
pypy3 aoc_005.py 6 > output_6.log &
process_6=$!
pypy3 aoc_005.py 7 > output_7.log &
process_7=$!
pypy3 aoc_005.py 8 > output_8.log &
process_8=$!
pypy3 aoc_005.py 9 > output_9.log &
process_9=$!
pypy3 aoc_005.py 10 > output_10.log &
process_10=$!
pypy3 aoc_005.py 11 > output_11.log &
process_11=$!
pypy3 aoc_005.py 12 > output_12.log &
process_12=$!
pypy3 aoc_005.py 13 > output_13.log &
process_13=$!
pypy3 aoc_005.py 14 > output_14.log &
process_14=$!
pypy3 aoc_005.py 15 > output_15.log &
process_15=$!

wait $process_0 $process_1 $process_2 $process_3 \
     $process_4 $process_5 $process_6 $process_7 \
     $process_8 $process_9 $process_10 $process_11 \
     $process_12 $process_13 $process_14 $process_15

cat output_*.log | sort -n
rm -f output_*.log
