# A2-deeplink 最终产物

> Sink: `https://www.baidu.com`  
> App 期望: **到达百度**  
> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。

_批次: 2026-07-21 01:04 · `report/run_valuable.py`_

把候选 `bilibili://…url=baidu` 包进 d.bilibili + jump 再签发。是否打开取决于客户端路由，必须 App 测。

## 产物表

| id | 成功 | short_url / 测试 URL | 备注 | App |
|----|------|----------------------|------|-----|
| mall_web | ✅ | `https://b23.tv/sAzFlNW` | mall/web | **✅ 成功** 01:18:29 |
| browser | ❌ | `-` | browser | — |
| webview | ✅ | `https://b23.tv/SEQOYA2` | webview | **🟨 无法打开** 01:12:54 |
| link | ✅ | `https://b23.tv/xaTIl20` | link | **❌ 无法打开** 01:20:16 |
| http | ✅ | `https://b23.tv/9w33Xka` | http | **❌ 无法打开** 01:20:40 |

## 复制列表

```text
https://b23.tv/sAzFlNW
https://b23.tv/SEQOYA2
https://b23.tv/xaTIl20
https://b23.tv/9w33Xka
```

## App 实测登记

| 时间 | 产物 | 结果 |
|------|------|------|
| 01:12:54 | SEQOYA2（webview） | **🟨** 网页无法打开，疑似出站 |
| 01:18:29 | sAzFlNW（mall/web） | **✅** 成功到百度 |
| 01:20:16 | xaTIl20（link） | **❌** 网页无法打开 |
| 01:20:40 | 9w33Xka（http） | **❌** 网页无法打开 |

**结论**：有效 deeplink 仍是 **`bilibili://mall/web?url=`**；`link`/`http`/`webview` 当前不能稳定完成落地。
