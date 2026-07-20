# B-mint-policy 最终产物

> Sink: `https://www.baidu.com`  
> App 期望: **无「到 baidu」终判（负例应无短链）**  
> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。

_批次: 2026-07-21 01:04 · `report/run_valuable.py`_

积木：baidu **直接** oid 应失败；站内应成功。成功的站内 b23 **不是**滥用终态。

## 产物表

| id | 成功 | short_url / 测试 URL | 备注 | App |
|----|------|----------------------|------|-----|
| neg_baidu_direct | ❌ | `-` | expect_ok=False actual_ok=False | ⬜ |
| pos_www_root | ✅ | `https://b23.tv/3puMWnW` | expect_ok=True actual_ok=True | ⬜ |
| neg_example | ❌ | `-` | expect_ok=False actual_ok=False | ⬜ |

## 复制列表

```text
https://b23.tv/3puMWnW
```

## App 实测登记

测完把上表 App 列改为 ✅/❌/🟨，并更新本目录 README 状态。
