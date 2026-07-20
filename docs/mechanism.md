# 机制说明

## 两层问题

| 层 | 做什么 | 关键点 |
|---|---|---|
| A. 短链签发 | 任意 `*.bilibili.com` URL → `b23.tv` | `POST /x/share/click` |
| B. 出站包装 | 让「站内 URL」里嵌外站 | `jump.html` + `bilibili://mall/web?url=` |

web2bilibili 同时做 A + B：先把外站 `T` 塞进站内长链，再签发 b23。

## 长链结构

```text
https://mall.bilibili.com/jump.html
  ?Url=https://d.bilibili.com/?schema=bilibili://mall/web?url=<URLENCODE(T)>
```

- 外层 host 是 `mall.bilibili.com` → 满足短链白名单
- 真正目标在 `url=` 参数里

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
  → B 站 App 内可能 openScheme 打开 url= 外站
```

**不能假设**所有环境都会自动打开外站；以当前客户端策略为准。

## 与样本对照

真实滥用样本常见：

- `share_from=h5` + `share_source=QQ|COPY`
- `unique_k` = 短码
- Location 落在 `mall.../jump.html?Url=...外站`

本工具生成的 Location 形态与之同构（终点可换为实验用域名）。
