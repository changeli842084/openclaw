# LEARNINGS

## 2026-04-07 | correction | 长时间无响应必须先回报阶段进展
- 用户反馈：`你又有87分钟没有响应了`
- 问题：在执行 Git/GitHub 网络诊断期间，没有及时向用户发送阶段性进展，导致长时间静默。
- 正确认知：即使任务仍在处理中，只要超过短时间没有可见回复，也应先向用户做一次简短状态同步，而不是等待所有诊断完全结束。
- 以后做法：
  1. 长于 30 秒的排查或执行，先发一句阶段性回报。
  2. 长于 2-5 分钟的任务，按阶段持续同步“已确认事实 / 下一步 / 是否需要继续”。
  3. 不把“还在查”当作不回复的理由。
- 分类：correction
- 触发来源：用户直接纠正
- Source: simplify-and-harden
- Pattern-Key: long-running-task-must-send-progress-update

## 2026-04-07 | best_practice | 诊断类任务先报事实再继续深挖
- 场景：GitHub push 间歇性失败、网络/TLS 诊断。
- 做法：优先快速给出已确认事实（远端、DNS、curl、ls-remote、dry-run push），再决定是否继续深挖代理/TLS/环境问题。
- 价值：即使后续诊断耗时较长，用户也能先获得可行动结论。
- 分类：best_practice
- Source: simplify-and-harden
- Pattern-Key: diagnose-report-facts-before-deep-dive
- **See Also**: `long-running-task-must-send-progress-update`

## 2026-04-07 | correction | 硬件诊断也必须阶段性回报，不能只做首轮探测
- 用户反馈：`你又卡住114分钟了`
- 问题：在 USB 无线网卡排查中，只完成了首轮只读探测，没有及时把“已识别设备 / 尚未确认驱动绑定”的阶段结果回报给用户。
- 正确认知：硬件/系统诊断同样属于长任务；即使还没拿到最终根因，也必须先同步当前已确认事实和下一步判断点。
- 以后做法：
  1. 首轮探测完成后立即回报：设备是否被识别、驱动是否加载、接口是否出现。
  2. 若需要进一步查看日志/驱动支持，先告诉用户目前最可能的方向。
  3. 心跳期间若存在这类未结项诊断，恢复正常对话后优先补发正式结论。
- 分类：correction
- 触发来源：用户直接纠正
- Source: simplify-and-harden
- Pattern-Key: hardware-diagnosis-must-report-intermediate-findings
- **See Also**: `long-running-task-must-send-progress-update`
