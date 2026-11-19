#!/usr/bin/env python3
"""Fill the auto-generated blocks in README.md from public sources. Stdlib only.

Each block sits between <!-- NAME starts --> and <!-- NAME ends -->. A block that
fails to load is left unchanged and the script exits non-zero after the others
are written.
"""
import email.utils
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

README = "README.md"
LIMIT = 5
USER = "tobiaskocur"
PROFILE_REPO = USER  # the profile repo itself is not "work"
MAX_BYTES = 2_000_000


def fetch(url, token=None):
    headers = {"User-Agent": "tobiaskocur-profile-readme"}
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(MAX_BYTES)


def md_text(s):
    # Source text is untrusted: collapse whitespace and escape markdown/HTML syntax.
    s = " ".join(s.split())
    return re.sub(r"([\\`*_{}\[\]<>()#+!|~&])", r"\\\1", s)


def feed(url, link_re):
    """Latest items of an RSS feed as (title, link, YYYY-MM-DD)."""
    link_re = re.compile(link_re)
    out = []
    for it in ET.fromstring(fetch(url)).iterfind("./channel/item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        when = email.utils.parsedate_to_datetime(it.findtext("pubDate") or "")
        if title and "@" not in title and link_re.fullmatch(link):
            out.append((title, link, when.strftime("%Y-%m-%d")))
        if len(out) == LIMIT:
            break
    return out


def repos():
    """Most recently pushed public, non-fork repos of USER as (name, url, date)."""
    url = f"https://api.github.com/users/{USER}/repos?type=owner&sort=pushed&per_page=30"
    out = []
    for r in json.loads(fetch(url, os.environ.get("GITHUB_TOKEN"))):
        name = r["name"]
        if r["private"] or r["fork"] or name == PROFILE_REPO or not re.fullmatch(r"[\w.-]+", name):
            continue
        out.append((name, f"https://github.com/{USER}/{name}", r["pushed_at"][:10]))
        if len(out) == LIMIT:
            break
    return out


SOURCES = {
    "recent_work": repos,
    "noily": lambda: feed("https://noily.eu/rss/", r"https://noily\.eu/[\w./%~-]*"),
    "blog": lambda: feed("https://tobiaskocur.com/feed.xml", r"https://tobiaskocur\.com/[\w./%~-]*"),
}


def render(items):
    return "\n\n".join(f"[{md_text(t)}]({l}) - {d}" for t, l, d in items)


def main():
    text = open(README, encoding="utf-8").read()
    failed = []
    for name, load in SOURCES.items():
        pattern = re.compile(rf"(<!-- {name} starts -->).*?(<!-- {name} ends -->)", re.S)
        if not pattern.search(text):
            failed.append(f"{name}: markers not found")
            continue
        try:
            items = load()
            if not items:
                raise ValueError("no usable items")
        except Exception as e:  # leave the block as is, report at the end
            failed.append(f"{name}: {e}")
            continue
        text = pattern.sub(lambda m: f"{m[1]}\n{render(items)}\n{m[2]}", text, count=1)
    if text != open(README, encoding="utf-8").read():
        open(README, "w", encoding="utf-8").write(text)
    if failed:
        sys.exit("; ".join(failed))


main()
