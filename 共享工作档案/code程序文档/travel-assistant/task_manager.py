#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务管理器 - 智能旅行助手项目
确保任务闭环和文件正确存储

作者: Manager Agent
日期: 2026-03-11
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class TaskManager:
    """
    任务管理器
    
    管理项目任务的分配、执行和闭环
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化任务管理器
        
        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                "project_config.json"
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.base_dir = self.config['base_directory']
        self._ensure_directories()
        
        # 任务状态跟踪
        self.tasks: Dict[str, Dict] = {}
        self.task_log = os.path.join(self.base_dir, "task_log.json")
        self._load_task_log()
    
    def _ensure_directories(self) -> None:
        """确保所有目录存在"""
        for dir_path in self.config['directories'].values():
            os.makedirs(dir_path, exist_ok=True)
            print(f"[INFO] 确保目录存在: {dir_path}")
    
    def _load_task_log(self) -> None:
        """加载任务日志"""
        if os.path.exists(self.task_log):
            with open(self.task_log, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = {}
    
    def _save_task_log(self) -> None:
        """保存任务日志"""
        with open(self.task_log, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def create_task(self, task_id: str, agent: str, description: str,
                   output_file: str, dependencies: List[str] = None) -> Dict:
        """
        创建新任务
        
        Args:
            task_id: 任务ID
            agent: 执行Agent (researcher/coder/office)
            description: 任务描述
            output_file: 预期输出文件（相对路径）
            dependencies: 依赖的任务ID列表
            
        Returns:
            任务信息字典
        """
        # 获取Agent的保存路径
        agent_config = self.config['agents'].get(agent, {})
        save_dir = agent_config.get('save_path', self.base_dir)
        
        # 构建完整输出路径
        full_output_path = os.path.join(save_dir, output_file)
        
        task = {
            'task_id': task_id,
            'agent': agent,
            'description': description,
            'output_file': output_file,
            'full_output_path': full_output_path,
            'dependencies': dependencies or [],
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'verified_at': None
        }
        
        self.tasks[task_id] = task
        self._save_task_log()
        
        print(f"[INFO] 创建任务: {task_id}")
        print(f"       Agent: {agent}")
        print(f"       输出: {full_output_path}")
        
        return task
    
    def start_task(self, task_id: str) -> None:
        """标记任务开始"""
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = 'in_progress'
            self.tasks[task_id]['started_at'] = datetime.now().isoformat()
            self._save_task_log()
            print(f"[INFO] 任务开始: {task_id}")
    
    def complete_task(self, task_id: str) -> bool:
        """
        标记任务完成并验证
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功验证
        """
        if task_id not in self.tasks:
            print(f"[ERROR] 任务不存在: {task_id}")
            return False
        
        task = self.tasks[task_id]
        output_path = task['full_output_path']
        
        # 验证输出文件是否存在
        if os.path.exists(output_path):
            task['status'] = 'completed'
            task['completed_at'] = datetime.now().isoformat()
            task['verified_at'] = datetime.now().isoformat()
            task['file_size'] = os.path.getsize(output_path)
            self._save_task_log()
            
            print(f"[SUCCESS] 任务完成并验证: {task_id}")
            print(f"          输出文件: {output_path}")
            print(f"          文件大小: {task['file_size']} bytes")
            return True
        else:
            task['status'] = 'failed'
            task['error'] = f"输出文件不存在: {output_path}"
            self._save_task_log()
            
            print(f"[ERROR] 任务完成但验证失败: {task_id}")
            print(f"        预期文件: {output_path}")
            return False
    
    def check_dependencies(self, task_id: str) -> bool:
        """
        检查任务依赖是否满足
        
        Args:
            task_id: 任务ID
            
        Returns:
            依赖是否全部完成
        """
        if task_id not in self.tasks:
            return False
        
        dependencies = self.tasks[task_id].get('dependencies', [])
        for dep_id in dependencies:
            if dep_id not in self.tasks:
                print(f"[WARNING] 依赖任务不存在: {dep_id}")
                return False
            if self.tasks[dep_id]['status'] != 'completed':
                print(f"[WARNING] 依赖任务未完成: {dep_id}")
                return False
        
        return True
    
    def get_task_status(self, task_id: str = None) -> Dict:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID，为None则返回所有任务
            
        Returns:
            任务状态字典
        """
        if task_id:
            return self.tasks.get(task_id, {})
        
        # 统计所有任务
        status_count = {
            'created': 0,
            'in_progress': 0,
            'completed': 0,
            'failed': 0
        }
        
        for task in self.tasks.values():
            status = task.get('status', 'unknown')
            status_count[status] = status_count.get(status, 0) + 1
        
        return {
            'total': len(self.tasks),
            'by_status': status_count,
            'tasks': self.tasks
        }
    
    def generate_report(self) -> str:
        """
        生成项目报告
        
        Returns:
            报告文件路径
        """
        report_path = os.path.join(
            self.config['directories']['output'],
            f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        status = self.get_task_status()
        
        report = f"""# 智能旅行助手 - 项目报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 任务统计

- 总任务数: {status['total']}
- 已完成: {status['by_status'].get('completed', 0)}
- 进行中: {status['by_status'].get('in_progress', 0)}
- 待开始: {status['by_status'].get('created', 0)}
- 失败: {status['by_status'].get('failed', 0)}

## 任务详情

"""
        
        for task_id, task in self.tasks.items():
            report += f"""### {task_id}
- **Agent**: {task['agent']}
- **描述**: {task['description']}
- **状态**: {task['status']}
- **输出文件**: {task['full_output_path']}
- **创建时间**: {task['created_at']}
- **完成时间**: {task.get('completed_at', 'N/A')}

"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[INFO] 项目报告已生成: {report_path}")
        return report_path


def main():
    """演示任务管理器功能"""
    print("=" * 60)
    print("🚀 任务管理器 - 智能旅行助手")
    print("=" * 60)
    
    # 创建任务管理器
    manager = TaskManager()
    
    # 创建项目任务
    print("\n📋 创建项目任务...")
    
    # 阶段2: 调研任务
    manager.create_task(
        task_id="phase2_research",
        agent="researcher",
        description="昆明旅行信息调研",
        output_file="research_report.md",
        dependencies=[]
    )
    
    # 阶段4: 工具开发任务
    manager.create_task(
        task_id="phase4_price_monitor",
        agent="coder",
        description="价格监控工具开发",
        output_file="price_monitor.py",
        dependencies=[]
    )
    
    manager.create_task(
        task_id="phase4_route_optimizer",
        agent="coder",
        description="行程优化工具开发",
        output_file="route_optimizer.py",
        dependencies=[]
    )
    
    manager.create_task(
        task_id="phase4_budget_visualizer",
        agent="coder",
        description="预算可视化工具开发",
        output_file="budget_visualizer.py",
        dependencies=[]
    )
    
    # 验证已完成的文件
    print("\n🔍 验证已完成的文件...")
    
    # 检查 price_monitor.py
    if os.path.exists(os.path.join(manager.base_dir, "price_monitor.py")):
        manager.start_task("phase4_price_monitor")
        manager.complete_task("phase4_price_monitor")
    
    # 检查 route_optimizer.py
    if os.path.exists(os.path.join(manager.base_dir, "route_optimizer.py")):
        manager.start_task("phase4_route_optimizer")
        manager.complete_task("phase4_route_optimizer")
    
    # 获取任务状态
    print("\n📊 任务状态:")
    status = manager.get_task_status()
    print(f"  总任务: {status['total']}")
    print(f"  已完成: {status['by_status'].get('completed', 0)}")
    print(f"  进行中: {status['by_status'].get('in_progress', 0)}")
    print(f"  待开始: {status['by_status'].get('created', 0)}")
    
    # 生成项目报告
    print("\n📄 生成项目报告...")
    report_path = manager.generate_report()
    
    print("\n" + "=" * 60)
    print("✅ 任务管理器初始化完成！")
    print("=" * 60)
    print(f"\n项目目录: {manager.base_dir}")
    print(f"任务日志: {manager.task_log}")
    print(f"项目报告: {report_path}")


if __name__ == '__main__':
    main()
