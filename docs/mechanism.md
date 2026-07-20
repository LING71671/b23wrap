# 机制说明

> 本文描述技术流程。完整**已验证成功链路**与流程图见 **[chains.md](./chains.md)**。  
> 使用见 [DISCLAIMER.md](../DISCLAIMER.md)。

## 两层能力

| 层 | 做什么 | 关键点 |
|---|---|---|
| A. 短链签发 | 任意 `*.bilibili.com` URL → `b23.tv` | `POST /x/share/click` |
| B. 长链包装 | 站内 URL 内嵌目标网址 | `jump.html` + `bilibili://mall/web?url=` |

默认产品路径 **C1**：先 B 再 A。已证实变体 **C2–C5** 见 [chains.md](./chains.md)。

## C1 长链结构

```text
https://mall.bilibili.com/jump.html
  ?Url=https://d.bilibili.com/?schema=bilibili://mall/web?url=<URLENCODE(T)>
```

- 外层 host 是 `mall.bilibili.com` → 满足短链域名要求  
- **必杀组件**：`bilibili://mall/web?url=`（App 内打开外站依赖此 scheme）

## 签发接口

```text
POST https://api.bilibili.com/x/share/click
  （C2 可用 https://api.biliapi.net/x/share/click）
Content-Type: application/x-www-form-urlencoded

platform=android
share_channel=COPY
share_id=public.webview.0.0.pv
share_mode=4
oid=<完整站内长链>
buvid=<非空>
build=7710300
```

成功时 `data.content` 含 `https://b23.tv/xxxxx`。

文档参考：社区 `bilibili-API-collect` → `docs/misc/b23tv.md`。

## 打开后的行为

**核心结论：外站跳转基本只在 B 站 App 里点开时才可能发生。**

```text
用户点 b23.tv/xxx
  → 302 到 jump 长链（仍是 bilibili 域）
  → 【普通浏览器】常停在 d.bilibili.com → 到不了目标站
  → 【B 站 App 内】openScheme 执行 bilibili://mall/web?url=目标 → 可能打开目标站
```

| 环境 | 会不会到你填的网址 |
|---|---|
| B 站 App 内打开短链 | 可能（C1–C5 已在实验中对 baidu sink 证实） |
| 系统浏览器 / 桌面浏览器 | 通常不会 |
| 微信等内置浏览器 | 通常不会 |

## 代码入口

| 函数 | 作用 |
|------|------|
| `build_jump_long_url` / `build_long_url` | C1 / C4 / C5 包装 |
| `mint_b23` | 签发（可选 `api_host=biliapi` → C2） |
| `generate` | 全流程 |

CLI：`python scripts/cli.py <url> [--chain c1|c2|c4|c5] [--api-host biliapi]`
