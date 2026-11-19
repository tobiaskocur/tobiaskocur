#!/usr/bin/env python3
"""Rewrite the block between <!-- recent:start --> and <!-- recent:end --> in README.md
with the latest posts from the public Noily RSS feed. Stdlib only."""
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://noily.eu/rss/"
README = "README.md"
LIMIT = 5
LINK = re.compile(r"https://noily\.eu/[\w./%~-]*")
START, END = "<!-- recent:start -->", "<!-- recent:end -->"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "tobiaskocur-profile-readme"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(2_000_000)


def md_text(s):
    # Feed text is untrusted: collapse whitespace and escape markdown/HTML syntax.
    s = " ".join(s.split())
    return re.sub(r"([\\`*_{}\[\]<>()#+!|~&])", r"\\\1", s)


def posts(xml):
    items = []
    for it in ET.fromstring(xml).iterfind("./channel/item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        if title and "@" not in title and LINK.fullmatch(link):
            items.append((title, link))
        if len(items) == LIMIT:
            break
    return items


def main():
    items = posts(fetch(FEED))
    if not items:
        sys.exit("feed has no usable items; README left unchanged")
    block = "\n".join(f"- [{md_text(t)}]({l})" for t, l in items)
    text = open(README, encoding="utf-8").read()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        sys.exit("markers not found in README.md")
    new = pattern.sub(lambda _: f"{START}\n{block}\n{END}", text, count=1)
    if new != text:
        open(README, "w", encoding="utf-8").write(new)


main()
