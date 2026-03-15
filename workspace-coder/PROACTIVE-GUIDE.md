# Proactive-Agent 使用指南 - Coder

## 核心协议速查

### 1. WAL Protocol（先写后回）

**触发条件：**
- ✏️ 修正：代码修改、逻辑调整、Bug修复
- 📍 专有名词：库名、框架名、API名称
- 🎨 偏好：代码风格、命名规范、注释习惯
- 📋 决策："用X方案" / "选Y架构"
- 🔢 具体数值：版本号、端口号、配置参数

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
## 2026-03-15 17:10 技术决策
- 项目：数据处理脚本
- 语言：Python 3.10
- 库：pandas, numpy
- 决策：使用面向对象方式编写
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
写个Python脚本处理Excel数据

## 2026-03-15 17:15 Agent
已创建脚本框架，包含数据读取、清洗、导出功能，使用pandas
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

**绝对路径：** `/home/lcc/.openclaw/workspace-coder/`

**关键文件：**
- `SESSION-STATE.md` - 活跃任务状态
- `memory/working-buffer.md` - 危险区日志
- `SOUL.md` - 行事原则
- `MEMORY.md` - 长期记忆
