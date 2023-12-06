#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


# Input: (f"{doc_id}\t{word} {tf} {idf} {w}")
# Output: (f"{word} {doc_id} \t {normalization_factor} {tf} {idf}")
def reduce_one_group(key, group):
    """Reduce one group."""
    normalization_factor = 0
    group1, group2 = itertools.tee(group, 2)
    for line in group2:
        # print("line is : ", line)
        value = line.partition("\t")[2]
        word, tf, idf, w = value.strip().split()
        normalization_factor += float(w)
        # print("key: ", key, " |||   w: ", w)
    # print("normalization: ", normalization_factor)
    for line in group1:
        value = line.partition("\t")[2]
        word, tf, idf, w = value.strip().split()
        print(f"{word} {key}\t{str(normalization_factor)} {tf} {idf}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
