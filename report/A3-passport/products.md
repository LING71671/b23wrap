# A3-passport 最终产物

> Sink: `https://www.baidu.com`  
> App 期望: **是否跳到百度或危险页（Web 侧）**  
> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。

_批次: 2026-07-21 01:04 · `report/run_valuable.py`_

开放重定向面探测（未登录）。`ok=✅` 仅表示 **HTTP Location/最终 URL 出现 baidu 字样**，不是完整登录链滥用。需你在浏览器/App Web 进一步确认。

## 产物表

| id | 成功 | short_url / 测试 URL | 备注 | App |
|----|------|----------------------|------|-----|
| passport_login_gourl_get | ✅ | `https://passport.bilibili.com/login?gourl=https%3A%2F%2Fwww.baidu.com` | status=200 loc='' err=None | ⬜ |
| passport_login_go_url | ✅ | `https://passport.bilibili.com/login?go_url=https%3A%2F%2Fwww.baidu.com` | status=200 loc='' err=None | ⬜ |
| www_login_gourl | ✅ | `https://www.bilibili.com/?gourl=https%3A%2F%2Fwww.baidu.com` | status=200 loc='' err=None | ⬜ |
| crossDomain_shape | ❌ | `https://passport.biligame.com/crossDomain?gourl=https%3A%2F%2Fwww.baidu.com` | status=302 loc='https://www.bilibili.com' err=None | ⬜ |

## 复制列表

```text
https://passport.bilibili.com/login?gourl=https%3A%2F%2Fwww.baidu.com
https://passport.bilibili.com/login?go_url=https%3A%2F%2Fwww.baidu.com
https://www.bilibili.com/?gourl=https%3A%2F%2Fwww.baidu.com
```

## App 实测登记

测完把上表 App 列改为 ✅/❌/🟨，并更新本目录 README 状态。
