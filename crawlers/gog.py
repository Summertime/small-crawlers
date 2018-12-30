#!/usr/bin/env python3

import json
from itertools import count, takewhile
from typing import Generator

import requests


url = "https://www.gog.com/games/ajax/filtered"


def gog_crawler(media_type: str) -> Generator[dict, None, None]:
    with requests.Session() as session:
        total_pages = 100
        for page in takewhile(lambda p: p <= total_pages, count(1)):
            data = session.get(url=url, params={"page": page}).json()
            yield from data["products"]
            total_pages = data["totalPages"]


if __name__ == "__main__":
    for media_type in ["game", "movie"]:
        for item in gog_crawler(media_type):
            with open(f"gog.{item['id']}.json", "w", encoding="utf8") as f:
                json.dump(item, f, sort_keys=True, separators=(",", ":"))
