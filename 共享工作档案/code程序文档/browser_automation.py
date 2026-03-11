#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器自动化工具 - 使用 mcporter + chrome-devtools-mcp
用于网页浏览、数据采集、自动化操作

作者: AI Assistant
创建时间: 2026-03-11
"""

import subprocess
import json
import time
import re
from typing import Optional, Dict, List, Any

class BrowserAutomation:
    """浏览器自动化控制器"""
    
    def __init__(self, config_path: str = "~/.config/mcporter/mcporter.json"):
        """
        初始化浏览器自动化工具
        
        Args:
            config_path: mcporter 配置文件路径
        """
        self.config_path = config_path
        self.server_name = "chrome-devtools"
        self.current_url = None
        self.page_elements = {}  # 缓存页面元素
    
    def _run_mcporter(self, tool: str, **kwargs) -> Dict[str, Any]:
        """
        调用 mcporter 执行工具
        
        Args:
            tool: 工具名称，如 "navigate_page", "take_snapshot" 等
            **kwargs: 工具参数
            
        Returns:
            解析后的 JSON 结果
        """
        # 构建参数
        args_list = []
        for key, value in kwargs.items():
            if isinstance(value, bool):
                args_list.append(f"{key}={str(value).lower()}")
            elif isinstance(value, (list, dict)):
                args_list.append(f"{key}={json.dumps(value)}")
            else:
                args_list.append(f"{key}={value}")
        
        # 构建命令
        cmd = [
            "mcporter", "call",
            f"{self.server_name}.{tool}",
            "--config", self.config_path,
            "--output", "json"
        ]
        
        for arg in args_list:
            cmd.append(arg)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"❌ 错误: {result.stderr}")
                return {"error": result.stderr}
            
            # 尝试解析 JSON 输出
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                # 如果不是 JSON，返回原始文本
                return {"output": result.stdout}
                
        except subprocess.TimeoutExpired:
            return {"error": "命令执行超时"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== 导航操作 ====================
    
    def navigate(self, url: str, ignore_cache: bool = False) -> Dict[str, Any]:
        """
        导航到指定 URL
        
        Args:
            url: 目标网址
            ignore_cache: 是否忽略缓存
            
        Returns:
            操作结果
            
        Example:
            >>> browser = BrowserAutomation()
            >>> browser.navigate("https://www.meituan.com")
        """
        result = self._run_mcporter(
            "navigate_page",
            type="url",
            url=url,
            ignoreCache=ignore_cache
        )
        if "error" not in result:
            self.current_url = url
            print(f"✅ 已导航到: {url}")
        return result
    
    def reload(self, ignore_cache: bool = True) -> Dict[str, Any]:
        """刷新当前页面"""
        return self._run_mcporter("navigate_page", type="reload", ignoreCache=ignore_cache)
    
    def go_back(self) -> Dict[str, Any]:
        """返回上一页"""
        return self._run_mcporter("navigate_page", type="back")
    
    def go_forward(self) -> Dict[str, Any]:
        """前进"""
        return self._run_mcporter("navigate_page", type="forward")
    
    # ==================== 页面信息获取 ====================
    
    def get_snapshot(self, verbose: bool = False) -> Dict[str, Any]:
        """
        获取页面结构快照
        
        Returns:
            页面元素结构，包含 uid、元素类型、文本内容等
            
        Example:
            >>> snapshot = browser.get_snapshot()
            >>> print(snapshot)
        """
        result = self._run_mcporter("take_snapshot", verbose=verbose)
        if "output" in result:
            # 解析文本输出，提取元素信息
            self._parse_snapshot(result["output"])
        return result
    
    def _parse_snapshot(self, snapshot_text: str):
        """解析快照文本，提取元素信息"""
        self.page_elements = {}
        lines = snapshot_text.split('\n')
        for line in lines:
            # 匹配 uid=xxx 格式
            match = re.search(r'uid=(\S+)\s+(\S+)\s+"([^"]*)"', line)
            if match:
                uid, elem_type, text = match.groups()
                self.page_elements[uid] = {
                    'type': elem_type,
                    'text': text,
                    'uid': uid
                }
    
    def find_element_by_text(self, text: str) -> Optional[str]:
        """
        根据文本内容查找元素 uid
        
        Args:
            text: 要查找的文本
            
        Returns:
            元素 uid 或 None
            
        Example:
            >>> uid = browser.find_element_by_text("搜索")
            >>> if uid:
            ...     browser.click(uid)
        """
        for uid, info in self.page_elements.items():
            if text.lower() in info['text'].lower():
                return uid
        return None
    
    def find_elements_by_type(self, elem_type: str) -> List[Dict]:
        """
        根据元素类型查找所有匹配元素
        
        Args:
            elem_type: 元素类型，如 "link", "button", "textbox" 等
            
        Returns:
            匹配的元素列表
        """
        return [
            info for uid, info in self.page_elements.items()
            if info['type'].lower() == elem_type.lower()
        ]
    
    # ==================== 元素操作 ====================
    
    def click(self, uid: str, include_snapshot: bool = False) -> Dict[str, Any]:
        """
        点击元素
        
        Args:
            uid: 元素 uid
            include_snapshot: 是否在返回结果中包含页面快照
            
        Example:
            >>> browser.click("1_42")
        """
        return self._run_mcporter("click", uid=uid, includeSnapshot=include_snapshot)
    
    def fill(self, uid: str, value: str, include_snapshot: bool = False) -> Dict[str, Any]:
        """
        填写表单元素
        
        Args:
            uid: 输入框元素 uid
            value: 要填入的值
            include_snapshot: 是否在返回结果中包含页面快照
            
        Example:
            >>> browser.fill("1_15", "昆明美食")
        """
        return self._run_mcporter("fill", uid=uid, value=value, includeSnapshot=include_snapshot)
    
    def type_text(self, text: str, submit_key: Optional[str] = None) -> Dict[str, Any]:
        """
        输入文本
        
        Args:
            text: 要输入的文本
            submit_key: 提交按键，如 "Enter"
            
        Example:
            >>> browser.type_text("昆明美食", submit_key="Enter")
        """
        kwargs = {"text": text}
        if submit_key:
            kwargs["submitKey"] = submit_key
        return self._run_mcporter("type_text", **kwargs)
    
    def press_key(self, key: str, include_snapshot: bool = False) -> Dict[str, Any]:
        """
        按下键盘按键
        
        Args:
            key: 按键名称，如 "Enter", "Tab", "Escape" 等
            include_snapshot: 是否在返回结果中包含页面快照
            
        Example:
            >>> browser.press_key("Enter")
        """
        return self._run_mcporter("press_key", key=key, includeSnapshot=include_snapshot)
    
    def hover(self, uid: str, include_snapshot: bool = False) -> Dict[str, Any]:
        """悬停在元素上"""
        return self._run_mcporter("hover", uid=uid, includeSnapshot=include_snapshot)
    
    def wait_for(self, texts: List[str], timeout: int = 5000) -> Dict[str, Any]:
        """
        等待页面中出现指定文本
        
        Args:
            texts: 要等待的文本列表
            timeout: 超时时间（毫秒）
            
        Example:
            >>> browser.wait_for(["加载完成", "综合排序"], timeout=10000)
        """
        return self._run_mcporter("wait_for", text=texts, timeout=timeout)
    
    # ==================== JavaScript 执行 ====================
    
    def execute_script(self, script: str, args: Optional[List] = None) -> Dict[str, Any]:
        """
        在页面中执行 JavaScript
        
        Args:
            script: JavaScript 函数代码
            args: 传递给函数的参数列表
            
        Returns:
            脚本执行结果
            
        Example:
            >>> # 获取页面标题
            >>> result = browser.execute_script("() => document.title")
            >>> 
            >>> # 获取所有链接
            >>> result = browser.execute_script(
            ...     "() => Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.text}))"
            ... )
        """
        kwargs = {"function": script}
        if args:
            kwargs["args"] = json.dumps(args)
        return self._run_mcporter("evaluate_script", **kwargs)
    
    def get_page_info(self) -> Dict[str, Any]:
        """获取页面基本信息（标题、URL等）"""
        return self.execute_script("""
            () => ({
                title: document.title,
                url: window.location.href,
                domain: window.location.hostname,
                pathname: window.location.pathname
            })
        """)
    
    # ==================== 截图 ====================
    
    def screenshot(self, file_path: str, full_page: bool = False, 
                   format: str = "png") -> Dict[str, Any]:
        """
        截取屏幕截图
        
        Args:
            file_path: 保存路径
            full_page: 是否截取整个页面
            format: 图片格式 (png, jpeg, webp)
            
        Example:
            >>> browser.screenshot("/tmp/meituan.png", full_page=True)
        """
        return self._run_mcporter(
            "take_screenshot",
            filePath=file_path,
            fullPage=full_page,
            format=format
        )
    
    # ==================== 网络监控 ====================
    
    def list_network_requests(self, page_size: int = 50) -> Dict[str, Any]:
        """列出网络请求"""
        return self._run_mcporter("list_network_requests", pageSize=page_size)
    
    def list_console_messages(self, page_size: int = 50) -> Dict[str, Any]:
        """列出控制台日志"""
        return self._run_mcporter("list_console_messages", pageSize=page_size)
    
    # ==================== 设备模拟 ====================
    
    def emulate_device(self, width: int, height: int) -> Dict[str, Any]:
        """
        模拟设备视口
        
        Args:
            width: 视口宽度
            height: 视口高度
            
        Example:
            >>> # 模拟手机
            >>> browser.emulate_device(375, 667)
        """
        return self._run_mcporter("resize_page", width=width, height=height)
    
    def emulate_mobile(self) -> Dict[str, Any]:
        """模拟移动端设备 (iPhone SE)"""
        return self.emulate_device(375, 667)
    
    def emulate_tablet(self) -> Dict[str, Any]:
        """模拟平板设备 (iPad)"""
        return self.emulate_device(768, 1024)
    
    def emulate_desktop(self) -> Dict[str, Any]:
        """模拟桌面设备"""
        return self.emulate_device(1920, 1080)
    
    # ==================== 性能分析 ====================
    
    def start_performance_trace(self, reload: bool = True) -> Dict[str, Any]:
        """开始性能追踪"""
        return self._run_mcporter("performance_start_trace", reload=reload)
    
    def stop_performance_trace(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """停止性能追踪"""
        kwargs = {}
        if file_path:
            kwargs["filePath"] = file_path
        return self._run_mcporter("performance_stop_trace", **kwargs)
    
    def lighthouse_audit(self, device: str = "desktop", 
                        mode: str = "navigation") -> Dict[str, Any]:
        """
        运行 Lighthouse 性能审计
        
        Args:
            device: 设备类型 (desktop, mobile)
            mode: 审计模式 (navigation, snapshot)
        """
        return self._run_mcporter(
            "lighthouse_audit",
            device=device,
            mode=mode
        )


# ==================== 便捷函数 ====================

def create_browser(config_path: str = "~/.config/mcporter/mcporter.json") -> BrowserAutomation:
    """
    创建浏览器自动化实例
    
    Returns:
        BrowserAutomation 实例
        
    Example:
        >>> browser = create_browser()
        >>> browser.navigate("https://www.example.com")
    """
    return BrowserAutomation(config_path)


# ==================== 使用示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("浏览器自动化工具 - 使用示例")
    print("=" * 60)
    
    # 创建浏览器实例
    browser = create_browser()
    
    # 示例 1: 基本导航
    print("\n📍 示例 1: 导航到网页")
    browser.navigate("https://www.example.com")
    
    # 示例 2: 获取页面信息
    print("\n📍 示例 2: 获取页面信息")
    info = browser.get_page_info()
    print(f"页面信息: {json.dumps(info, indent=2, ensure_ascii=False)}")
    
    # 示例 3: 获取页面快照
    print("\n📍 示例 3: 获取页面快照")
    snapshot = browser.get_snapshot()
    print(f"已获取页面快照，缓存了 {len(browser.page_elements)} 个元素")
    
    # 示例 4: 截图
    print("\n📍 示例 4: 截图")
    browser.screenshot("/tmp/example.png", full_page=True)
    print("截图已保存到 /tmp/example.png")
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)
