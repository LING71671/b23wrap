# A3-passport

| 项 | 内容 |
|----|------|
| 状态 | 🟨 未登录探测 **未证实** 开放重定向到 baidu |
| 产物 | [products.md](./products.md) |

| 探测 | 结果 |
|------|------|
| login?gourl=baidu | HTTP 200，无 Location→baidu |
| crossDomain?gourl=baidu | **302 → https://www.bilibili.com**（未到 baidu） |

需登录后完整 SSO 流再测；本轮不判 A3 滥用成立。
