# OpenClaw Control UI 中文翻译补充建议

## 问题描述
当前 `zh-CN` 语言文件存在部分翻译缺失，导致 Web UI 中部分页面显示英文。

## 受影响页面
1. **Usage (使用情况)** - 大量英文文本
2. **Agents (代理)** - 部分英文文本  
3. **通用 UI 组件** - 少量英文文本

## 建议补充的翻译

### 1. Usage 页面补充

```typescript
usage: {
  page: {
    subtitle: `查看令牌使用情况、会话峰值和成本驱动因素。`
  },
  common: {
    emptyValue: `—`,
    unknown: `未知`
  },
  loading: {
    title: `使用情况概览`,
    badge: `加载中`
  },
  metrics: {
    tokens: `令牌`,
    cost: `成本`,
    session: `会话`,
    sessions: `会话`
  },
  presets: {
    today: `今天`,
    last7d: `7天`,
    last30d: `30天`
  },
  filters: {
    title: `筛选`,
    to: `至`,
    startDate: `开始日期`,
    endDate: `结束日期`,
    timeZone: `时区`,
    timeZoneLocal: `本地`,
    timeZoneUtc: `UTC`,
    pin: `固定`,
    pinned: `已固定`,
    unpin: `取消固定`,
    selectAll: `全选`,
    clear: `清除`,
    clearAll: `全部清除`,
    remove: `移除筛选`,
    all: `全部`,
    days: `天`,
    hours: `小时`,
    session: `会话`,
    agent: `代理`,
    channel: `频道`,
    provider: `提供商`,
    model: `模型`,
    tool: `工具`,
    daysCount: `{count} 天`,
    hoursCount: `{count} 小时`,
    sessionsCount: `{count} 个会话`
  },
  query: {
    placeholder: `筛选会话 (例如 key:agent:main:cron* model:gpt-4o has:errors minTokens:2000)`,
    apply: `筛选 (客户端)`,
    matching: `{shown} / {total} 个会话匹配`,
    inRange: `范围内共 {total} 个会话`,
    tip: `提示：使用筛选或点击柱状图来缩小日期范围。`
  },
  export: {
    label: `导出`,
    sessionsCsv: `会话 CSV`,
    dailyCsv: `每日 CSV`,
    json: `JSON`
  },
  empty: {
    title: `选择日期范围`,
    subtitle: `加载使用数据以比较成本、检查会话和深入时间线，无需离开仪表板。`,
    hint: `选择日期范围并点击刷新以加载使用数据。`,
    noData: `无数据`,
    featureOverview: `概览卡片`,
    featureSessions: `会话排名`,
    featureTimeline: `时间线深入`
  },
  daily: {
    title: `每日使用`,
    total: `总计`,
    byType: `按类型`,
    tokensTitle: `每日令牌使用`,
    costTitle: `每日成本`
  },
  breakdown: {
    output: `输出`,
    input: `输入`,
    cacheWrite: `缓存写入`,
    cacheRead: `缓存读取`,
    total: `总计`,
    tokensByType: `按类型令牌`,
    costByType: `按类型成本`
  },
  overview: {
    title: `使用概览`,
    messages: `消息`,
    messagesHint: `范围内的用户和助手消息总数。`,
    messagesAbbrev: `消息`,
    user: `用户`,
    assistant: `助手`,
    toolCalls: `工具调用`,
    toolCallsHint: `跨会话的工具调用总数。`,
    toolsUsed: `个工具`,
    errors: `错误`,
    errorsHint: `范围内的消息和工具错误总数。`,
    toolResults: `个工具结果`,
    avgTokens: `平均令牌/消息`,
    avgTokensHint: `此范围内每条消息的平均令牌数。`,
    avgCost: `平均成本/消息`,
    avgCostHint: `提供商报告成本时每条消息的平均成本。`,
    avgCostHintMissing: `提供商报告成本时每条消息的平均成本。此范围内部分或全部会话缺少成本数据。`,
    acrossMessages: `共 {count} 条消息`,
    sessions: `会话`,
    sessionsHint: `范围内的不同会话数。`,
    sessionsInRange: `范围内共 {count} 个`,
    throughput: `吞吐量`,
    throughputHint: `吞吐量显示活跃时间内每分钟令牌数。越高越好。`,
    tokensPerMinute: `令牌/分钟`,
    perMinute: `/分钟`,
    errorRate: `错误率`,
    errorHint: `错误率 = 错误 / 总消息数。越低越好。`,
    avgSession: `平均会话`,
    cacheHitRate: `缓存命中率`,
    cacheHint: `缓存命中率 = 缓存读取 / (输入 + 缓存读取)。越高越好。`,
    cached: `已缓存`,
    prompt: `提示`,
    calls: `调用`,
    topModels: `热门模型`,
    topProviders: `热门提供商`,
    topTools: `热门工具`,
    topAgents: `热门代理`,
    topChannels: `热门频道`,
    peakErrorDays: `错误高峰日`,
    peakErrorHours: `错误高峰时段`,
    noModelData: `无模型数据`,
    noProviderData: `无提供商数据`,
    noToolCalls: `无工具调用`,
    noAgentData: `无代理数据`,
    noChannelData: `无频道数据`,
    noErrorData: `无错误数据`
  },
  sessions: {
    title: `会话`,
    shown: `显示 {count} 个`,
    total: `共 {count} 个`,
    avg: `平均`,
    all: `全部`,
    recent: `最近查看`,
    recentShort: `最近`,
    sort: `排序`,
    ascending: `升序`,
    descending: `降序`,
    clearSelection: `清除选择`,
    noRecent: `无最近会话`,
    noneInRange: `范围内无会话`,
    more: `+{count} 更多`,
    selected: `已选择 ({count})`,
    copy: `复制`,
    copyName: `复制会话名称`,
    limitReached: `仅显示前 1,000 个会话。缩小日期范围以获取完整结果。`
  },
  details: {
    noUsageData: `此会话无使用数据。`,
    duration: `持续时间`,
    modelMix: `模型混合`,
    filtered: `(已筛选)`,
    close: `关闭会话详情`,
    noTimeline: `无时间线数据`,
    noDataInRange: `范围内无数据`,
    usageOverTime: `时间使用趋势`,
    reset: `重置`,
    perTurn: `每轮`,
    cumulative: `累计`,
    turnRange: `第 {start}–{end} 轮，共 {total} 轮`,
    assistantOutputTokens: `助手输出令牌`,
    userToolInputTokens: `用户+工具输入令牌`,
    tokensWrittenToCache: `写入缓存的令牌`,
    tokensReadFromCache: `从缓存读取的令牌`,
    noContextData: `无上下文数据`,
    systemPromptBreakdown: `系统提示分解`,
    collapse: `折叠`,
    collapseAll: `全部折叠`,
    expandAll: `全部展开`,
    baseContextPerMessage: `每条消息基础上下文`,
    system: `系统`,
    systemShort: `系统`,
    skills: `技能`,
    tools: `工具`,
    files: `文件`,
    ofInput: `输入的`,
    of: `的`,
    timelineFiltered: `时间线已筛选`,
    conversation: `对话`,
    noMessages: `无消息`,
    tool: `工具`,
    toolResult: `工具结果`,
    hasTools: `有工具`,
    searchConversation: `搜索对话`,
    you: `您`,
    noMessagesMatch: `无匹配消息。`
  },
  mosaic: {
    title: `活动时间`,
    subtitleEmpty: `估算需要会话时间戳。`,
    subtitle: `从会话跨度估算 (首次/末次活动)。时区：{zone}。`,
    noTimelineData: `尚无时间线数据。`,
    dayOfWeek: `星期`,
    midnight: `午夜`,
    fourAm: `凌晨4点`,
    eightAm: `上午8点`,
    noon: `中午`,
    fourPm: `下午4点`,
    eightPm: `晚上8点`,
    legend: `低 → 高令牌密度`,
    sun: `周日`,
    mon: `周一`,
    tue: `周二`,
    wed: `周三`,
    thu: `周四`,
    fri: `周五`,
    sat: `周六`
  }
}
```

### 2. 通用组件补充

```typescript
common: {
  // 已有翻译...
  theme: `主题`  // 新增
}

nav: {
  // 已有翻译...
}

tabs: {
  // 修改
  appearance: `外观`  // 原为 "外观与设置"
}
```

### 3. Chat 页面补充

```typescript
chat: {
  // 已有翻译...
  toolCallsToggle: `切换工具调用和工具结果`  // 新增
}
```

## 翻译原则

1. **保留技术术语**：WebSocket、Tailscale、Cron、Webhook 等保持英文
2. **保持简洁**：按钮和标签尽量简短
3. **一致性**：与现有翻译风格保持一致
4. **占位符保留**：如 `{count}`、`{time}`、`{zone}` 等变量保持不变

## 建议操作

1. 在 `packages/control-ui/src/i18n/zh-CN.ts` 中添加上述翻译
2. 运行测试确保无语法错误
3. 提交 PR 到主仓库

## 参考

- 当前语言文件路径：`packages/control-ui/src/i18n/zh-CN.ts`
- 英文原文参考：`packages/control-ui/src/i18n/en.ts` 或主文件中的 `T` 对象

---

**提交者**：OpenClaw 用户
**日期**：2026-03-24
**版本**：2026.3.23-1
