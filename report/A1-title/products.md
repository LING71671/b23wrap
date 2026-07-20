# A1-title 最终产物

> Sink: `https://www.baidu.com`  
> App 期望: **到达百度（文案仅社工面）**  
> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。

_批次: 2026-07-21 01:04 · `report/run_valuable.py`_

A1 载荷 + `share_title`/`share_content`：看 `api_content` 是否被诱导文案污染。

## 产物表

| id | 成功 | short_url / 测试 URL | 备注 | App |
|----|------|----------------------|------|-----|
| title_clean | ✅ | `https://b23.tv/4BwUmD3` | title='官方活动入口' content='点击查看详情' raw_content='https://b23.tv/4BwUmD3' | ⬜ |
| title_neutral | ✅ | `https://b23.tv/wI3Fm2I` | title='分享链接' content=None raw_content='https://b23.tv/wI3Fm2I' | ⬜ |

## 复制列表

```text
https://b23.tv/4BwUmD3
https://b23.tv/wI3Fm2I
```

## App 实测登记

测完把上表 App 列改为 ✅/❌/🟨，并更新本目录 README 状态。
