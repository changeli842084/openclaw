# 公共技能目录

## 说明

此目录 (`~/.openclaw/skills/`) 存放**所有 Agent 共享的公共技能**。

## 技能加载优先级

根据 OpenClaw 官方设计，技能加载优先级如下：

1. **`<workspace>/skills` (最高优先级)** - Agent 专属技能目录
   - `~/.openclaw/workspace-manager/skills/` - manager 专属
   - `~/.openclaw/workspace-coder/skills/` - coder 专属
   - `~/.openclaw/workspace-researcher/skills/` - researcher 专属
   - `~/.openclaw/workspace-office/skills/` - office 专属

2. **`~/.openclaw/skills` (中等优先级)** - 公共共享技能（本目录）

3. **Bundled skills (最低优先级)** - 系统自带技能

## 规则

- **公共技能**：放在本目录，所有 Agent 共享使用，只需安装一次
- **专属技能**：放在对应 Agent 的 `workspace/skills/` 目录下，仅该 Agent 可用
- **优先级**：同名技能优先使用 Agent 自己 workspace 中的版本

## 当前公共技能

（在此列出已安装的公共技能）
