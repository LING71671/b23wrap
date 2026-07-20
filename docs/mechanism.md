# 机制说明

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

```text
用户点 b23.tv/xxx
  → 302 到 jump 长链
  → 浏览器 JS 常跳到 d.bilibili.com（唤起 App / 下载）
  → B 站 App 内可能 openScheme 打开 url= 目标
```

是否真正打开外站取决于当前客户端策略，桌面浏览器通常不会直接跳出。
