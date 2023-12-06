#!/usr/bin/env python3
"""Map3."""
import sys


# Input: {word} {di} {tfik}
# Output: {word} {di} {tfik}
for line in sys.stdin:
    word = line.split()[0]
    di = line.split()[1]
    tfik = line.split()[2]
    print(f"{word}\t{di} {tfik}")
