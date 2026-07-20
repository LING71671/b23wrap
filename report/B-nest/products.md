# B-nest 最终产物

> Sink: `https://www.baidu.com`  
> App 期望: **到达百度（若客户端仍解析内层）**  
> 浏览器失败 ≠ 终判失败。终判以你在 **B 站 App** 内结果为准。

_批次: 2026-07-21 01:04 · `report/run_valuable.py`_

多层嵌套仍嵌入 baidu 后签发。成功者请在 App 验证是否仍到百度。

## 产物表

| id | 成功 | short_url / 测试 URL | 备注 | App |
|----|------|----------------------|------|-----|
| double_jump_via_core | ✅ | `https://b23.tv/J1QbDa5` | 双层 | **✅ 成功**（似两次 bilibili） 01:19:24 |
| standard_a1 | ✅ | `https://b23.tv/SK2iK31` | 标准 A1 | **✅ 成功** 01:18:48 |
| jump_of_jump | ✅ | `https://b23.tv/1C9lzGI` | jump套jump | **✅ 成功** 01:19:47 |

## 复制列表

```text
https://b23.tv/J1QbDa5
https://b23.tv/SK2iK31
https://b23.tv/1C9lzGI
```

## App 实测登记

| 时间 | 产物 | 结果 |
|------|------|------|
| 01:18:48 | SK2iK31 | **✅** 成功 |
| 01:19:24 | J1QbDa5 | **✅** 成功；过程**好像跳了两次 bilibili** |
| 01:19:47 | 1C9lzGI | **✅** 成功 |

**结论**：多层嵌套 **不能** 靠「多包几层」规避落地；检测应递归解 Url/schema。
