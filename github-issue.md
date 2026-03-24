# [i18n/zh-CN] 补充 Usage 页面及其他中文翻译

## 问题描述

当前 OpenClaw Control UI 的简体中文 (`zh-CN`) 翻译存在部分缺失，主要影响 **Usage (使用情况)** 页面，导致该页面大部分文本显示为英文。

## 受影响范围

- **Usage 页面** - 大量英文文本未翻译
- **Chat 页面** - 缺少 `toolCallsToggle` 翻译
- **通用组件** - 缺少 `theme` 翻译

## 环境信息

- OpenClaw 版本: 2026.3.23-1
- 浏览器: Chrome/Firefox
- 语言设置: 简体中文 (zh-CN)

## 建议的翻译内容

### 1. Usage 页面完整翻译

已准备完整的 Usage 页面翻译，包含以下模块：

| 模块 | 键数 | 说明 |
|------|------|------|
| `usage.page` | 1 | 页面副标题 |
| `usage.common` | 2 | 通用显示文本 |
| `usage.loading` | 2 | 加载状态 |
| `usage.metrics` | 4 | 指标标签 |
| `usage.presets` | 3 | 预设时间范围 |
| `usage.filters` | 26 | 筛选器相关 |
| `usage.query` | 5 | 查询输入 |
| `usage.export` | 4 | 导出功能 |
| `usage.empty` | 6 | 空状态提示 |
| `usage.daily` | 5 | 每日统计 |
| `usage.breakdown` | 7 | 数据分解 |
| `usage.overview` | 42 | 概览卡片 |
| `usage.sessions` | 17 | 会话列表 |
| `usage.details` | 33 | 详情面板 |
| `usage.mosaic` | 16 | 活动时间热力图 |

**总计: 约 170+ 个翻译键**

### 2. 其他补充

```typescript
// Chat 页面
chat.toolCallsToggle: `切换工具调用和工具结果`

// 通用
common.theme: `主题`

// Tabs 优化
tabs.appearance: `外观`  // 简化为更简洁的表达
```

## 翻译原则

1. **技术术语保留**: WebSocket、Tailscale、Cron、Webhook、JSON、CSV 等保持英文
2. **简洁性**: 按钮和标签尽量简短，符合中文 UI 习惯
3. **一致性**: 与现有翻译风格保持一致（如 "令牌"、"会话"、"代理" 等）
4. **占位符保留**: `{count}`、`{time}`、`{zone}`、`{shown}`、`{total}` 等变量保持不变

## 示例对比

### Before (英文)
```
Usage Overview
Tokens: 1.2M
Cost: $0.45
Sessions: 23
Filter sessions...
Export
```

### After (中文)
```
使用概览
令牌: 1.2M
成本: $0.45
会话: 23
筛选会话...
导出
```

## 附件

- [zh-CN-translation-patch.ts](附件文件) - 包含完整翻译的 TypeScript 代码片段
- [translation-issue.md](详细说明) - 详细翻译说明文档

## 建议操作

1. 将附件中的翻译合并到 `packages/control-ui/src/i18n/zh-CN.ts`
2. 运行 `npm run build` 确保编译通过
3. 在本地测试验证
4. 提交 PR

## 参考

- 英文原文: `packages/control-ui/src/i18n/en.ts` 或主文件中的 `T` 对象
- 现有中文翻译: `packages/control-ui/src/i18n/zh-CN.ts`
- 相关 PR: (待创建)

---

**提交者**: OpenClaw 中文用户  
**日期**: 2026-03-24  
**版本**: 2026.3.23-1
