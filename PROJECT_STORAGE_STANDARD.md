# 项目文件存储规范

> 制定日期：2026-03-11  
> 适用范围：所有 Agent 协作项目

---

## 📁 存储架构

```
~/.openclaw/
│
├── workspace-manager/          # Manager 工作区（仅配置文件）
│   ├── AGENTS.md
│   ├── BOOTSTRAP.md
│   ├── HEARTBEAT.md
│   ├── IDENTITY.md
│   ├── MEMORY.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   └── USER.md
│
├── workspace-researcher/       # Researcher 工作区（仅配置文件）
│   └── ...（配置文件）
│
├── workspace-coder/            # Coder 工作区（仅配置文件）
│   └── ...（配置文件）
│
├── workspace-office/           # Office 工作区（仅配置文件）
│   └── ...（配置文件）
│
└── 共享工作档案/               # ⭐ 所有项目交付物存储在这里
    │
    ├── 截图/                   # 所有截图统一存放
    │
    ├── 原始数据文档/           # 原始数据文件
    │
    ├── office办公文档/         # Office 生成的文档
    │
    ├── tmp/                    # 临时文件
    │
    └── code程序文档/           # 代码项目存放
        │
        ├── browser-automation/     # 浏览器自动化项目
        │   ├── browser_automation.py
        │   ├── README.md
        │   └── ...
        │
        └── {project-name}/         # 其他项目按名称存放
            │
            ├── docs/               # Researcher 输出
            │   └── *.md
            │
            ├── src/ 或 根目录      # Coder 输出
            │   └── *.py
            │
            ├── output/             # Office 输出
            │   └── *.md / *.docx / *.xlsx
            │
            ├── data/               # 共享数据
            │   └── *.json / *.csv
            │
            └── config/             # 项目配置
                └── *.json
```

---

## 🎯 Agent 输出路径规范

### Researcher
- **输出目录**: `~/.openclaw/共享工作档案/{项目类型}/{项目名}/docs/`
- **文件格式**: `.md`, `.txt`, `.json`, `.csv`
- **示例**: `~/.openclaw/共享工作档案/code程序文档/travel-assistant/docs/research_report.md`

### Coder
- **输出目录**: `~/.openclaw/共享工作档案/{项目类型}/{项目名}/`
- **文件格式**: `.py`, `.js`, `.sh`
- **示例**: `~/.openclaw/共享工作档案/code程序文档/travel-assistant/price_monitor.py`

### Office
- **输出目录**: `~/.openclaw/共享工作档案/{项目类型}/{项目名}/output/`
- **文件格式**: `.docx`, `.xlsx`, `.pdf`, `.md`
- **示例**: `~/.openclaw/共享工作档案/code程序文档/travel-assistant/output/昆明旅行手册.md`

### Manager
- **不直接生成文件**
- **仅管理任务和协调**
- **项目报告保存到**: `~/.openclaw/共享工作档案/{项目类型}/{项目名}/output/`

---

## ⚠️ 禁止行为

1. **禁止在 workspace-* 目录保存项目文件**
   - ❌ `~/.openclaw/workspace-manager/*.py`
   - ❌ `~/.openclaw/workspace-coder/*.py`
   - ✅ `~/.openclaw/共享工作档案/code程序文档/{项目}/*.py`

2. **禁止分散存储**
   - ❌ 同一项目的文件保存在不同位置
   - ✅ 所有相关文件保存在项目目录内

3. **禁止临时文件残留**
   - ❌ 测试生成的 `_history.json` 等文件
   - ✅ 临时文件保存到 `tmp/` 或清理

---

## ✅ 最佳实践

### 1. 项目启动时创建目录结构
```bash
mkdir -p ~/.openclaw/共享工作档案/{类型}/{项目名}/{docs,src,output,data,config}
```

### 2. 使用绝对路径保存文件
```python
# ❌ 错误
save_path = "research_report.md"

# ✅ 正确
save_path = "/home/lcc/.openclaw/共享工作档案/code程序文档/travel-assistant/docs/research_report.md"
```

### 3. 文件命名规范
- 使用小写字母
- 使用连字符 `-` 或下划线 `_`
- 包含版本号或日期（可选）
- 示例：`research_report_v1.md`, `price_monitor.py`

### 4. 定期清理
- Manager 定期清理 workspace-manager 中的临时文件
- 项目完成后归档旧文件

---

## 🔧 工具函数

### 获取项目路径（Python）
```python
import os

def get_project_path(project_type: str, project_name: str, 
                     subdir: str = "", filename: str = "") -> str:
    """
    获取项目文件路径
    
    Args:
        project_type: 项目类型 (code程序文档/office办公文档/原始数据文档)
        project_name: 项目名称
        subdir: 子目录 (docs/src/output/data/config)
        filename: 文件名
    """
    base = f"/home/lcc/.openclaw/共享工作档案/{project_type}/{project_name}"
    if subdir:
        base = os.path.join(base, subdir)
    if filename:
        base = os.path.join(base, filename)
    return base

# 使用示例
research_path = get_project_path("code程序文档", "travel-assistant", "docs", "report.md")
code_path = get_project_path("code程序文档", "travel-assistant", "", "tool.py")
output_path = get_project_path("code程序文档", "travel-assistant", "output", "manual.md")
```

---

## 📊 当前项目整改清单

### 已发现问题
- [x] Manager workspace 中有临时文件（已清理）
- [x] 部分文件路径不规范

### 整改措施
1. ✅ 清理 Manager workspace 中的 .py 和 .json 文件
2. ✅ 确认所有项目文件在 travel-assistant/ 目录
3. ✅ 制定本存储规范
4. ⏸️ 通知所有 Agent 遵守规范

---

## 📝 更新日志

### 2026-03-11
- 制定初始版本
- 定义 Agent 输出路径规范
- 明确禁止行为和最佳实践
