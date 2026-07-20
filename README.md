# b23wrap

本地工具：把 **任意 http(s) 网址** 包装成 B 站会员购 `jump.html` 长链，再调用官方分享接口签发真实 **`b23.tv`** 短链。

> **仅限本地研究与机制验证。请遵守法律与平台规则。**

## 目录

```text
b23wrap/
├── app/
│   ├── core.py          # 长链包装 + /x/share/click 签发
│   ├── server.py        # 本地 Web UI + API
│   └── static/          # 前端
├── scripts/
│   └── cli.py           # 命令行
├── docs/
│   └── mechanism.md     # 原理说明
├── start.bat            # Windows 一键启动
├── DISCLAIMER.md
└── README.md
```

## 环境

- Python 3.10+（仅标准库）
- 可访问 `api.bilibili.com`

## 启动 Web

```powershell
cd B:\b23wrap
python app\server.py
```

或双击 `start.bat`。

浏览器：http://127.0.0.1:8765/

## 命令行

```powershell
python scripts\cli.py https://www.baidu.com
python scripts\cli.py https://www.baidu.com --long-only
python scripts\cli.py https://www.baidu.com --json
```

## API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/health` | 健康检查 |
| POST | `/api/generate` | `{"url":"https://..."}` → b23 |

## 原理摘要

1. 目标 `T` → `bilibili://mall/web?url=T`
2. 包进 `d.bilibili.com/?schema=...`
3. 包进 `mall.bilibili.com/jump.html?Url=...`
4. `POST https://api.bilibili.com/x/share/click`（`public.webview.0.0.pv`）
5. 得到官方 `https://b23.tv/xxxxx`

参考：[bilibili-API-collect · b23tv.md](https://github.com/pskdje/bilibili-API-collect/blob/main/docs/misc/b23tv.md)

## 限制

| 点 | 说明 |
|---|---|
| 短链真实 | 由 B 站签发 |
| 桌面浏览器 | 打开 b23 常停在 `d.bilibili.com` |
| 真机 App | 是否打开目标页取决于客户端策略 |
| 接口风控 | `/x/share/click` 可能变更或失败 |

## License

见 `DISCLAIMER.md`。
