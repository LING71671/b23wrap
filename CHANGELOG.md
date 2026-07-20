# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/) 风格。

## [Unreleased]

### Added

- 文档：README / chains — App 已证实成功链路 **C1–C5** 与流程图
- CLI / API：`--chain`（`c1`/`c2`/`c4`/`c5`）、`--api-host biliapi`
- `build_long_url`：双层嵌套（C4）、jump 套 jump（C5）
- Web UI / GitHub Pages：链路下拉选择 C1 / C2 / C4 / C5（与 core 对齐）

### Changed

- README 以 C1–C5 替代单一 L0 描述；默认行为仍为 C1

## [0.1.0] - 2026-07-20

### Added

- 核心：目标 URL → 会员购 `jump.html` 长链包装
- 核心：调用 `POST /x/share/click` 签发官方 `b23.tv`
- 本地 Web UI + `/api/generate` / `/api/health`
- CLI：`scripts/cli.py`
- 文档：机制说明、GPL-3.0 许可、完整免责声明
- 开源准备：CONTRIBUTING、SECURITY、CHANGELOG
- 明确说明：**仅在 B 站 App 内打开短链才可能跳到目标站**
- 前端：MIMO 风格浅色产品页 UI
- 许可证：GNU GPL v3

[0.1.0]: https://github.com/LING71671/b23wrap/releases/tag/v0.1.0
