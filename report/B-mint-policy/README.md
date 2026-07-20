# B-mint-policy

| 项 | 内容 |
|----|------|
| 状态 | 🟨 策略符合预期（积木） |
| 产物 | [products.md](./products.md) · 探针 [probe.py](./probe.py) |

| 用例 | 期望 | 实际 |
|------|------|------|
| oid=baidu 直接 | 无 b23 | ✅ 无 |
| oid=example 直接 | 无 b23 | ✅ 无 |
| oid=www.bilibili.com | 有 b23 | ✅ 有（**不是**滥用终态） |

证明：外站必须先包装。完整 probe 历史数据见同目录 `probe.py`。
