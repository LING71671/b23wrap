# b23wrap

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/downloads/)

**开源本地工具箱**：将任意 `http(s)` URL 包装为 B 站会员购 `jump.html` 长链，并调用公开分享接口签发官方 **`b23.tv`** 短链。

> ⚠️ **请先阅读 [DISCLAIMER.md](./DISCLAIMER.md)。**  
> 本项目非 B 站官方产品；仅供学习、研究与本地实验。请遵守法律与平台规则。

### 重要：跳转只在 B 站内生效

生成的 `b23.tv` **不会在普通浏览器里直接打开你填的网址**。

| 打开方式 | 常见结果 |
|---|---|
| **B 站 App 内**点击短链 | 才可能执行 `mall/web`，打开你指定的目标站 |
| 系统浏览器 / 微信内置浏览器等 | 多半停在 `d.bilibili.com` 或官方中转/唤起页，**不会**自动跳到目标站 |
| 仅复制链接到电脑 Chrome 打开 | 同样通常**到不了**目标站 |

请把短链当作「**需在 B 站客户端内打开**」的链接，而不是通用外链短址。

---

## 功能

| 能力 | 说明 |
|---|---|
| 长链包装 | 目标 URL → `mall.bilibili.com/jump.html?Url=...` |
| 官方短链 | `POST /x/share/click` → `https://b23.tv/xxxxx` |
| Web UI | 浏览器本地操作 |
| CLI | 命令行一键生成 |
| HTTP API | `POST /api/generate` 便于脚本集成 |

**零第三方 Python 依赖**（仅标准库）。

---

## 快速开始

### 环境

- Python **3.10+**
- 可访问 `https://api.bilibili.com`

### Web 工具箱

```bash
# Windows
cd B:\b23wrap
python app/server.py

# 或
start.bat
```

浏览器打开：<http://127.0.0.1:8765/>

### 命令行

```bash
python scripts/cli.py https://www.example.com
python scripts/cli.py https://www.example.com --long-only   # 仅输出包装长链
python scripts/cli.py https://www.example.com --json
```

### API

```bash
# 健康检查
curl http://127.0.0.1:8765/api/health

# 生成（示例用 Python，避免 shell 转义问题）
python -c "import urllib.request,json; print(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765/api/generate', data=json.dumps({'url':'https://www.example.com'}).encode(), headers={'Content-Type':'application/json'})).read().decode())"
```

| 方法 | 路径 | 请求体 | 说明 |
|---|---|---|---|
| GET | `/api/health` | — | 服务状态 |
| POST | `/api/generate` | `{"url":"https://..."}` | 返回 `short_url` / `long_url` 等 |

---

## 仓库结构

```text
b23wrap/
├── app/
│   ├── core.py           # 核心逻辑
│   ├── server.py         # 本地 HTTP 服务
│   └── static/           # Web UI
├── scripts/
│   └── cli.py            # 命令行入口
├── docs/
│   └── mechanism.md      # 机制说明
├── LICENSE               # MIT
├── DISCLAIMER.md         # 免责声明（必读）
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── start.bat
└── README.md
```

---

## 原理（摘要）

1. 目标 `T` → `bilibili://mall/web?url=T`
2. 包入 `d.bilibili.com/?schema=...`
3. 包入 `mall.bilibili.com/jump.html?Url=...`（站内域名）
4. `POST https://api.bilibili.com/x/share/click`  
   `share_id=public.webview.0.0.pv`，`oid=<长链>`
5. 得到官方 `b23.tv` 短链

详见 [docs/mechanism.md](./docs/mechanism.md)。  
接口说明可参考社区文档：[bilibili-API-collect · b23.tv](https://github.com/SocialSisterYi/bilibili-API-collect)（及 fork 中的 `b23tv.md`）。

### 使用限制（技术）

| 点 | 说明 |
|---|---|
| 短链真实性 | 由 B 站服务签发，非本工具伪造域名 |
| **跳转场景** | **仅在 B 站 App（客户端）内打开时，才可能跳到指定网站** |
| 普通浏览器 | 打开短链常停在 `d.bilibili.com` 等官方中转页，**不会**进目标站 |
| 客户端策略 | App 是否允许打开外域 `url=` 取决于版本/风控，本工具无法保证 |
| 接口变更 | 分享接口可能调整或失败 |

---

## 免责声明

**完整条款见 [DISCLAIMER.md](./DISCLAIMER.md)。** 摘要：

- 非官方、无担保、使用者自担责任；
- 禁止用于欺诈、违法或误导性用途；
- 使用本软件即视为接受免责声明。

---

## 贡献

见 [CONTRIBUTING.md](./CONTRIBUTING.md)。欢迎 Issue / PR（文档、兼容性、错误处理等）。

## 安全

见 [SECURITY.md](./SECURITY.md)。请勿在 Issue 中公开可被滥用的实时攻击细节。

## License

[MIT](./LICENSE) © b23wrap contributors  

第三方商标（哔哩哔哩 / bilibili / b23.tv 等）归其权利人所有。
