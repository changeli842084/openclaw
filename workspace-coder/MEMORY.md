# MEMORY.md - 程序员的长期记忆库

## 用户偏好
- 输出路径：`/home/lcc/.openclaw/共享工作档案/code程序文档/`
- 代码风格：
  - Python：遵循 PEP 8，使用 4 空格缩进。
  - JavaScript：使用 2 空格缩进，语句末尾加分号。
- 文档要求：每个项目必须包含 README.md，说明用途、安装方法、使用示例。
- 测试要求：关键函数必须有单元测试，测试覆盖率建议 >80%。

## 常用技术栈记录
- 数据处理：Python + pandas + numpy
- Web 开发：Node.js + Express 或 Flask
- 自动化脚本：Bash 或 Python
- 数据库：SQLite、MySQL（需用户提供连接信息）

## 重要决策
- 2026-03-11：确定所有项目必须包含依赖文件，便于复现环境。
- 2026-03-11：测试通过的标准是全部单元测试通过，且无严重 bug。

## 工具配置状态
- Python 3.10+ 已安装，pip 可用。
- Node.js 18+ 已安装，npm 可用。
- Git 已安装，但需用户授权使用。
- 代码编辑器（VS Code）已安装，但通常通过命令行调用。

## 技能目录规则（重要）
根据 OpenClaw 官方设计，技能加载优先级如下：
1. **`<workspace>/skills` (最高优先级)** - 本 Agent 专属技能目录
2. **`~/.openclaw/skills` (中等优先级)** - 公共共享技能（所有Agent共用）
3. **Bundled skills (最低优先级)** - 系统自带技能

### 本 Agent 技能路径
- **专属技能**: `~/.openclaw/workspace-coder/skills/` - 仅 coder 可用
- **公共技能**: `~/.openclaw/skills/` - 所有Agent共享

### 规则说明
- 专属技能放在自己的 `workspace/skills/` 目录下，其他Agent无法访问
- 公共技能统一放在 `~/.openclaw/skills/`，只安装一次，所有Agent共享
- 同名技能优先使用自己 workspace 中的版本
