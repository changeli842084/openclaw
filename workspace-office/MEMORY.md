# MEMORY.md - 办公专家的长期记忆库

## 我的工作区路径（必须记住）
**我的工作区**: `/home/lcc/.openclaw/workspace-office/`

这是我在系统中的家目录，所有我的文件、配置、记忆都存储在这里。

## 用户偏好
- 输出文件路径：`/home/lcc/.openclaw/共享工作档案/office办公文档/`
- 文件命名格式：`YYYY-MM-DD_描述.扩展名`
- 文档风格：喜欢简洁明了，图表用蓝色系，PPT 使用公司模板（若有）。
- 数据分析偏好：喜欢看到同比、环比趋势，以及异常值标注。

## 常用模板记录
- Word 报告模板：位于 `/home/lcc/.openclaw/templates/report_template.docx`
- PPT 模板：位于 `/home/lcc/.openclaw/templates/presentation_template.pptx`
- Excel 分析模板：位于 `/home/lcc/.openclaw/templates/analysis_template.xlsx`

## 重要决策
- 2026-03-11：确定数据分析前必须先检查数据完整性，缺失值需标注。
- 2026-03-11：所有图表必须添加标题和轴标签。

## 工具配置状态
- `python-docx`、`openpyxl`、`python-pptx`、`pandas`、`matplotlib`、`moviepy` 等库已安装。
- 字体文件：确保中文字体（如"微软雅黑"）可用。

## 技能目录规则（重要）
根据 OpenClaw 官方设计，技能加载优先级如下：
1. **`<workspace>/skills` (最高优先级)** - 本 Agent 专属技能目录
2. **`~/.openclaw/skills` (中等优先级)** - 公共共享技能（所有Agent共用）
3. **Bundled skills (最低优先级)** - 系统自带技能

### 本 Agent 技能路径
- **专属技能**: `~/.openclaw/workspace-office/skills/` - 仅 office 可用
- **公共技能**: `~/.openclaw/skills/` - 所有Agent共享

### 规则说明
- 专属技能放在自己的 `workspace/skills/` 目录下，其他Agent无法访问
- 公共技能统一放在 `~/.openclaw/skills/`，只安装一次，所有Agent共享
- 同名技能优先使用自己 workspace 中的版本
