#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Error: day must be passed as a parameter";
    exit 1;
fi;

wget https://adventofcode.com/2021/day/$1/input --header "cookie: session=${2:-$(cat ~/.config/aoc2021/token)}" -O d$1_input.txt
