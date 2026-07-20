# A1 最终产物

> Sink: `https://www.baidu.com`  
> App 期望: **到达百度**  
> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。

_批次: 2026-07-21 01:04 · `report/run_valuable.py`_

主滥用原型：mall jump + mall/web + public.webview，T=baidu。

## 产物表

| id | 成功 | short_url / 测试 URL | 备注 | App |
|----|------|----------------------|------|-----|
| a1_baidu | ✅ | `https://b23.tv/r7i1YAD` | core.generate | **✅ 成功** |

## 复制列表

```text
https://b23.tv/r7i1YAD
```

## App 实测登记

| 时间 | 结果 | 记录 |
|------|------|------|
| 2026-07-21 01:10:35 | **✅ 成功** | 到达百度（完整 A1 包装） |
