# 有价值链路 · 实测摘要（含 App 终判）

| 项 | 内容 |
|----|------|
| 服务端批次 | 2026-07-21 · [`run_valuable.py`](./run_valuable.py) |
| App 实测 | **2026-07-21 01:10–01:20**（你提供，两批） |
| Sink | `https://www.baidu.com` |
| 原始 dump | 不入库（`.gitignore`）；本地重跑 `python report/run_valuable.py` |

---

## App 实测记录（原始）

| 时间 | 产物 | 结果 |
|------|------|------|
| 01:10:35 | https://b23.tv/r7i1YAD | **✅ 成功**（到百度） |
| 01:11:32 | https://b23.tv/fa4qc6b | **❌ 疑似失败** — 停在 `jump.html?Url=https://www.baidu.com&…&outsideMall=yes` **空白页**，未进百度 |
| 01:11:58 | https://b23.tv/iu3kxoO | **❌ 失败** — 无下一步跳转 |
| 01:12:17 | https://b23.tv/kyr7SC6 | **✅ 成功**（到百度） |
| 01:12:54 | https://b23.tv/SEQOYA2 | **🟨 部分** — 「网页无法打开」，但**疑似已出站**（webview scheme） |
| 01:18:29 | https://b23.tv/sAzFlNW | **✅ 成功**（显式 mall/web） |
| 01:18:48 | https://b23.tv/SK2iK31 | **✅ 成功**（标准 A1） |
| 01:19:24 | https://b23.tv/J1QbDa5 | **✅ 成功** — 到百度，过程中**似跳了两次 bilibili**（双层嵌套） |
| 01:19:47 | https://b23.tv/1C9lzGI | **✅ 成功**（jump 套 jump） |
| 01:20:16 | https://b23.tv/xaTIl20 | **❌** 网页无法打开（link scheme） |
| 01:20:40 | https://b23.tv/9w33Xka | **❌** 网页无法打开（http scheme） |

---

## 总览（签发 vs App）

| ID | 服务端签发 | App 终判 | 结论 |
|----|------------|----------|------|
| **A1** | ✅ | **✅ 成功** | 完整三层包装有效；`sAzFlNW` / `SK2iK31` / `r7i1YAD` 均证实 |
| **A1-alt-host** | ✅ | **✅ 成功** | 换 `biliapi.net` 不影响落地 |
| **A1-title** | ✅ 签发 / title 未进文案 | 未单独测 | 载荷同 A1，预期成功 |
| **A2 jump?Url=外站** | ✅ 能签发 | **❌ 空白页** | 半吊子 |
| **A2 d?schema=https 外站** | ✅ 能签发 | **❌ 无跳转** | 无效外跳 |
| **A2 webview scheme** | ✅ | **🟨 打开失败** | 疑似出站意图 |
| **A2 link / http scheme** | ✅ | **❌ 网页无法打开** | 不构成有效落地 |
| **B-mint-policy** | ✅ 策略符合 | — | 外站直接 oid 不行 |
| **B-nest** | ✅ | **✅ 成功** | 双层/jump套jump **仍到百度**；可能多一次站内跳 |
| **A3 / A4** | — | — | 未覆盖 |

---

## 安全含义（给排查）

```text
有效滥用（已证实）:
  T=baidu
    → bilibili://mall/web?url=T
    → d.bilibili.com?schema=…
    → mall.bilibili.com/jump.html?Url=…
    → public.webview → b23
    → App 内打开 → 到 T

无效/半吊子（能签发、App 不到 T）:
  jump.html?Url=T 直接          → b23 → App 空白
  d.bilibili.com?schema=T(http) → b23 → 无跳转
```

| 点 | 说明 |
|----|------|
| **必杀组件** | `bilibili://mall/web?url=`（经 d. + jump；嵌套多层仍有效） |
| **嵌套** | 双层/jump套jump **仍成功到外站**；用户可能感到多跳一次站内 |
| **仅 jump?Url=外站** | 可污染 b23，App **空白**，非完整滥用 |
| **link / http / webview scheme** | 签发或出站感有，**落地失败或不可用** |
| **签发域名** | `api.bilibili.com` / `api.biliapi.net` 均可用 |
| **治理建议** | 重点解 oid 内 **mall/web** 与多层 jump/schema；裸 `Url=外站` 优先级低于 mall/web |

---

## 产物 App 状态（齐）

| short | 路径 | App |
|-------|------|-----|
| https://b23.tv/r7i1YAD | A1 | ✅ |
| https://b23.tv/kyr7SC6 | A1-alt-host | ✅ |
| https://b23.tv/sAzFlNW | mall/web 显式 | ✅ |
| https://b23.tv/SK2iK31 | A1 标准 | ✅ |
| https://b23.tv/J1QbDa5 | B-nest 双层 | ✅（似两次 bilibili） |
| https://b23.tv/1C9lzGI | B-nest jump套jump | ✅ |
| https://b23.tv/fa4qc6b | jump Url=外站 | ❌ 空白 |
| https://b23.tv/iu3kxoO | d schema=http | ❌ |
| https://b23.tv/SEQOYA2 | webview | 🟨 无法打开 |
| https://b23.tv/xaTIl20 | link | ❌ 无法打开 |
| https://b23.tv/9w33Xka | http | ❌ 无法打开 |

主结论已齐，**暂无新的必测链接**。可选：A1-title（`4BwUmD3`）确认无差别，可跳过。

---

## 复现签发

```bash
python report/run_valuable.py          # 本地生成 results.json / batch_results.json（已 gitignore）
python scripts/cli.py https://www.baidu.com
```
