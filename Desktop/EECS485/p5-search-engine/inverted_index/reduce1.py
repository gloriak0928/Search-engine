#!/usr/bin/env python3
"""Reduce2."""
import sys
import itertools


# Input: {word} {di} 1
# Output: {word} {di} {tfik}
def main():
    """Divide sorted lines into groups that share a key."""
    # with open("total_document_count.txt", 'r', encoding='utf-8') as file:
    #     total_document_count = int(file.read())

    for key, group in itertools.groupby(sys.stdin, keyfunc):
        tf = 0
        for line in group:
            tf += int(line.partition("\t")[2])
        print(f"{key} {tf}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


if __name__ == "__main__":
    main()
