#!/usr/bin/env python3
"""Word count reducer."""
import sys
import itertools
# import collections
import math


# Input: {word} {di} {idf}
# Output: {word} {doc_id}\t{tfik} {idf}
def main():
    """Divide sorted lines into groups that share a key."""
    with open("total_document_count.txt", "r", encoding='utf-8') as file:
        total_document_count = float(file.read())

    for _, group in itertools.groupby(sys.stdin, keyfunc):
        group_list = list(group)
        idf = float(len(group_list))
        idf = math.log10(total_document_count) - math.log10(idf)
        for line in group_list:
            word = line.split()[0]
            di = line.split()[1]
            tf = line.split()[2]
            print(f"{word} {di}\t{tf} {idf}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


if __name__ == "__main__":
    main()
