# Proactive-Agent 使用指南 - Researcher

## 核心协议速查

### 1. WAL Protocol（先写后回）

**触发条件：**
- ✏️ 修正："是X，不是Y" / "实际上..." / "不对"
- 📍 专有名词：人名、地名、公司名、产品名
- 🎨 偏好："我喜欢..." / "用...风格"
- 📋 决策："我们用X方案" / "选Y"
- 🔢 具体数值：日期、金额、数量、ID、URL

**执行步骤：**
```
1. 识别关键信息
2. 打开 SESSION-STATE.md
3. 写入关键信息（带时间戳）
4. 保存文件
5. 回复用户
```

**示例：**
```markdown
## 2026-03-15 17:10 关键决策
- 主题：AI行业调研
- 决策：优先搜索中文资料
- 来源：用户明确要求
```

---

### 2. Working Buffer（危险区保护）

**触发条件：**
- 上下文使用率 > 60%

**执行步骤：**
```
1. 检查上下文使用率
2. 超过60% → 打开 memory/working-buffer.md
3. 每轮对话后追加记录
4. 格式：时间戳 + 用户消息摘要 + 我的回复摘要
```

**示例：**
```markdown
## 2026-03-15 17:15 Human
搜索最新AI新闻

## 2026-03-15 17:15 Agent
使用tavily搜索，找到10条相关新闻，已整理成列表
```

---

### 3. Compaction Recovery（压缩恢复）

**触发条件：**
- 新会话开始
- 检测到上下文被截断
- 用户问"我们刚才在说什么？"

**执行步骤：**
```
1. 读取 SESSION-STATE.md → 了解当前任务
2. 读取 memory/working-buffer.md → 了解最近对话
3. 整合信息，向用户确认
4. 继续任务
```

---

## 会话启动检查清单

每次会话开始时必须执行：

- [ ] 读取 SOUL.md（我的身份和原则）
- [ ] 读取 MEMORY.md（长期记忆）
- [ ] 读取 SESSION-STATE.md（当前任务状态）
- [ ] 检查 memory/working-buffer.md（危险区日志）

---

## 我的工作区

**绝对路径：** `/home/lcc/.openclaw/workspace-researcher/`

**关键文件：**
- `SESSION-STATE.md` - 活跃任务状态
- `memory/working-buffer.md` - 危险区日志
- `SOUL.md` - 行事原则
- `MEMORY.md` - 长期记忆
