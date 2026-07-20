# 机制说明

> 本文仅描述技术流程，不构成对任何平台策略的规避建议。使用见 [DISCLAIMER.md](../DISCLAIMER.md)。

## 两层能力

| 层 | 做什么 | 关键点 |
|---|---|---|
| A. 短链签发 | 任意 `*.bilibili.com` URL → `b23.tv` | `POST /x/share/click` |
| B. 长链包装 | 站内 URL 内嵌目标网址 | `jump.html` + `bilibili://mall/web?url=` |

b23wrap 同时做 A + B：先把目标 `T` 包进站内长链，再签发 b23。

## 长链结构

```text
https://mall.bilibili.com/jump.html
  ?Url=https://d.bilibili.com/?schema=bilibili://mall/web?url=<URLENCODE(T)>
```

- 外层 host 是 `mall.bilibili.com` → 满足短链域名要求
- 目标地址在 `url=` 参数里

## 签发接口（社区文档）

```text
POST https://api.bilibili.com/x/share/click
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

文档参考：`bilibili-API-collect` → `docs/misc/b23tv.md`。

## 打开后的行为

**核心结论：指定网站的跳转，基本只在 B 站 App 里点开时才可能发生。**

```text
用户点 b23.tv/xxx
  → 302 到 jump 长链（仍是 bilibili 域）
  → 【普通浏览器】JS 常停在 d.bilibili.com（唤起/下载页）→ 到不了目标站
  → 【B 站 App 内】可能 openScheme 执行 bilibili://mall/web?url=目标 → 才可能打开目标站
```

| 环境 | 会不会到你填的网址 |
|---|---|
| B 站 App 内打开短链 | 可能（取决于客户端是否允许该 `url=`） |
| 系统浏览器 / 桌面浏览器 | 通常不会 |
| 微信等内置浏览器 | 通常不会（或只引导去 App） |

本工具只负责「签发带包装参数的官方短链」，**不能**让短链在任意 App 外浏览器里变成通用跳转器。
