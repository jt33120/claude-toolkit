#!/usr/bin/env python3
"""Generate a batch of Grok Imagine shots in the user's own logged-in browser, one at a time, at human pace.

Usage:
    python grok_batch.py login [--profile DIR]
    python grok_batch.py run shots.json --steps grok_steps.json [--out public/ai] [--max 15] [--pause 30-90]
    python grok_batch.py check shots.json [--out public/ai]

`login` opens a dedicated browser profile: sign in to Grok once, then close the window.
`run` replays the calibrated steps for each missing shot, saves <out>/<id>.<ext> and logs the prompt
in <out>/ai-credits.json. It stops at the first captcha, usage limit or unknown screen: it never
tries to get past them. Shots already on disk are skipped, so a run can be resumed.
Requires: pip install playwright (uses the installed Google Chrome).
"""

import argparse
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PROFILE = Path.home() / ".grok-robot-profile"
TOOL = "Grok Imagine (subscription, web)"
MEDIA_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "video/mp4": ".mp4"}


class Stop(Exception):
    """Raised when the run must end and the user takes over."""


def load_shots(path):
    shots = json.loads(Path(path).read_text(encoding="utf-8"))
    ids = [s.get("id") for s in shots]
    if not all(ids) or len(ids) != len(set(ids)):
        raise SystemExit("Every shot needs a unique non-empty id.")
    if not all(s.get("prompt") for s in shots):
        raise SystemExit("Every shot needs a prompt.")
    return shots


def done_ids(out):
    return {p.stem for p in Path(out).glob("*") if p.suffix in MEDIA_EXT.values()}


def pending(shots, out):
    finished = done_ids(out)
    return [s for s in shots if s["id"] not in finished]


def render(value, shot):
    try:
        return value.format_map(shot) if isinstance(value, str) else value
    except KeyError as exc:
        raise SystemExit(f"Shot {shot['id']} has no field {exc} required by the steps file.")


def applies(step, shot):
    return all(str(shot.get(k)) == str(v) for k, v in step.get("when", {}).items())


def parse_pause(text):
    low, _, high = text.partition("-")
    low, high = float(low), float(high or low)
    if low < 0 or high < low:
        raise SystemExit("--pause must look like 30-90 (seconds).")
    return low, high


def locate(page, target, shot):
    """Build a Playwright locator from a JSON target: role/name, text, label, placeholder, testid or css."""
    t = {k: render(v, shot) for k, v in target.items()}
    if "role" in t:
        loc = page.get_by_role(t["role"], name=t.get("name"), exact=t.get("exact", False)) if t.get("name") \
            else page.get_by_role(t["role"])
    elif "text" in t:
        loc = page.get_by_text(t["text"], exact=t.get("exact", False))
    elif "label" in t:
        loc = page.get_by_label(t["label"])
    elif "placeholder" in t:
        loc = page.get_by_placeholder(t["placeholder"])
    elif "testid" in t:
        loc = page.get_by_test_id(t["testid"])
    elif "css" in t:
        loc = page.locator(t["css"])
    else:
        raise SystemExit(f"Unknown target {target}")
    if "nth" in t:
        loc = loc.nth(int(t["nth"]))
    return loc


def record(out, entry):
    path = Path(out) / "ai-credits.json"
    credits = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    credits = [c for c in credits if c.get("file") != entry["file"]] + [entry]
    path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_stops(page, config, shot):
    for target in config.get("stop_if_visible", []):
        if locate(page, target, shot).first.is_visible():
            raise Stop(f"stop condition visible ({target}) — finish manually, then rerun.")


def save(path_stem, data, content_type):
    ext = MEDIA_EXT.get(content_type.split(";")[0].strip())
    if not ext:
        raise Stop(f"unexpected media type {content_type!r}")
    target = path_stem.with_suffix(ext)
    target.write_bytes(data)
    return target


def run_shot(page, config, shot, out):
    page.goto(config["url"])
    stem = Path(out) / shot["id"]
    saved = None
    for step in config["steps"]:
        if not applies(step, shot):
            continue
        check_stops(page, config, shot)
        action, timeout = step["do"], step.get("timeout", 30) * 1000
        if action == "wait":
            time.sleep(step["seconds"])
            continue
        loc = locate(page, step["target"], shot)
        try:
            loc.wait_for(state="visible", timeout=timeout)
        except Exception:
            check_stops(page, config, shot)
            raise Stop(f"step {step} not found — Grok's page changed: recalibrate grok_steps.json.")
        if action == "fill":
            loc.fill(render(step["value"], shot))
        elif action == "click":
            loc.click()
        elif action == "press":
            loc.press(step["key"])
        elif action == "download":
            with page.expect_download(timeout=timeout) as info:
                loc.click()
            download = info.value
            suffix = Path(download.suggested_filename).suffix or ".bin"
            saved = stem.with_suffix(suffix)
            download.save_as(saved)
        elif action == "save_media":
            src = loc.get_attribute("src")
            response = page.context.request.get(src)
            saved = save(stem, response.body(), response.headers.get("content-type", ""))
        elif action != "wait_for":
            raise SystemExit(f"Unknown action {action}")
        time.sleep(random.uniform(0.8, 2.5))
    if not saved:
        raise Stop(f"shot {shot['id']}: the steps file has no download or save_media step.")
    return saved


def browser(profile):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("pip install playwright  (Google Chrome must be installed)")
    manager = sync_playwright().start()
    context = manager.chromium.launch_persistent_context(
        str(profile), channel="chrome", headless=False, accept_downloads=True)
    return manager, context


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    login = sub.add_parser("login")
    login.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    check = sub.add_parser("check")
    check.add_argument("shots")
    check.add_argument("--out", default="public/ai")
    run = sub.add_parser("run")
    run.add_argument("shots")
    run.add_argument("--steps", required=True)
    run.add_argument("--out", default="public/ai")
    run.add_argument("--max", type=int, default=15)
    run.add_argument("--pause", default="30-90")
    run.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    args = parser.parse_args()

    if args.command == "check":
        missing = pending(load_shots(args.shots), args.out)
        print(json.dumps({"missing": [s["id"] for s in missing]}, indent=2))
        return
    if args.command == "login":
        manager, context = browser(args.profile)
        context.pages[0].goto("https://grok.com")
        print("Sign in, then close the browser window.")
        context.wait_for_event("close", timeout=0)
        manager.stop()
        return

    shots = load_shots(args.shots)
    config = json.loads(Path(args.steps).read_text(encoding="utf-8"))
    low, high = parse_pause(args.pause)
    todo = pending(shots, args.out)[: args.max]
    Path(args.out).mkdir(parents=True, exist_ok=True)
    manager, context = browser(args.profile)
    page = context.pages[0] if context.pages else context.new_page()
    report = {"saved": [], "stopped": None}
    try:
        for index, shot in enumerate(todo):
            if index:
                time.sleep(random.uniform(low, high))
            saved = run_shot(page, config, shot, args.out)
            record(args.out, {"file": saved.name, "id": shot["id"], "prompt": shot["prompt"],
                              "type": shot.get("type"), "tool": TOOL,
                              "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
            report["saved"].append(saved.name)
    except Stop as exc:
        report["stopped"] = str(exc)
    finally:
        context.close()
        manager.stop()
    report["missing"] = [s["id"] for s in pending(shots, args.out)]
    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(1 if report["stopped"] else 0)


if __name__ == "__main__":
    main()
