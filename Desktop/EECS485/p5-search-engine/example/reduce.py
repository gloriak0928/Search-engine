#!/usr/bin/env python3
"""Word count reducer."""
import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(key, group):
    """Reduce one group."""
    print(key, group, "!!!")
    word_count = 0
    for line in group:
        print("line: ", line)
        count = line.partition("\t")[2]
        p1=line.partition("\t")[0]
        p2=line.partition("\t")[1]
        print("p1: ", p1)
        print("p2: ", p2)
        print("count: ", count)
        word_count += int(count)
    print(f"{key} {word_count}")


if __name__ == "__main__":
    main()
