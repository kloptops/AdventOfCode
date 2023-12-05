#!/bin/bash

PYTHON_EXE=pypy3

$PYTHON_EXE aoc_005.py 0 10 > output_0.log &
process_0=$!
$PYTHON_EXE aoc_005.py 1 10 > output_1.log &
process_1=$!
$PYTHON_EXE aoc_005.py 2 10 > output_2.log &
process_2=$!
$PYTHON_EXE aoc_005.py 3 10 > output_3.log &
process_3=$!
$PYTHON_EXE aoc_005.py 4 10 > output_4.log &
process_4=$!
$PYTHON_EXE aoc_005.py 5 10 > output_5.log &
process_5=$!
$PYTHON_EXE aoc_005.py 6 10 > output_6.log &
process_6=$!
$PYTHON_EXE aoc_005.py 7 10 > output_7.log &
process_7=$!
$PYTHON_EXE aoc_005.py 8 10 > output_8.log &
process_8=$!
$PYTHON_EXE aoc_005.py 9 10 > output_9.log &
process_9=$!

wait $process_0 $process_1 $process_2 $process_3 \
     $process_4 $process_5 $process_6 $process_7 \
     $process_8 $process_9

cat output_*.log | sort -n
rm -f output_*.log
