#!/usr/bin/env python3
"""L1 probe: pure *.bilibili.com oid -> share/click -> b23 + Location.

Writes JSON lines to report/B-mint-policy/raw_results.jsonl and a summary dict.
Research only; no credentials.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

SHARE_API = "https://api.bilibili.com/x/share/click"
UA = (
    "Mozilla/5.0 BiliDroid/7.71.0 (bbcallen@gmail.com) "
    "os/android model/Pixel mobi_app/android build/7710300"
)

OUT_DIR = Path(__file__).resolve().parent


def mint(oid: str) -> dict:
    params = {
        "platform": "android",
        "share_channel": "COPY",
        "share_id": "public.webview.0.0.pv",
        "share_mode": "4",
        "oid": oid,
        "buvid": "XY" + uuid.uuid4().hex[:30].upper(),
        "build": "7710300",
        "share_session_id": str(uuid.uuid4()),
        "ts": str(int(time.time())),
    }
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        SHARE_API,
        data=data,
        method="POST",
        headers={
            "User-Agent": UA,
            "Content-Type": "application/x-www-form-urlencoded",
            "App-Key": "android64",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            http_status = resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        http_status = e.code
    except Exception as e:  # noqa: BLE001
        return {
            "ok": False,
            "error": f"request_failed: {e}",
            "http_status": None,
            "payload": None,
            "short_url": None,
            "location": None,
        }

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return {
            "ok": False,
            "error": f"non_json: {body[:200]}",
            "http_status": http_status,
            "payload": None,
            "short_url": None,
            "location": None,
        }

    content = ((payload.get("data") or {}).get("content") or "").strip()
    m = re.search(r"https?://b23\.tv/[A-Za-z0-9]+", content)
    short = m.group(0) if m else None
    loc = resolve(short) if short else None
    ok = payload.get("code") in (0, "0") and bool(short)
    return {
        "ok": ok,
        "error": None if ok else "no_b23_in_content",
        "http_status": http_status,
        "code": payload.get("code"),
        "message": payload.get("message"),
        "api_content": content or None,
        "payload_data_keys": list((payload.get("data") or {}).keys()),
        "short_url": short,
        "location": loc,
        "payload_raw_trim": json.dumps(payload, ensure_ascii=False)[:400],
    }


def resolve(short_url: str) -> str | None:
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):  # noqa: ANN002, ANN003
            return None

    opener = urllib.request.build_opener(NoRedir)
    req = urllib.request.Request(short_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with opener.open(req, timeout=15) as resp:
            return resp.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.headers.get("Location") if e.headers else None
    except Exception:  # noqa: BLE001
        return None


def same_target(oid: str, location: str | None) -> dict:
    """Compare oid vs Location (ignore share tracking query on Location)."""
    if not location:
        return {"match": False, "reason": "no_location"}
    o = urllib.parse.urlparse(oid)
    l = urllib.parse.urlparse(location)
    host_ok = (o.netloc or "").lower() == (l.netloc or "").lower()
    # path: allow trailing slash difference
    op = (o.path or "/").rstrip("/") or "/"
    lp = (l.path or "/").rstrip("/") or "/"
    path_ok = op == lp
    # if oid had query keys, require them present in location (subset)
    oq = dict(urllib.parse.parse_qsl(o.query, keep_blank_values=True))
    lq = dict(urllib.parse.parse_qsl(l.query, keep_blank_values=True))
    query_subset = all(lq.get(k) == v for k, v in oq.items()) if oq else True
    match = host_ok and path_ok and query_subset
    return {
        "match": match,
        "host_ok": host_ok,
        "path_ok": path_ok,
        "query_subset": query_subset,
        "oid_host": o.netloc,
        "loc_host": l.netloc,
        "oid_path": op,
        "loc_path": lp,
    }


CASES: list[tuple[str, str, str]] = [
    # id, category, oid
    ("video_bv", "positive_core", "https://www.bilibili.com/video/BV1GJ411x7h7"),
    (
        "video_bv_query",
        "positive_core",
        "https://www.bilibili.com/video/BV1GJ411x7h7?p=1",
    ),
    ("video_av_path", "positive_core", "https://www.bilibili.com/video/av2"),
    ("space_mid", "positive_core", "https://space.bilibili.com/2"),
    ("www_root", "positive_core", "https://www.bilibili.com/"),
    ("www_no_slash", "positive_variant", "https://www.bilibili.com"),
    ("m_video", "positive_subdomain", "https://m.bilibili.com/video/BV1GJ411x7h7"),
    ("live_room", "positive_subdomain", "https://live.bilibili.com/1"),
    ("mall_home", "positive_subdomain", "https://mall.bilibili.com/"),
    ("search", "positive_subdomain", "https://search.bilibili.com/all?keyword=test"),
    (
        "bangumi_ep",
        "positive_subdomain",
        "https://www.bilibili.com/bangumi/play/ep307457",
    ),
    ("read_cv", "positive_subdomain", "https://www.bilibili.com/read/cv1"),
    ("t_dynamic", "positive_subdomain", "https://t.bilibili.com/"),
    ("message", "positive_subdomain", "https://message.bilibili.com/"),
    ("member", "positive_subdomain", "https://member.bilibili.com/"),
    ("show", "positive_subdomain", "https://show.bilibili.com/"),
    ("game", "positive_subdomain", "https://game.bilibili.com/"),
    ("manga", "positive_subdomain", "https://manga.bilibili.com/"),
    ("api_host", "positive_edge", "https://api.bilibili.com/x/web-interface/nav"),
    ("http_scheme", "positive_edge", "http://www.bilibili.com/video/BV1GJ411x7h7"),
    (
        "fragment",
        "positive_edge",
        "https://www.bilibili.com/video/BV1GJ411x7h7#reply",
    ),
    (
        "jump_html_self",
        "positive_edge",
        "https://mall.bilibili.com/jump.html?Url=https%3A%2F%2Fwww.bilibili.com%2F",
    ),
    # negatives
    ("ext_example", "negative", "https://www.example.com/"),
    ("ext_baidu", "negative", "https://www.baidu.com/"),
    ("ext_http_baidu", "negative", "http://www.baidu.com/"),
    ("lookalike_suffix", "negative", "https://www.bilibili.com.example.com/"),
    ("lookalike_prefix", "negative", "https://notbilibili.com/"),
    ("b23_as_oid", "negative_or_edge", "https://b23.tv/BV1GJ411x7h7"),
    ("empty_path_only_host", "positive_edge", "https://bilibili.com/"),
    ("www_with_port", "negative_or_edge", "https://www.bilibili.com:443/"),
]


def main() -> int:
    results = []
    jsonl = OUT_DIR / "raw_results.jsonl"
    if jsonl.exists():
        jsonl.unlink()

    for i, (cid, cat, oid) in enumerate(CASES):
        print(f"[{i + 1}/{len(CASES)}] {cid} ...", flush=True)
        row = {
            "id": cid,
            "category": cat,
            "oid": oid,
            "ts": int(time.time()),
        }
        minted = mint(oid)
        row.update(minted)
        if minted.get("location"):
            row["target_compare"] = same_target(oid, minted["location"])
        else:
            row["target_compare"] = None
        results.append(row)
        with jsonl.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        time.sleep(0.35)  # gentle pacing

    summary = {
        "total": len(results),
        "ok": sum(1 for r in results if r.get("ok")),
        "fail": sum(1 for r in results if not r.get("ok")),
        "by_category": {},
        "cases": results,
    }
    for r in results:
        c = r["category"]
        summary["by_category"].setdefault(c, {"ok": 0, "fail": 0})
        if r.get("ok"):
            summary["by_category"][c]["ok"] += 1
        else:
            summary["by_category"][c]["fail"] += 1

    out = OUT_DIR / "results.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"total": summary["total"], "ok": summary["ok"], "fail": summary["fail"], "by_category": summary["by_category"]}, ensure_ascii=False, indent=2))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
