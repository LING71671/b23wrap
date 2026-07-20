# 滥用场景实测报告

| 文档 | 说明 |
|------|------|
| **[SUMMARY.md](./SUMMARY.md)** | **签发 + App 终判总览** |
| [run_valuable.py](./run_valuable.py) | 复现脚本（产物 dump 默认不提交） |

**Sink**：`https://www.baidu.com`

## 状态（含你 01:10 批次 App 结果）

| ID | 服务端 | App 终判 | 说明 |
|----|--------|----------|------|
| **A1** | ✅ | **✅** | r7i1YAD / sAzFlNW / SK2iK31 |
| **A1-alt-host** | ✅ | **✅** | kyr7SC6 |
| A1-title | ✅ 签发 | 未单独测 | 可跳过 |
| A2-container | ✅ 可签发 | **❌** | 空白/无跳转 |
| A2-deeplink | ✅ | **mall/web✅** · link/http/webview❌🟨 | |
| A3-passport | 未证实 | — | |
| A4-* | 🚫 | — | |
| B-mint-policy | ✅ | — | |
| **B-nest** | ✅ | **✅** | 双层/套 jump 仍到百度 |
