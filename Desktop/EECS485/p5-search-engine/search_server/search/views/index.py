"""
Search Engine index (main) view.

URLs include:
/
"""
import threading
import urllib.parse
import heapq
import flask
import requests
import search

import search.config
import search.model

# from search.config import SEARCH_INDEX_SEGMENT_API_URLS
# from search.config import APPLICATION_ROOT


def connect_to(url, results):
    """Connect to url and add result."""
    print("connection")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("current result is: ", results)
            results.append(response.json()["hits"])
        else:
            print("response status code is ", response.status_code)
    except requests.RequestException as e:
        print(f"Error while requesting {url}: {e}")


def construct_url(base_url, q, w):
    """Add q and w to base_url."""
    param = {}
    if q is not None:
        param["q"] = q
    if w is not None:
        param["w"] = w
    return f"{base_url}?{urllib.parse.urlencode(param)}" if param else base_url


@search.app.route("/")
def show_index():
    """Show Index."""
    # 1. http request for API json(multi threads)
    threads = []
    results = []
    w = flask.request.args.get("w")
    # print("w is", w)
    q = flask.request.args.get("q")
    # print("q is", q)
    context = {"pages": [], "have_result": True}
    # Start threads
    if not q:
        return flask.render_template("index.html", **context)

    for base_url in search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]:
        url = construct_url(base_url, q, w)
        # print("url is :", url)
        threads.append(threading.Thread(
            target=connect_to,
            args=(url, results)))
        # print("this request done")

    for thread in threads:
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

    # 2. merge the jsons you get from multi server into one(heapq.merge())
    merged_results = list(
        heapq.merge(*results, key=lambda x: x["score"], reverse=True)
    )[:10]
    print("merged_results is :", merged_results)

    # format of merged_results should be: [
    #     {
    #         "docid": 428,
    #         "score": 0.3841096158618974
    #     },
    #     {
    #         "docid": 1574,
    #         "score": 0.0917098632526262
    #     },
    #     ...
    # ]

    # 3. connect to database, get the page info by doc_id
    connection = search.model.get_db()
    for result in merged_results:
        data = connection.execute(
            """
            SELECT * from documents
            WHERE docid = ?;
            """,
            (result["docid"],),
        ).fetchall()[0]
        if data["summary"] == "":
            data["summary"] = "No summary available"
        context["pages"].append(data)

    return flask.render_template("index.html", **context)


# context = {"pages": [ {
#     docid:0,
#     title:a,
#     summary:a,
#     url:a,

#     }
# ]}
