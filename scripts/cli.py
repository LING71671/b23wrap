#!/usr/bin/env python3
"""CLI: python scripts/cli.py https://www.example.com

Copyright (C) 2026 b23wrap contributors
SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from core import build_long_url, generate  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(
        description="b23wrap CLI — verified chains C1–C5 (see docs/chains.md)"
    )
    ap.add_argument("url", help="Target http(s) URL")
    ap.add_argument(
        "--long-only",
        action="store_true",
        help="Only print wrapped bilibili long URL (no API call)",
    )
    ap.add_argument(
        "--chain",
        default="c1",
        help="c1 (default), c2 (biliapi host), c4/nest2, c5/nest-jump",
    )
    ap.add_argument(
        "--api-host",
        choices=("bilibili", "biliapi"),
        default=None,
        help="share/click host (default bilibili; c2 implies biliapi)",
    )
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    chain = args.chain
    api_host = args.api_host
    if chain.strip().lower() == "c2":
        chain = "c1"
        api_host = api_host or "biliapi"

    if args.long_only:
        long_url = build_long_url(args.url, chain)
        if args.json:
            print(
                json.dumps(
                    {"long_url": long_url, "chain": args.chain},
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            print(long_url)
        return 0

    try:
        result = generate(args.url, chain=chain, api_host=api_host)
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("target :", result["target"])
        print("chain  :", result.get("chain") or "")
        print("long   :", result["long_url"])
        print("b23    :", result["short_url"])
        print("api    :", result.get("share_api") or "")
        print("loc    :", result.get("location") or "")
        print(
            "note   : 请在 B 站 App 内打开短链才会跳到目标站；"
            "普通浏览器通常不会跳转。链路图见 docs/chains.md"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
