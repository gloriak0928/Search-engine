#!/usr/bin/env python3
"""Map 3."""
import sys


# Input: (f"{word} {doc_id}\t{tf} {idf}")
# Output: (f"{word} {doc_id}\t{tf} {idf} {w}")
for line in sys.stdin:
    key, _, value = line.partition("\t")
    word, doc_id = key.strip().split()
    tf, idf = value.strip().split()
    w = (float(tf) * float(idf)) ** 2
    print(f"{doc_id}\t{word} {tf} {idf} {w}")
