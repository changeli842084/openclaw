#!/usr/bin/env python3
"""
Agent 配置更新脚本

更新所有 Agent 的配置文件，确保他们使用正确的存储路径
"""

import os
import json

# 项目根目录
PROJECT_ROOT = "/home/lcc/.openclaw/共享工作档案/code程序文档/travel-assistant"

# 各 Agent 工作区
AGENT_WORKSPACES = {
    "manager": "/home/lcc/.openclaw/workspace-manager",
    "researcher": "/home/lcc/.openclaw/workspace-researcher",
    "coder": "/home/lcc/.openclaw/workspace-coder",
    "office": "/home/lcc/.openclaw/workspace-office"
}

# 存储规范
STORAGE_CONFIG = {
    "base_directory": "/home/lcc/.openclaw/共享工作档案",
    "project_types": {
        "code": "code程序文档",
        "office": "office办公文档",
        "data": "原始数据文档"
    },
    "agents": {
        "researcher": {
            "output_dir": "docs",
            "formats": [".md", ".txt", ".json", ".csv"],
            "description": "调研报告和数据收集"
        },
        "coder": {
            "output_dir": "",
            "formats": [".py", ".js", ".sh", ".json"],
            "description": "代码和工具开发"
        },
        "office": {
            "output_dir": "output",
            "formats": [".docx", ".xlsx", ".pdf", ".md"],
            "description": "文档和表格制作"
        },
        "manager": {
            "output_dir": "output",
            "formats": [".md", ".json"],
            "description": "项目管理和报告"
        }
    }
}


def get_output_path(agent: str, project_type: str, project_name: str, 
                    filename: str = "") -> str:
    """
    获取 Agent 的输出路径
    
    Args:
        agent: Agent 类型 (researcher/coder/office/manager)
        project_type: 项目类型 (code/office/data)
        project_name: 项目名称
        filename: 文件名（可选）
    """
    type_dir = STORAGE_CONFIG["project_types"].get(project_type, "code程序文档")
    agent_config = STORAGE_CONFIG["agents"].get(agent, {})
    subdir = agent_config.get("output_dir", "")
    
    path = os.path.join(
        STORAGE_CONFIG["base_directory"],
        type_dir,
        project_name
    )
    
    if subdir:
        path = os.path.join(path, subdir)
    
    if filename:
        path = os.path.join(path, filename)
    
    return path


def create_storage_config_file():
    """创建存储配置文件"""
    config_path = os.path.join(PROJECT_ROOT, "storage_config.json")
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(STORAGE_CONFIG, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 存储配置文件已创建: {config_path}")
    return config_path


def update_agent_tools_md():
    """更新 Agent 的 TOOLS.md 文件，添加存储规范"""
    
    storage_notice = """
## 📁 文件存储规范

### 重要提醒
所有项目文件必须保存到共享工作档案目录，禁止保存在 workspace-* 目录！

### 正确路径示例
```python
# Researcher 保存调研报告
save_path = "/home/lcc/.openclaw/共享工作档案/code程序文档/{项目名}/docs/report.md"

# Coder 保存代码
save_path = "/home/lcc/.openclaw/共享工作档案/code程序文档/{项目名}/tool.py"

# Office 保存文档
save_path = "/home/lcc/.openclaw/共享工作档案/code程序文档/{项目名}/output/document.md"
```

### 禁止行为
- ❌ 禁止保存到 workspace-* 目录
- ❌ 禁止使用相对路径
- ❌ 禁止分散存储文件

### 工具函数
```python
import sys
sys.path.insert(0, '/home/lcc/.openclaw/共享工作档案/code程序文档/travel-assistant')
from update_agent_config import get_output_path

# 获取正确的保存路径
save_path = get_output_path('researcher', 'code', 'my-project', 'report.md')
```
"""
    
    for agent, workspace in AGENT_WORKSPACES.items():
        tools_md = os.path.join(workspace, "TOOLS.md")
        if os.path.exists(tools_md):
            with open(tools_md, 'a', encoding='utf-8') as f:
                f.write(storage_notice)
            print(f"✅ 已更新 {agent} 的 TOOLS.md")


def print_storage_guide():
    """打印存储指南"""
    print("=" * 60)
    print("📁 Agent 文件存储规范")
    print("=" * 60)
    print()
    print("⚠️  重要：所有 Agent 必须遵守以下规范！")
    print()
    print("📌 存储位置:")
    print("   基础目录: /home/lcc/.openclaw/共享工作档案/")
    print()
    print("📌 各 Agent 输出目录:")
    for agent, config in STORAGE_CONFIG["agents"].items():
        subdir = config["output_dir"]
        path = f"{STORAGE_CONFIG['base_directory']}/code程序文档/{{项目名}}"
        if subdir:
            path = f"{path}/{subdir}"
        print(f"   {agent:12} -> {path}/")
    print()
    print("❌ 禁止行为:")
    print("   - 禁止保存到 workspace-* 目录")
    print("   - 禁止使用相对路径")
    print("   - 禁止分散存储文件")
    print()
    print("✅ 正确示例:")
    print('   save_path = "/home/lcc/.openclaw/共享工作档案/code程序文档/my-project/docs/report.md"')
    print()
    print("=" * 60)


def main():
    """主函数"""
    print("🚀 更新 Agent 存储配置...")
    print()
    
    # 创建存储配置文件
    config_path = create_storage_config_file()
    
    # 更新 Agent TOOLS.md
    # update_agent_tools_md()
    
    # 打印存储指南
    print_storage_guide()
    
    print()
    print("✅ 配置更新完成！")
    print(f"📄 配置文件: {config_path}")
    print()
    print("💡 使用示例:")
    print("   from update_agent_config import get_output_path")
    print("   path = get_output_path('researcher', 'code', 'project', 'file.md')")


if __name__ == '__main__':
    main()
