# OpenClaw Agent 间通信配置指南

## 概述

OpenClaw 支持多个 Agent 之间的协作通信。本指南介绍如何启用和配置 Agent 间通信功能，让项目经理（manager）能够调用研究员（researcher）、办公专家（office）、程序员（coder）等团队成员。

## 当前状态检查

### 1. 查看当前 Agent 列表
```bash
openclaw agents list
```

输出示例：
```
Agents:
- manager (default)
  Identity: 👔 项目经理
  Workspace: ~/.openclaw/workspace-manager
- researcher
  Identity: 🔍 研究员
  Workspace: ~/.openclaw/workspace-researcher
- office
  Identity: 📊 办公专家
  Workspace: ~/.openclaw/workspace-office
- coder
  Identity: 💻 程序员
  Workspace: ~/.openclaw/workspace-coder
```

### 2. 检查当前会话状态
```bash
openclaw sessions list
```

## 启用 Agent 间通信

### 方法一：修改配置文件（推荐）

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true
    },
    "profile": "full",
    "sessions": {
      "visibility": "all"
    }
  }
}
```

### 方法二：使用命令行配置

```bash
# 启用 Agent 间通信
openclaw config set tools.agentToAgent.enabled true

# 验证配置
openclaw config get tools.agentToAgent.enabled
```

### 方法三：完整配置示例

在 `~/.openclaw/openclaw.json` 中添加以下配置：

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allowlist": ["researcher", "office", "coder"],
      "denylist": []
    },
    "sessions": {
      "visibility": "all",
      "allowCrossSessionMessaging": true
    }
  }
}
```

配置说明：
- `enabled`: 启用 Agent 间通信
- `allowlist`: 允许通信的 Agent 列表（可选，为空则允许所有）
- `denylist`: 禁止通信的 Agent 列表（可选）
- `visibility`: 会话可见性设置
- `allowCrossSessionMessaging`: 允许跨会话消息

## 重启 Gateway

修改配置后需要重启 Gateway 使配置生效：

```bash
# 方法 1：使用 openclaw 命令
openclaw gateway restart

# 方法 2：使用 systemctl
sudo systemctl restart openclaw-gateway

# 方法 3：手动重启
openclaw gateway stop
openclaw gateway start
```

## 验证配置

### 1. 检查配置是否生效
```bash
openclaw config get tools.agentToAgent
```

### 2. 测试 Agent 间通信

启动 manager 会话，尝试向 researcher 发送消息：

```bash
# 在 manager 会话中执行
openclaw sessions send --agent researcher "测试消息"
```

或者使用 sessionKey：
```bash
openclaw sessions send --session-key agent:researcher:main "测试消息"
```

## 使用方式

### 方式一：直接发送消息

```bash
# 向 researcher 发送任务
openclaw sessions send \
  --session-key agent:researcher:main \
  "请搜索最新的 AI 大模型进展"
```

### 方式二：Spawn 子 Agent

```bash
# 启动 researcher 执行特定任务
openclaw sessions spawn \
  --agent researcher \
  --task "搜索 OpenAI 最新动态" \
  --mode run
```

### 方式三：使用工具调用（在 Agent 代码中）

在 manager 的代码中使用：

```javascript
// 向 researcher 发送消息
await sessions_send({
  sessionKey: "agent:researcher:main",
  message: "请执行调研任务",
  timeoutSeconds: 60
});
```

## 故障排查

### 问题 1：Agent-to-agent messaging is disabled

**原因**：Agent 间通信未启用

**解决**：
```bash
openclaw config set tools.agentToAgent.enabled true
openclaw gateway restart
```

### 问题 2：agentId is not allowed for sessions_spawn

**原因**：当前配置不允许 spawn 指定的 agent

**解决**：
1. 检查 `tools.sessions.spawnAllowedAgents` 配置
2. 或设置为允许所有：
```json
{
  "tools": {
    "sessions": {
      "spawnAllowedAgents": ["*"]
    }
  }
}
```

### 问题 3：Session not found

**原因**：目标 Agent 没有活跃的会话

**解决**：
```bash
# 先启动目标 Agent 的会话
openclaw sessions spawn --agent researcher --mode session
```

## 最佳实践

### 1. 团队工作流设计

```
项目经理 (manager)
    ├── 调用研究员 (researcher) - 信息收集
    ├── 调用办公专家 (office) - 文档处理
    └── 调用程序员 (coder) - 代码开发
```

### 2. 任务分配模式

**模式 A：直接指派**
```
Manager → Researcher: "搜索 XXX 信息"
Researcher → Manager: 返回结果
```

**模式 B：流水线协作**
```
Manager → Researcher: 收集信息
Researcher → Office: 生成报告
Office → Manager: 提交最终文档
```

### 3. 会话管理建议

- 长期任务：使用 `mode: session` 保持会话活跃
- 一次性任务：使用 `mode: run` 执行后自动清理
- 定时任务：使用 `cron` 配置周期性执行

## 安全注意事项

1. **权限控制**：使用 `allowlist` 限制可通信的 Agent
2. **消息审核**：敏感操作建议添加人工确认
3. **日志记录**：启用 `command-logger` 记录所有通信

```json
{
  "hooks": {
    "internal": {
      "command-logger": {
        "enabled": true
      }
    }
  }
}
```

## 参考文档

- [OpenClaw Agents 文档](https://docs.openclaw.ai/cli/agents)
- [OpenClaw Sessions 文档](https://docs.openclaw.ai/cli/sessions)
- [OpenClaw Config 文档](https://docs.openclaw.ai/cli/config)

---

**文档版本**：1.0  
**创建时间**：2026-03-10  
**适用版本**：OpenClaw 2026.3.7+
