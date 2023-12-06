#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


# Input: <doc_id % 3, (word, doc_id, normalization_factor, tf, idf)>
# Output: word, idf, doc_id, tf, normalization_factor
def reduce_one_group(group):
    """Reduce one group."""
    current_line = ""
    # current_id = -1
    current_word = ""
    for line in group:
        value = line.partition("\t")[2]
        word, doc_id, normalization_factor, tf, idf = value.strip().split()
        if word == current_word:
            current_line += f" {doc_id} {tf} {normalization_factor}"
        else:
            if current_word != "":
                print(f"{current_line}")
            current_line = f"{word} {idf} {doc_id} {tf} {normalization_factor}"
            # current_id = doc_id
            current_word = word
    print(f"{current_line}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
