# 项目经理工具说明

## 📂 工具定义文件位置

我的工具定义文件存放在：

~/.openclaw/workspace-manager/tools/
text


这里有三个 JSON 文件，每个文件定义了一个“函数”，供我在需要时调用。

## 🛠️ 工具与技能的区别

| 类型 | 存放位置 | 作用 | 示例 |
|------|----------|------|------|
| **工具定义** | `tools/` | 告诉 AI 有哪些函数可用 | `research_task.json` |
| **技能实现** | `skills/` | 实际执行功能的代码 | browser-control 技能 |

## 🔧 我定义的三个工具

### 1. research_task —— 调用研究员

**文件位置**：`~/workspace-manager/tools/research_task.json`

**文件内容**：
```json
{
  "name": "research_task",
  "description": "调用研究员执行网络资料抓取或监控任务",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "详细描述研究员需要做什么，包括网址、关键词、监控频率等"
      }
    },
    "required": ["query"]
  },
  "command": "openclaw agents run researcher \"{{query}}\" --response-format text"
}

作用：当需要网络信息时，我用这个工具把任务派给 researcher。
2. office_task —— 调用办公专家

文件位置：~/workspace-manager/tools/office_task.json

文件内容：
json

{
  "name": "office_task",
  "description": "调用办公专家处理文档、表格、PPT等办公任务",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "详细描述办公专家需要做什么，例如生成报告、分析表格、制作PPT等"
      }
    },
    "required": ["query"]
  },
  "command": "openclaw agents run office \"{{query}}\" --response-format text"
}

作用：当需要文档处理时，我用这个工具把任务派给 office。
3. code_task —— 调用程序员

文件位置：~/workspace-manager/tools/code_task.json

文件内容：
json

{
  "name": "code_task",
  "description": "调用程序员编写代码或开发工具",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "详细描述程序员需要做什么，包括编程语言、功能需求、输入输出示例等"
      }
    },
    "required": ["query"]
  },
  "command": "openclaw agents run coder \"{{query}}\" --response-format text"
}

作用：当需要编写代码时，我用这个工具把任务派给 coder。
🔐 为什么我能执行这些命令？

因为我启用了 coding profile，在 ~/.openclaw/openclaw.json 中配置了：
json

{
  "id": "manager",
  "tools": {
    "profile": "coding"
  }
}

coding profile 赋予了我以下权限：

    ✅ exec：执行 shell 命令（这是调用子 Agent 的关键）

    ✅ read/write：读写文件

    ✅ 会话管理能力

    ✅ 记忆访问能力

⚠️ 使用注意事项

    命令路径：openclaw 命令必须在 PATH 中，否则需要在 command 中使用绝对路径（如 /home/lcc/.npm-global/bin/openclaw）

    参数传递：{{query}} 会被实际传入的 query 参数替换

    返回格式：--response-format text 确保返回纯文本，便于我阅读

    失败处理：

        如果子 Agent 调用失败，我会重试最多 3 次

        连续失败会记录到 MEMORY.md

📌 验证工具是否生效

执行以下命令测试：
bash

# 测试调用 coder
openclaw agents run manager "让程序员写一个打印 Hello World 的 Python 脚本"

如果能看到 coder 返回代码，说明工具调用正常。
text


**复制时请注意**：要包括开头的 `# 项目经理工具说明` 和结尾的三个反引号（\`\`\`），确保格式完整。

---

## ⚠️ 同时别忘了创建真正的工具定义文件

`TOOLS.md` 只是说明书，真正让项目经理能调用子 Agent 的是 `tools/` 目录下的三个 **JSON 文件**。如果你还没创建，请务必执行：

```bash
mkdir -p ~/.openclaw/workspace-manager/tools

# 创建 research_task.json
cat > ~/.openclaw/workspace-manager/tools/research_task.json << 'EOF'
{
  "name": "research_task",
  "description": "调用研究员执行网络资料抓取或监控任务",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "详细描述研究员需要做什么，包括网址、关键词、监控要求等"
      }
    },
    "required": ["query"]
  },
  "command": "openclaw agents run researcher \"{{query}}\" --response-format text"
}
EOF

# 类似地创建另外两个文件（可参考之前命令）
