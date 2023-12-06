#!/usr/bin/env python3
"""Map 4."""
import sys


# Input: (f"{word} {doc_id} \t {normalization_factor} {tf} {idf}")
# Output: {int(doc_id)%3} \t {word} {doc_id} {normalization_factor} {tf} {idf}
for line in sys.stdin:
    # """input: <(word, doc_id)"""
    key, _, value = line.partition("\t")
    word, doc_id = key.strip().split()
    normalization_factor, tf, idf = value.strip().split()
    print(
        f"{int(doc_id) % 3}\t{word} {doc_id} {normalization_factor} {tf} {idf}"
        )
