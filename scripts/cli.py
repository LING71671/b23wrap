#!/usr/bin/env python3
"""CLI: python scripts/cli.py https://www.baidu.com"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from core import build_jump_long_url, generate  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="web2b-short CLI")
    ap.add_argument("url", help="Target http(s) URL")
    ap.add_argument(
        "--long-only",
        action="store_true",
        help="Only print wrapped bilibili long URL (no API call)",
    )
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    if args.long_only:
        long_url = build_jump_long_url(args.url)
        if args.json:
            print(json.dumps({"long_url": long_url}, ensure_ascii=False, indent=2))
        else:
            print(long_url)
        return 0

    try:
        result = generate(args.url)
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("target :", result["target"])
        print("long   :", result["long_url"])
        print("b23    :", result["short_url"])
        print("loc    :", result.get("location") or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
