"""Core: wrap external URL + mint official b23.tv via Bilibili share API.

Copyright (C) 2026 b23wrap contributors
SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

SHARE_API_DEFAULT = "https://api.bilibili.com/x/share/click"
SHARE_API_BILIAPI = "https://api.biliapi.net/x/share/click"
SHARE_API = SHARE_API_DEFAULT

# Verified successful chains (App-confirmed); see docs/chains.md
CHAIN_IDS = ("c1", "c2", "c4", "c5")
# c3 ≡ c1 (explicit mall/web is the same builder)

API_HOSTS = {
    "bilibili": SHARE_API_DEFAULT,
    "biliapi": SHARE_API_BILIAPI,
}

UA = (
    "Mozilla/5.0 BiliDroid/7.71.0 (bbcallen@gmail.com) "
    "os/android model/Pixel mobi_app/android build/7710300"
)


def normalize_target(url: str) -> str:
    url = (url or "").strip()
    if not url:
        raise ValueError("请输入目标网址")
    if not re.match(r"^https?://", url, re.I):
        url = "https://" + url
    p = urllib.parse.urlparse(url)
    if not p.netloc or "." not in p.netloc:
        raise ValueError("网址格式不正确")
    if p.scheme not in ("http", "https"):
        raise ValueError("仅支持 http/https")
    return url


def build_jump_long_url(target: str) -> str:
    """
    C1/C3: Nest target into Bilibili mall jump / deep-link long URL.

    target
      -> bilibili://mall/web?url=<target>
      -> d.bilibili.com/?schema=...
      -> mall.bilibili.com/jump.html?Url=...
    """
    target = normalize_target(target)
    schema = "bilibili://mall/web?url=" + urllib.parse.quote(target, safe="")
    d_url = "https://d.bilibili.com/?" + urllib.parse.urlencode({"schema": schema})
    return "https://mall.bilibili.com/jump.html?" + urllib.parse.urlencode({"Url": d_url})


def build_long_url(target: str, chain: str = "c1") -> str:
    """
    Build stand-in long URL for a verified chain id.

    chain:
      c1 / c3 — standard triple wrap (default)
      c4 / nest2 — C1(C1(T))
      c5 / nest-jump — jump.html?Url=<C1(T)>
    """
    chain = (chain or "c1").strip().lower().replace("_", "-")
    if chain in ("c1", "c3", "standard", "default"):
        return build_jump_long_url(target)
    if chain in ("c4", "nest2", "double"):
        inner = build_jump_long_url(target)
        return build_jump_long_url(inner)
    if chain in ("c5", "nest-jump", "jump-jump"):
        inner = build_jump_long_url(target)
        return "https://mall.bilibili.com/jump.html?" + urllib.parse.urlencode(
            {"Url": inner}
        )
    raise ValueError(
        f"未知 chain={chain!r}，可选: c1, c3, c4/nest2, c5/nest-jump（见 docs/chains.md）"
    )


def resolve_share_api(api_host: str | None = None, api_url: str | None = None) -> str:
    if api_url:
        return api_url.strip()
    key = (api_host or "bilibili").strip().lower()
    if key not in API_HOSTS:
        raise ValueError(f"未知 api_host={api_host!r}，可选: bilibili, biliapi")
    return API_HOSTS[key]


def mint_b23(
    long_url: str,
    *,
    api_host: str | None = None,
    api_url: str | None = None,
) -> dict:
    """
    Mint official b23.tv via POST /x/share/click
    share_id=public.webview.0.0.pv, oid=<bilibili.com long URL>
    """
    api = resolve_share_api(api_host, api_url)
    params = {
        "platform": "android",
        "share_channel": "COPY",
        "share_id": "public.webview.0.0.pv",
        "share_mode": "4",
        "oid": long_url,
        "buvid": "XY" + uuid.uuid4().hex[:30].upper(),
        "build": "7710300",
        "share_session_id": str(uuid.uuid4()),
        "ts": str(int(time.time())),
    }
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
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"B站接口 HTTP {e.code}: {body[:200]}") from e
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"请求 B站接口失败: {e}") from e

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"接口返回非 JSON: {body[:200]}") from e

    if payload.get("code") not in (0, "0"):
        raise RuntimeError(
            f"接口错误 code={payload.get('code')} msg={payload.get('message')}"
        )

    content = ((payload.get("data") or {}).get("content") or "").strip()
    m = re.search(r"https?://b23\.tv/[A-Za-z0-9]+", content)
    if not m:
        raise RuntimeError(
            "接口未返回 b23 短链（可能被风控或参数失效）。"
            f" raw={json.dumps(payload, ensure_ascii=False)[:300]}"
        )
    return {
        "short_url": m.group(0),
        "api_content": content,
        "api_raw": payload,
        "share_api": api,
    }


def resolve_b23(short_url: str) -> str | None:
    """One-shot GET, return Location if 3xx."""

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


def generate(
    target: str,
    *,
    chain: str = "c1",
    api_host: str | None = None,
) -> dict:
    """
    Full pipeline: target URL -> long URL (chain) -> b23 -> Location probe.

    chain: c1 (default), c4/nest2, c5/nest-jump
    api_host: bilibili (default) or biliapi  → C2 when biliapi + c1
    """
    target = normalize_target(target)
    chain_n = (chain or "c1").strip().lower()
    # C2 = C1 wrap + biliapi host
    if chain_n in ("c2",):
        chain_n = "c1"
        api_host = api_host or "biliapi"
    long_url = build_long_url(target, chain_n)
    minted = mint_b23(long_url, api_host=api_host)
    location = resolve_b23(minted["short_url"])
    chain_label = "c2" if (api_host or "bilibili") == "biliapi" and chain_n in (
        "c1",
        "c3",
        "standard",
        "default",
    ) else chain_n
    return {
        "ok": True,
        "target": target,
        "chain": chain_label,
        "long_url": long_url,
        "short_url": minted["short_url"],
        "location": location,
        "share_api": minted.get("share_api"),
        "api_content": minted["api_content"],
        "note": (
            "b23 由 B 站短链服务签发。"
            "只有在 B 站 App 内打开短链，才可能跳转到目标网站；"
            "普通浏览器通常停在 d.bilibili.com 等中转页，不会进入目标站。"
            "App 内是否允许打开外站仍取决于客户端策略。"
            "已验证链路见 docs/chains.md。"
        ),
        "open_in_bilibili_app_only": True,
        "lab_only": True,
    }
