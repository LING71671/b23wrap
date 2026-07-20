# 贡献指南

感谢关注 **b23wrap**。

## 开发

- Python 3.10+，无额外 pip 依赖
- 修改核心逻辑：`app/core.py`
- 修改 Web：`app/server.py`、`app/static/*`
- 本地验证：

```bash
python scripts/cli.py https://www.example.com --json
python app/server.py --port 8765
```

## 提交 PR 前

1. 确认未引入真实滥用样本、违规链接或隐私数据
2. 更新 `CHANGELOG.md`（如有用户可见变更）
3. 保持中立技术表述，避免教唆恶意用途的文案

## 行为准则

- 尊重他人，围绕技术改进讨论
- 不讨论如何大规模滥用短链或规避平台处置
- 维护者有权关闭不当 Issue / PR
