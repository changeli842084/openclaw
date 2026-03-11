#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 配置文件

所有 Agent 必须使用此配置来确定文件保存路径
确保任务闭环和文件统一管理

使用方法:
    from agent_config import get_output_path, AGENT_CONFIG
    
    # 获取保存路径
    save_path = get_output_path('researcher', 'report.md')
    
    # 或者使用完整路径
    save_path = AGENT_CONFIG['base_directory'] + '/docs/report.md'
"""

import os

# 项目根目录
PROJECT_ROOT = "/home/lcc/.openclaw/共享工作档案/code程序文档/travel-assistant"

# Agent 配置
AGENT_CONFIG = {
    "base_directory": PROJECT_ROOT,
    "agents": {
        "researcher": {
            "name": "Researcher",
            "description": "负责信息调研和数据收集",
            "output_directory": os.path.join(PROJECT_ROOT, "docs"),
            "allowed_formats": [".md", ".txt", ".json", ".csv"]
        },
        "coder": {
            "name": "Coder",
            "description": "负责代码开发和工具编写",
            "output_directory": PROJECT_ROOT,
            "allowed_formats": [".py", ".js", ".sh", ".json"]
        },
        "office": {
            "name": "Office",
            "description": "负责文档制作和表格生成",
            "output_directory": os.path.join(PROJECT_ROOT, "output"),
            "allowed_formats": [".docx", ".xlsx", ".pdf", ".pptx"]
        }
    },
    "shared_directories": {
        "docs": os.path.join(PROJECT_ROOT, "docs"),
        "data": os.path.join(PROJECT_ROOT, "data"),
        "output": os.path.join(PROJECT_ROOT, "output"),
        "code": PROJECT_ROOT,
        "screenshots": "/home/lcc/.openclaw/共享工作档案/截图"
    }
}


def get_output_path(agent_type: str, filename: str) -> str:
    """
    获取 Agent 的输出文件路径
    
    Args:
        agent_type: Agent 类型 (researcher/coder/office)
        filename: 文件名
        
    Returns:
        完整的文件保存路径
    """
    if agent_type not in AGENT_CONFIG['agents']:
        raise ValueError(f"未知的 Agent 类型: {agent_type}")
    
    agent = AGENT_CONFIG['agents'][agent_type]
    output_dir = agent['output_directory']
    
    # 确保目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 返回完整路径
    return os.path.join(output_dir, filename)


def get_shared_path(directory: str, filename: str = None) -> str:
    """
    获取共享目录路径
    
    Args:
        directory: 目录名称 (docs/data/output/code/screenshots)
        filename: 文件名（可选）
        
    Returns:
        目录路径或完整文件路径
    """
    if directory not in AGENT_CONFIG['shared_directories']:
        raise ValueError(f"未知的目录: {directory}")
    
    path = AGENT_CONFIG['shared_directories'][directory]
    
    # 确保目录存在
    os.makedirs(path, exist_ok=True)
    
    if filename:
        return os.path.join(path, filename)
    return path


def validate_file_path(filepath: str, agent_type: str = None) -> bool:
    """
    验证文件路径是否在允许的范围内
    
    Args:
        filepath: 文件路径
        agent_type: Agent 类型（可选）
        
    Returns:
        是否有效
    """
    # 必须是绝对路径
    if not os.path.isabs(filepath):
        print(f"[ERROR] 必须使用绝对路径: {filepath}")
        return False
    
    # 检查是否在项目目录内
    if not filepath.startswith(PROJECT_ROOT):
        print(f"[ERROR] 文件必须在项目目录内: {filepath}")
        return False
    
    # 如果指定了 Agent 类型，检查文件格式
    if agent_type:
        ext = os.path.splitext(filepath)[1].lower()
        allowed = AGENT_CONFIG['agents'][agent_type]['allowed_formats']
        if ext not in allowed:
            print(f"[ERROR] Agent {agent_type} 不允许保存 {ext} 格式文件")
            print(f"       允许的格式: {', '.join(allowed)}")
            return False
    
    return True


def print_config():
    """打印配置信息"""
    print("=" * 60)
    print("📋 Agent 配置文件")
    print("=" * 60)
    print(f"\n项目根目录: {PROJECT_ROOT}")
    print("\n共享目录:")
    for name, path in AGENT_CONFIG['shared_directories'].items():
        print(f"  {name}: {path}")
    
    print("\nAgent 配置:")
    for agent_type, config in AGENT_CONFIG['agents'].items():
        print(f"\n  [{agent_type}] {config['name']}")
        print(f"    描述: {config['description']}")
        print(f"    输出目录: {config['output_directory']}")
        print(f"    允许格式: {', '.join(config['allowed_formats'])}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    print_config()
    
    # 演示使用
    print("\n💡 使用示例:")
    print(f"  Researcher 保存报告: {get_output_path('researcher', 'report.md')}")
    print(f"  Coder 保存脚本: {get_output_path('coder', 'tool.py')}")
    print(f"  Office 保存文档: {get_output_path('office', 'document.docx')}")
    print(f"  共享数据目录: {get_shared_path('data')}")
