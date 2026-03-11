# 浏览器自动化工具

使用 `mcporter` + `chrome-devtools-mcp` 进行网页浏览和自动化操作。

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `browser_automation.py` | 核心工具类，封装了所有浏览器操作 |
| `example_usage.py` | 使用示例和演示脚本 |
| `README.md` | 本文档 |

## 🔧 前置要求

1. **已安装 mcporter**
   ```bash
   npm install -g mcporter
   ```

2. **已配置 chrome-devtools-mcp**
   ```bash
   # 配置文件位置: ~/.config/mcporter/mcporter.json
   {
     "mcpServers": {
       "chrome-devtools": {
         "command": "npx",
         "args": ["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"]
       }
     }
   }
   ```

3. **Python 3.7+**

## 🚀 快速开始

### 1. 导入工具

```python
import sys
sys.path.insert(0, '/home/lcc/.openclaw/共享工作档案/code程序文档')

from browser_automation import create_browser
```

### 2. 创建浏览器实例

```python
browser = create_browser()
```

### 3. 基本操作

```python
# 导航到网页
browser.navigate("https://www.example.com")

# 获取页面快照
browser.get_snapshot()

# 截图
browser.screenshot("/tmp/screenshot.png", full_page=True)

# 执行 JavaScript
result = browser.execute_script("() => document.title")
```

## 📖 API 文档

### 导航操作

| 方法 | 说明 | 示例 |
|------|------|------|
| `navigate(url)` | 导航到 URL | `browser.navigate("https://www.meituan.com")` |
| `reload()` | 刷新页面 | `browser.reload()` |
| `go_back()` | 返回上一页 | `browser.go_back()` |
| `go_forward()` | 前进 | `browser.go_forward()` |

### 页面信息

| 方法 | 说明 | 示例 |
|------|------|------|
| `get_snapshot()` | 获取页面结构 | `browser.get_snapshot()` |
| `get_page_info()` | 获取页面信息 | `browser.get_page_info()` |
| `find_element_by_text(text)` | 按文本查找元素 | `browser.find_element_by_text("搜索")` |
| `find_elements_by_type(type)` | 按类型查找元素 | `browser.find_elements_by_type("link")` |

### 元素操作

| 方法 | 说明 | 示例 |
|------|------|------|
| `click(uid)` | 点击元素 | `browser.click("1_42")` |
| `fill(uid, value)` | 填写表单 | `browser.fill("1_15", "昆明美食")` |
| `type_text(text, submit_key)` | 输入文本 | `browser.type_text("hello", "Enter")` |
| `press_key(key)` | 按键 | `browser.press_key("Enter")` |
| `hover(uid)` | 悬停 | `browser.hover("1_42")` |
| `wait_for(texts, timeout)` | 等待文本出现 | `browser.wait_for(["加载完成"], 5000)` |

### JavaScript 执行

| 方法 | 说明 | 示例 |
|------|------|------|
| `execute_script(script, args)` | 执行 JS | `browser.execute_script("() => document.title")` |

### 截图

| 方法 | 说明 | 示例 |
|------|------|------|
| `screenshot(path, full_page)` | 截图 | `browser.screenshot("/tmp/img.png", True)` |

### 设备模拟

| 方法 | 说明 | 示例 |
|------|------|------|
| `emulate_device(w, h)` | 自定义尺寸 | `browser.emulate_device(375, 667)` |
| `emulate_mobile()` | 模拟手机 | `browser.emulate_mobile()` |
| `emulate_tablet()` | 模拟平板 | `browser.emulate_tablet()` |
| `emulate_desktop()` | 模拟桌面 | `browser.emulate_desktop()` |

### 性能分析

| 方法 | 说明 | 示例 |
|------|------|------|
| `start_performance_trace()` | 开始性能追踪 | `browser.start_performance_trace()` |
| `stop_performance_trace()` | 停止性能追踪 | `browser.stop_performance_trace()` |
| `lighthouse_audit()` | Lighthouse 审计 | `browser.lighthouse_audit()` |

### 网络监控

| 方法 | 说明 | 示例 |
|------|------|------|
| `list_network_requests()` | 列出网络请求 | `browser.list_network_requests()` |
| `list_console_messages()` | 列出控制台日志 | `browser.list_console_messages()` |

## 💡 使用示例

### 示例 1: 基本网页浏览

```python
from browser_automation import create_browser

browser = create_browser()
browser.navigate("https://www.meituan.com")
browser.screenshot("/tmp/meituan.png", full_page=True)
```

### 示例 2: 搜索操作

```python
browser = create_browser()
browser.navigate("https://duckduckgo.com")

# 获取页面快照
browser.get_snapshot()

# 查找搜索框
textboxes = browser.find_elements_by_type("textbox")
if textboxes:
    search_uid = textboxes[0]['uid']
    browser.fill(search_uid, "Python programming")
    browser.press_key("Enter")
```

### 示例 3: 数据采集

```python
browser = create_browser()
browser.navigate("https://www.example.com")

# 使用 JavaScript 提取数据
data = browser.execute_script("""
    () => {
        const links = Array.from(document.querySelectorAll('a'));
        return links.map(a => ({
            text: a.textContent.trim(),
            href: a.href
        }));
    }
""")

import json
with open('data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)
```

### 示例 4: 设备模拟测试

```python
browser = create_browser()
browser.navigate("https://www.example.com")

# 桌面视图
browser.emulate_desktop()
browser.screenshot("/tmp/desktop.png")

# 手机视图
browser.emulate_mobile()
browser.screenshot("/tmp/mobile.png")
```

## 🎮 运行演示

```bash
cd /home/lcc/.openclaw/共享工作档案/code程序文档
python3 example_usage.py
```

演示菜单：
1. 基本导航
2. 页面快照
3. 表单交互
4. JavaScript 执行
5. 设备模拟
6. 网络监控
7. 数据采集框架
0. 运行所有演示

## ⚠️ 注意事项

1. **页面结构变化**: 网页结构可能会更新，需要根据实际页面调整选择器
2. **等待时间**: 网络加载需要时间，适当使用 `time.sleep()` 或 `wait_for()`
3. **元素 uid**: 每次页面刷新后 uid 会变化，需要重新获取快照
4. **反爬机制**: 部分网站有反爬机制，注意控制请求频率
5. **合法使用**: 遵守网站的 robots.txt 和服务条款

## 🔧 故障排除

### 问题: mcporter 命令未找到

**解决**: 确保 mcporter 已安装并在 PATH 中
```bash
npm install -g mcporter
which mcporter
```

### 问题: chrome-devtools 服务器未配置

**解决**: 检查配置文件
```bash
cat ~/.config/mcporter/mcporter.json
```

### 问题: 元素未找到

**解决**: 
1. 先调用 `get_snapshot()` 获取最新页面结构
2. 检查 uid 是否正确
3. 确认页面已完全加载

### 问题: 命令超时

**解决**: 
1. 增加等待时间
2. 检查网络连接
3. 确认目标网站可访问

## 📚 相关资源

- [mcporter 文档](http://mcporter.dev)
- [chrome-devtools-mcp GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [MCP 协议文档](https://modelcontextprotocol.io)

## 📝 更新日志

### 2026-03-11
- 初始版本发布
- 封装 mcporter + chrome-devtools-mcp 常用操作
- 提供 7 个使用示例
