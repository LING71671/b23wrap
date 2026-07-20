# A2-container 最终产物

> Sink: `https://www.baidu.com`  
> App 期望: **到达百度（仅当该容器真解析外链）**  
> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。

_批次: 2026-07-21 01:04 · `report/run_valuable.py`_

抽样：把 baidu 塞进不同站内 URL query 再 public.webview。「能签发」≠「App 会打开 baidu」；须 App 验证。

## 产物表

| id | 成功 | short_url / 测试 URL | 备注 | App |
|----|------|----------------------|------|-----|
| jump_Url | ✅ 签发 | `https://b23.tv/fa4qc6b` | 直链 Url=baidu | **❌ 空白页** |
| jump_url_lower | ❌ | `https://mall.bilibili.com/jump.html?url=…` | 未签发 | — |
| d_schema_http | ✅ 签发 | `https://b23.tv/iu3kxoO` | schema=https 外站 | **❌ 无跳转** |
| d_schema_mallweb | ❌ | `https://d.bilibili.com/?schema=bilibili%3A%2F%2Fmall%2Fweb%3Furl%3Dhttps%3A%2F%2Fwww.baidu.com` | mint_ok=False loc_mentions_baidu=True | ⬜ |
| www_link_url | ❌ | `https://www.bilibili.com/blackboard/link.html?url=https%3A%2F%2Fwww.baidu.com` | mint_ok=False loc_mentions_baidu=True | ⬜ |
| live_html_q | ❌ | `https://live.bilibili.com/p/html/live-app-hotrank/index.html?url=https%3A%2F%2Fwww.baidu.com` | mint_ok=False loc_mentions_baidu=True | ⬜ |
| link_jump_type | ❌ | `https://link.bilibili.com/?jump_type=browser&url=https%3A%2F%2Fwww.baidu.com` | mint_ok=False loc_mentions_baidu=True | ⬜ |
| search_keyword_url | ✅ | `https://b23.tv/TZoKMPz` | mint_ok=True loc_mentions_baidu=True | ⬜ |

## 复制列表

```text
https://b23.tv/fa4qc6b
https://b23.tv/iu3kxoO
https://b23.tv/TZoKMPz
```

## App 实测登记

| 时间 | 产物 | 结果 |
|------|------|------|
| 01:11:32 | fa4qc6b | **❌** 停在 jump.html（含 `Url=baidu`、`outsideMall=yes`）**空白**，未进百度 |
| 01:11:58 | iu3kxoO | **❌** 没有下一步跳转 |

**结论**：简化容器**能污染 b23**，但**当前 App 不构成完整外站落地**；有效滥用仍依赖 A1 的 `mall/web` 链。
