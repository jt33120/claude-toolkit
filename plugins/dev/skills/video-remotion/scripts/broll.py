#!/usr/bin/env python3
"""Search and download free stock video (Pexels, Pixabay) and log each clip's credit.

Usage:
    python broll.py search "<query>" [--source pexels|pixabay|both] [--orientation portrait|landscape|square]
                    [--min-duration S] [--limit N]
    python broll.py download <pexels|pixabay> <id> [--out public/broll] [--target-long 1920]

Keys are read from PEXELS_API_KEY and PIXABAY_API_KEY (free); they are never printed.
`download` saves <source>-<id>.mp4 and records source page, author and license in
<out>/credits.json. Standard library only.
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PEXELS = "https://api.pexels.com/v1/videos"
PIXABAY = "https://pixabay.com/api/videos/"
LICENSES = {
    "pexels": "Pexels License (https://www.pexels.com/license/)",
    "pixabay": "Pixabay Content License (https://pixabay.com/service/license-summary/)",
}
KEY_ENV = {"pexels": "PEXELS_API_KEY", "pixabay": "PIXABAY_API_KEY"}
USER_AGENT = "claude-toolkit-broll/1.0"


def fetch(url, headers=None):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    return urllib.request.urlopen(request, timeout=60)


def api_key(source):
    key = os.environ.get(KEY_ENV[source], "")
    if not key:
        sys.exit(f"{KEY_ENV[source]} is not set (free key: create an account on {source}.com).")
    return key


def get_json(source, url):
    headers = {"Authorization": api_key("pexels")} if source == "pexels" else None
    with fetch(url, headers) as response:
        return json.load(response)


def pick_file(files, target_long):
    """Smallest mp4 whose longer side reaches target_long, else the largest available."""
    usable = [f for f in files if f.get("link") and f.get("width") and f.get("height")]
    usable = [f for f in usable if f.get("file_type", "video/mp4") == "video/mp4"]
    if not usable:
        return None
    long_side = lambda f: max(f["width"], f["height"])
    enough = [f for f in usable if long_side(f) >= target_long]
    return min(enough, key=long_side) if enough else max(usable, key=long_side)


def pexels_clip(item, target_long=1920):
    chosen = pick_file(item.get("video_files", []), target_long)
    if not chosen:
        return None
    return {
        "source": "pexels", "id": item["id"], "page_url": item.get("url"),
        "author": item.get("user", {}).get("name"), "author_url": item.get("user", {}).get("url"),
        "duration": item.get("duration"), "width": chosen["width"], "height": chosen["height"],
        "download_url": chosen["link"],
    }


def pixabay_clip(item, target_long=1920):
    files = [{"link": v.get("url"), "width": v.get("width"), "height": v.get("height")}
             for v in item.get("videos", {}).values()]
    chosen = pick_file(files, target_long)
    if not chosen:
        return None
    return {
        "source": "pixabay", "id": item["id"], "page_url": item.get("pageURL"),
        "author": item.get("user"), "author_url": None,
        "duration": item.get("duration"), "width": chosen["width"], "height": chosen["height"],
        "download_url": chosen["link"],
    }


def search(source, query, orientation, limit):
    if source == "pexels":
        params = {"query": query, "per_page": limit}
        if orientation:
            params["orientation"] = orientation
        data = get_json("pexels", f"{PEXELS}/search?{urllib.parse.urlencode(params)}")
        return [c for c in map(pexels_clip, data.get("videos", [])) if c]
    params = {"key": api_key("pixabay"), "q": query[:100], "per_page": max(3, limit), "safesearch": "true"}
    data = get_json("pixabay", f"{PIXABAY}?{urllib.parse.urlencode(params)}")
    clips = [c for c in map(pixabay_clip, data.get("hits", [])) if c]
    if orientation in ("portrait", "landscape"):
        clips = [c for c in clips if (c["height"] > c["width"]) == (orientation == "portrait")]
    return clips[:limit]


def lookup(source, clip_id, target_long):
    if source == "pexels":
        return pexels_clip(get_json("pexels", f"{PEXELS}/videos/{clip_id}"), target_long)
    params = urllib.parse.urlencode({"key": api_key("pixabay"), "id": clip_id})
    hits = get_json("pixabay", f"{PIXABAY}?{params}").get("hits", [])
    return pixabay_clip(hits[0], target_long) if hits else None


def record_credit(out, clip, filename):
    path = out / "credits.json"
    credits = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    credits = [c for c in credits if c.get("file") != filename]
    credits.append({
        "file": filename, "source": clip["source"], "id": clip["id"], "page_url": clip["page_url"],
        "author": clip["author"], "license": LICENSES[clip["source"]],
    })
    path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def download(source, clip_id, out, target_long):
    clip = lookup(source, clip_id, target_long)
    if not clip:
        sys.exit(f"No downloadable mp4 found for {source} {clip_id}.")
    out.mkdir(parents=True, exist_ok=True)
    filename = f"{source}-{clip_id}.mp4"
    with fetch(clip["download_url"]) as response, (out / filename).open("wb") as handle:
        while chunk := response.read(1 << 20):
            handle.write(chunk)
    record_credit(out, clip, filename)
    return {"file": str(out / filename), **{k: clip[k] for k in ("page_url", "author", "width", "height", "duration")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    find = sub.add_parser("search")
    find.add_argument("query")
    find.add_argument("--source", choices=["pexels", "pixabay", "both"], default="both")
    find.add_argument("--orientation", choices=["portrait", "landscape", "square"])
    find.add_argument("--min-duration", type=float, default=0)
    find.add_argument("--limit", type=int, default=8)
    get = sub.add_parser("download")
    get.add_argument("source", choices=["pexels", "pixabay"])
    get.add_argument("id")
    get.add_argument("--out", default="public/broll")
    get.add_argument("--target-long", type=int, default=1920)
    args = parser.parse_args()

    if args.command == "search":
        sources = ["pexels", "pixabay"] if args.source == "both" else [args.source]
        results = []
        for source in sources:
            try:
                results += search(source, args.query, args.orientation, args.limit)
            except SystemExit as exc:
                if args.source != "both":
                    raise
                print(f"skipped {source}: {exc}", file=sys.stderr)
        results = [c for c in results if (c["duration"] or 0) >= args.min_duration]
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(download(args.source, args.id, Path(args.out), args.target_long), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
