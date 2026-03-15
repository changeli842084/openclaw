# MEMORY.md - 情报研究员的长期记忆库

## 用户偏好
- 输出文件路径：`/home/lcc/.openclaw/共享工作档案/原始数据文档/`
- 文件命名格式：`YYYY-MM-DD_关键词.md`
- 喜欢在报告中看到数据来源和收集时间。

## 常用搜索关键词记录
- 用户常查询的主题：行业动态、竞品信息、技术趋势。
- 特殊网站偏好：小红书（生活类）、抖音（短视频趋势）、知乎（深度问答）。

## 重要决策
- 2026-03-11：确定普通收集优先顺序为 `tavily` → `multi-search-engine`，结果合并后去重。
- 2026-03-11：特别收集如需登录，必须先经 manager 与用户沟通，收到凭证后才可使用。

## 工具配置状态
- `tavily` API Key 已配置（环境变量）。
- `multi-search-engine` 配置正常。
- `mcporter` + `chrome-devtools-mcp` 工具组已安装，但需确认浏览器驱动正常。

## 技能目录规则（重要）
根据 OpenClaw 官方设计，技能加载优先级如下：
1. **`<workspace>/skills` (最高优先级)** - 本 Agent 专属技能目录
2. **`~/.openclaw/skills` (中等优先级)** - 公共共享技能（所有Agent共用）
3. **Bundled skills (最低优先级)** - 系统自带技能

### 本 Agent 技能路径
- **专属技能**: `~/.openclaw/workspace-researcher/skills/` - 仅 researcher 可用
- **公共技能**: `~/.openclaw/skills/` - 所有Agent共享

### 规则说明
- 专属技能放在自己的 `workspace/skills/` 目录下，其他Agent无法访问
- 公共技能统一放在 `~/.openclaw/skills/`，只安装一次，所有Agent共享
- 同名技能优先使用自己 workspace 中的版本
