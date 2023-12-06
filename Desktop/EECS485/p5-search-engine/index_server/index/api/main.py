"""REST API for index page."""
import re
import os
# import glob
import math
# import functools

import flask
# import logging

# import index_server
import index


# Every REST API route should return 403
# if a user is not authenticated.
# The only exception is /api/v1/, which is publicly available.
@index.app.route("/api/v1/")
def get_index_api():
    """Return API resource URLs."""
    context = {"hits": "/api/v1/hits/", "url": "/api/v1/"}
    return flask.jsonify(**context)


@index.app.route("/api/v1/hits/")
def get_index_hits_api():
    """Return API resource URLs."""
    stopwords = index.app.config["STOPWORDS"]
    inverted_index = index.app.config["INVERTED_INDEX"]
    q = flask.request.args.get("q", type=str)
    q = re.sub(r"[^a-zA-Z0-9 ]+", "", q)
    q = q.casefold()
    q = q.split()
    w = flask.request.args.get("w", default=0.5, type=float)
    print("in index_server")
    # 1. Find intersection
    # segments_with_word is a list of sets.
    segments_with_word = []
    context = {"hits": []}
    filtered_q = []
    for word in q:
        # Check if q contains stopwords
        if word not in stopwords:
            if word in inverted_index.keys():
                filtered_q.append(word)
                # Each set contains the doc_id for one word
                segments_with_word.append(set(inverted_index[word][1].keys()))
            else:
                return flask.jsonify(**context)

    # intersection is a list of doc_id that interact
    # between all sets in segments_with_word
    intersection_set = segments_with_word[0]
    for i in range(1, len(segments_with_word)):
        intersection_set = intersection_set.intersection(segments_with_word[i])
    intersection_set = list(intersection_set)

    # 2. Compute every hits
    stopwords = index.app.config["PAGE_RANK_DICT"]
    for doc_id in intersection_set:
        # inverted_index_segments = {}
        tf = []
        idf = []
        for word in filtered_q:
            # inverted_index_segments[word] = (
            #     inverted_index[word][0],
            #     inverted_index[word][1][doc_id],
            # )
            tf.append(inverted_index[word][1][doc_id][0])
            idf.append(inverted_index[word][0])
            normalization = inverted_index[word][1][doc_id][1]
        pagerank_d = stopwords[doc_id]

        context["hits"].append(
            {
                "docid": doc_id,
                "score": compute_score(w, pagerank_d, tf, idf, normalization),
            }
        )
    context["hits"] = sorted(
        context["hits"], key=lambda x: x["score"], reverse=True
    )
    print(context)
    return flask.jsonify(**context)


def compute_score(w, pagerank_d, tf, idf, document_normalization):
    """Return tf-idf score."""
    document_vector = [v1 * v2 for v1, v2 in zip(tf, idf)]
    up = sum(v1 * v2 for v1, v2 in zip(idf, document_vector))
    tfidf = up / (
        math.sqrt(sum(x**2 for x in idf)) * math.sqrt(document_normalization)
    )

    score = w * pagerank_d + (1 - w) * tfidf
    return score


def load_index():
    """Load index."""
    # 1, Read the index_path file and load it as a dictionary
    base_path = "index_server/index/inverted_index/"
    index_path = os.path.join(base_path, index.app.config["INDEX_PATH"])
    with open(index_path, 'r', encoding='utf-8') as file:
        for line in file:
            split_line = line.split()
            term = split_line[0]
            idf = float(split_line[1])
            index.app.config["INVERTED_INDEX"][term] = (idf, {})
            for i in range(2, len(split_line), 3):
                # app.config["INVERTED_INDEX"][term][1] is {doc_id: (tf, di)}
                index.app.config["INVERTED_INDEX"][term][1][
                    int(split_line[i])] = (
                    int(split_line[i + 1]),
                    float(split_line[i + 2]),
                )

    # 2, Read the stopwords file and load it as a set
    with open("index_server/index/stopwords.txt", "r", encoding='utf-8') as f:
        for line in f:
            index.app.config["STOPWORDS"].add(line.split()[0])

    # 3, Read the pagerank file and load it as a dictionary
    with open(
        "index_server/index/pagerank.out", 'r', encoding='utf-8'
    ) as file:  # from index_server/index/
        for line in file:
            split_line = line.split(",")
            doc_id = int(split_line[0])
            pagerank = float(split_line[1])
            index.app.config["PAGE_RANK_DICT"][doc_id] = pagerank
