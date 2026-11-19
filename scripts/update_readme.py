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
TOKEN = os.environ.get("GITHUB_TOKEN")
RELEASE_LINK = re.compile(rf"https://github\.com/{USER}/[\w.-]+/releases/tag/[\w.%~+-]+")


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
        try:
            when = email.utils.parsedate_to_datetime(it.findtext("pubDate") or "")
        except (TypeError, ValueError):
            continue  # one bad item must not drop the whole feed
        if title and "@" not in title and link_re.fullmatch(link):
            out.append((title, link, when.strftime("%Y-%m-%d"), ""))
        if len(out) == LIMIT:
            break
    return out


def public_repos():
    """Public, non-fork repos of USER (excluding the profile repo), most recently pushed first."""
    url = f"https://api.github.com/users/{USER}/repos?type=owner&sort=pushed&per_page=100"
    out = []
    for r in json.loads(fetch(url, TOKEN)):
        if r["private"] or r["fork"] or r["archived"] or r["name"] == PROFILE_REPO or not re.fullmatch(r"[\w.-]+", r["name"]):
            continue
        out.append(r)
    return out


def recent_releases():
    """Latest releases across public repos; with no release at all, the latest pushed repos.

    Returns (title, link, date, note) tuples. Any API error propagates, so a broken
    releases call never silently turns into the fallback list.
    """
    repos = public_repos()
    releases = []
    for r in repos:
        url = f"https://api.github.com/repos/{USER}/{r['name']}/releases?per_page=1"
        for rel in json.loads(fetch(url, TOKEN)):
            if rel.get("draft") or not rel.get("published_at"):
                continue
            link = rel.get("html_url", "")
            if RELEASE_LINK.fullmatch(link):
                label = rel.get("name") or rel["tag_name"]
                releases.append((f"{r['name']} {label}", link, rel["published_at"][:10], ""))
    if releases:
        return sorted(releases, key=lambda x: x[2], reverse=True)[:LIMIT]
    return [(r["name"], r["html_url"], r["pushed_at"][:10], r.get("description") or "") for r in repos[:LIMIT]]


SOURCES = {
    "recent_releases": recent_releases,
    "noily": lambda: feed("https://noily.eu/rss/", r"https://noily\.eu/[\w./%~-]*"),
    "blog": lambda: feed("https://tobiaskocur.com/feed.xml", r"https://tobiaskocur\.com/[\w./%~-]*"),
}


def render(items):
    return "\n\n".join(
        f"[{md_text(t)}]({l}) - {d}" + (f"<br>{md_text(n)}" if n else "") for t, l, d, n in items
    )


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
