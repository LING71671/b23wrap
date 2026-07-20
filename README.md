# web2bilibili

实验室工具：把**任意 http(s) 网址**包装成 B 站会员购 `jump.html` 长链，再调用官方分享接口签发真实 **`b23.tv`** 短链。

> **仅限本地防御研究 / 机制复现。禁止钓鱼、引流、传播违规内容。**

## 目录

```text
web2bilibili/
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

- Python 3.10+（仅标准库，无第三方依赖）
- 可访问 `api.bilibili.com`

## 启动 Web

```powershell
cd B:\web2bilibili
python app\server.py
```

或双击 `start.bat`。

浏览器打开：http://127.0.0.1:8765/

## 命令行

```powershell
# 完整：生成 b23
python scripts\cli.py https://www.baidu.com

# 只要包装长链（不调 API）
python scripts\cli.py https://www.baidu.com --long-only

# JSON 输出
python scripts\cli.py https://www.baidu.com --json
```

## API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/health` | 健康检查 |
| POST | `/api/generate` | `{"url":"https://..."}` → b23 |

示例：

```powershell
python -c "import urllib.request,json; r=urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765/api/generate',data=json.dumps({'url':'https://www.baidu.com'}).encode(),headers={'Content-Type':'application/json'})); print(r.read().decode())"
```

## 原理摘要

1. 目标 `T` → `bilibili://mall/web?url=T`
2. 包进 `d.bilibili.com/?schema=...`
3. 包进 `mall.bilibili.com/jump.html?Url=...`（`*.bilibili.com`，可被缩短）
4. `POST https://api.bilibili.com/x/share/click`  
   `share_id=public.webview.0.0.pv`，`oid=长链`，`share_channel=COPY`
5. 返回官方 `https://b23.tv/xxxxx`

参考：[bilibili-API-collect · b23tv.md](https://github.com/pskdje/bilibili-API-collect/blob/main/docs/misc/b23tv.md)

## 限制

| 点 | 说明 |
|---|---|
| 短链真实 | 由 B 站签发，非伪造域名 |
| 桌面浏览器 | 打开 b23 常停在 `d.bilibili.com` |
| 真机 App | 才可能执行 `mall/web` 打开外站（策略可变） |
| 接口风控 | `/x/share/click` 可能变更或失败 |

## License

见 `DISCLAIMER.md`。代码仅供安全研究与教育。
