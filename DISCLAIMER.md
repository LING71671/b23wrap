# 免责声明 / Disclaimer

**使用本软件即表示你已阅读、理解并同意本声明。**  
**By using this software, you acknowledge that you have read and agree to this disclaimer.**

---

## 中文

### 1. 性质与定位

`b23wrap` 是一个**开源命令行 / 本地 Web 工具箱**，用于：

- 理解 B 站短链（`b23.tv`）与分享相关接口的技术机制；
- 在**本地**生成包装后的站内长链，并调用公开接口获取官方短链；
- 研究、教学、接口联调与个人实验。

本项目**不是**哔哩哔哩（Bilibili）官方产品，与上海宽娱数码科技有限公司及其关联公司**无任何隶属或授权关系**。

### 1.1 跳转行为说明（必读）

本工具生成的 `b23.tv` 链接：

- **只有在哔哩哔哩客户端（B 站 App）内打开时**，才**有可能**跳转到你填写的目标网站；
- 在系统浏览器、桌面 Chrome、微信等**非 B 站 App 环境**中打开，通常**只会**停留在 B 站官方中转页（如 `d.bilibili.com` / 唤起 App 页），**不会**自动进入目标网站；
- 即便在 App 内，是否允许打开外站仍受 B 站客户端策略、版本与风控影响，**不保证**一定成功。

请勿将本工具宣传或理解为「任意环境都能跳转的通用短链服务」。

### 2. 使用者义务

你必须：

1. 遵守你所在司法辖区的法律法规；
2. 遵守 B 站用户协议、社区规范及接口使用惯例；
3. 仅在你有权操作的目标与场景下使用本工具；
4. 对你生成、分发、点击的链接及由此产生的一切后果**自行承担全部责任**。

### 3. 禁止用途

**严禁**将本工具用于（包括但不限于）：

- 钓鱼、欺诈、身份盗用、社会工程；
- 传播违法、侵权或平台禁止的内容；
- 对 B 站或第三方系统的未授权攻击、滥用或干扰；
- 任何以误导用户点击「看似 B 站官方短链」为目的的恶意行为。

### 4. 无担保

本软件按 **「现状 / AS IS」** 提供，不提供任何明示或暗示担保，包括但不限于：

- 适销性、特定用途适用性、不侵权；
- 接口持续可用、结果准确、不被风控或策略变更影响；
- 在任意客户端（浏览器 / App）中打开短链后的跳转行为。

B 站产品与接口可随时变更；本项目**不保证**功能长期有效。

### 5. 责任限制

在法律允许的最大范围内，作者与贡献者**不承担**因使用或无法使用本软件而导致的任何直接、间接、附带、特殊或后果性损害（包括数据丢失、业务中断、声誉损失等），无论基于合同、侵权或其他理论。

### 6. 第三方与商标

- 「哔哩哔哩」「bilibili」「b23.tv」等为相应权利人的商标或标识，本项目仅作技术描述使用。
- 本软件会请求 `api.bilibili.com` 等第三方服务；你与第三方之间的关系受其条款约束。

### 7. 开源许可

代码以 [MIT License](./LICENSE) 授权。  
**MIT 许可不减免你对本免责声明的遵守义务。** 若 MIT 与本声明在「责任限制 / 禁止用途」上可并存，则二者同时适用。

### 8. 联系与移除

若权利人认为本仓库存在侵权或不当内容，请通过 GitHub Issues（或发布页说明的联系方式）沟通，我们将尽快处理。

---

## English

### Nature

`b23wrap` is an **open-source local toolbox** for studying Bilibili short-link (`b23.tv`) related mechanisms. It is **not** an official Bilibili product and is **not affiliated with** or endorsed by Bilibili.

### Jump behavior (important)

Generated `b23.tv` links may open your target URL **only when opened inside the Bilibili app**. In a normal browser they typically stay on official intermediate pages (e.g. `d.bilibili.com`) and **do not** navigate to your target. Even in-app behavior depends on Bilibili client policy and is **not guaranteed**.

### Your responsibilities

You must comply with applicable laws, Bilibili’s terms, and platform rules. You are **solely responsible** for any links you generate, distribute, or open.

### Prohibited use

Do **not** use this software for phishing, fraud, malware distribution, unauthorized attacks, or any activity intended to deceive users via Bilibili-looking short links.

### No warranty / Limitation of liability

THE SOFTWARE IS PROVIDED **“AS IS”** WITHOUT WARRANTY OF ANY KIND. Authors and contributors shall not be liable for any damages arising from use of the software. Bilibili APIs and client behavior may change at any time.

### License

Source code is under the [MIT License](./LICENSE). This disclaimer applies in addition to the MIT license terms where compatible.
