#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器自动化工具 - 使用示例
展示如何使用 browser_automation.py 进行网页操作
"""

import sys
sys.path.insert(0, '/home/lcc/.openclaw/共享工作档案/code程序文档')

from browser_automation import create_browser
import json
import time


def demo_basic_navigation():
    """演示基本导航功能"""
    print("\n" + "=" * 60)
    print("🌐 演示 1: 基本网页导航")
    print("=" * 60)
    
    browser = create_browser()
    
    # 导航到美团
    print("\n1️⃣ 导航到美团官网...")
    result = browser.navigate("https://www.meituan.com")
    time.sleep(2)
    
    # 获取页面信息
    print("\n2️⃣ 获取页面信息...")
    info = browser.get_page_info()
    if 'output' in info:
        print(f"页面标题: {info['output']}")
    
    # 截图
    print("\n3️⃣ 截取页面截图...")
    browser.screenshot("/tmp/meituan_home.png", full_page=True)
    print("✅ 截图已保存到: /tmp/meituan_home.png")
    
    print("\n✅ 演示 1 完成!")


def demo_page_snapshot():
    """演示页面快照功能"""
    print("\n" + "=" * 60)
    print("📸 演示 2: 页面快照与元素查找")
    print("=" * 60)
    
    browser = create_browser()
    
    # 导航到示例页面
    print("\n1️⃣ 导航到页面...")
    browser.navigate("https://www.example.com")
    time.sleep(1)
    
    # 获取快照
    print("\n2️⃣ 获取页面快照...")
    browser.get_snapshot()
    
    # 查找元素
    print("\n3️⃣ 查找页面元素...")
    links = browser.find_elements_by_type("link")
    print(f"找到 {len(links)} 个链接:")
    for link in links[:5]:  # 只显示前5个
        print(f"  - [{link['uid']}] {link['text'][:30]}...")
    
    # 根据文本查找
    print("\n4️⃣ 根据文本查找元素...")
    uid = browser.find_element_by_text("More")
    if uid:
        print(f"找到 'More' 链接，uid: {uid}")
    
    print("\n✅ 演示 2 完成!")


def demo_form_interaction():
    """演示表单交互"""
    print("\n" + "=" * 60)
    print("📝 演示 3: 表单交互 (使用 DuckDuckGo 搜索)")
    print("=" * 60)
    
    browser = create_browser()
    
    # 导航到 DuckDuckGo
    print("\n1️⃣ 导航到 DuckDuckGo...")
    browser.navigate("https://duckduckgo.com")
    time.sleep(2)
    
    # 获取快照
    print("\n2️⃣ 获取页面快照...")
    browser.get_snapshot()
    
    # 查找搜索框
    print("\n3️⃣ 查找搜索框...")
    # 通常搜索框是 textbox 类型
    textboxes = browser.find_elements_by_type("textbox")
    if textboxes:
        search_uid = textboxes[0]['uid']
        print(f"找到搜索框，uid: {search_uid}")
        
        # 输入搜索词
        print("\n4️⃣ 输入搜索词...")
        browser.fill(search_uid, "Python programming")
        time.sleep(1)
        
        # 按回车提交
        print("\n5️⃣ 提交搜索...")
        browser.press_key("Enter")
        time.sleep(3)
        
        # 截图
        browser.screenshot("/tmp/search_results.png")
        print("✅ 搜索结果截图已保存到: /tmp/search_results.png")
    else:
        print("❌ 未找到搜索框")
    
    print("\n✅ 演示 3 完成!")


def demo_javascript_execution():
    """演示 JavaScript 执行"""
    print("\n" + "=" * 60)
    print("⚡ 演示 4: JavaScript 执行")
    print("=" * 60)
    
    browser = create_browser()
    
    # 导航到页面
    print("\n1️⃣ 导航到页面...")
    browser.navigate("https://www.example.com")
    time.sleep(1)
    
    # 执行 JavaScript
    print("\n2️⃣ 执行 JavaScript...")
    
    # 获取页面所有链接
    result = browser.execute_script("""
        () => {
            const links = Array.from(document.querySelectorAll('a'));
            return links.slice(0, 5).map(a => ({
                text: a.textContent.trim(),
                href: a.href
            }));
        }
    """)
    print(f"页面链接: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 获取页面统计信息
    print("\n3️⃣ 获取页面统计...")
    stats = browser.execute_script("""
        () => ({
            links: document.querySelectorAll('a').length,
            images: document.querySelectorAll('img').length,
            headings: document.querySelectorAll('h1, h2, h3').length,
            paragraphs: document.querySelectorAll('p').length
        })
    """)
    print(f"页面统计: {json.dumps(stats, indent=2)}")
    
    print("\n✅ 演示 4 完成!")


def demo_device_emulation():
    """演示设备模拟"""
    print("\n" + "=" * 60)
    print("📱 演示 5: 设备模拟")
    print("=" * 60)
    
    browser = create_browser()
    
    # 导航到响应式测试页面
    print("\n1️⃣ 导航到页面...")
    browser.navigate("https://www.example.com")
    time.sleep(1)
    
    # 桌面视图
    print("\n2️⃣ 桌面视图 (1920x1080)...")
    browser.emulate_desktop()
    time.sleep(1)
    browser.screenshot("/tmp/desktop_view.png")
    print("✅ 桌面视图截图已保存")
    
    # 平板视图
    print("\n3️⃣ 平板视图 (768x1024)...")
    browser.emulate_tablet()
    time.sleep(1)
    browser.screenshot("/tmp/tablet_view.png")
    print("✅ 平板视图截图已保存")
    
    # 手机视图
    print("\n4️⃣ 手机视图 (375x667)...")
    browser.emulate_mobile()
    time.sleep(1)
    browser.screenshot("/tmp/mobile_view.png")
    print("✅ 手机视图截图已保存")
    
    print("\n✅ 演示 5 完成!")


def demo_network_monitoring():
    """演示网络监控"""
    print("\n" + "=" * 60)
    print("🌐 演示 6: 网络请求监控")
    print("=" * 60)
    
    browser = create_browser()
    
    # 导航到页面
    print("\n1️⃣ 导航到页面...")
    browser.navigate("https://www.example.com")
    time.sleep(2)
    
    # 获取网络请求
    print("\n2️⃣ 获取网络请求列表...")
    requests = browser.list_network_requests(page_size=20)
    print(f"网络请求: {json.dumps(requests, indent=2)[:500]}...")
    
    # 获取控制台消息
    print("\n3️⃣ 获取控制台消息...")
    messages = browser.list_console_messages(page_size=10)
    print(f"控制台消息: {json.dumps(messages, indent=2)[:500]}...")
    
    print("\n✅ 演示 6 完成!")


def demo_data_collection():
    """
    演示数据采集 - 以美团为例
    注意：这只是一个示例框架，实际使用需要根据具体页面结构调整
    """
    print("\n" + "=" * 60)
    print("📊 演示 7: 数据采集框架 (美团示例)")
    print("=" * 60)
    
    browser = create_browser()
    
    print("\n📋 数据采集流程:")
    print("1. 导航到目标网站")
    print("2. 获取页面快照，分析页面结构")
    print("3. 定位搜索框/筛选条件")
    print("4. 输入搜索词并提交")
    print("5. 等待结果加载")
    print("6. 使用 JavaScript 提取数据")
    print("7. 保存数据到文件")
    
    print("\n💡 示例代码框架:")
    print("""
    # 1. 导航
    browser.navigate("https://www.meituan.com")
    
    # 2. 获取快照
    browser.get_snapshot()
    
    # 3. 查找搜索框
    search_uid = browser.find_element_by_text("搜索")
    
    # 4. 输入并搜索
    browser.fill(search_uid, "昆明美食")
    browser.press_key("Enter")
    
    # 5. 等待结果
    browser.wait_for(["综合排序", "商家列表"], timeout=10000)
    
    # 6. 提取数据
    data = browser.execute_script("""
        () => {
            // 根据实际页面结构编写提取逻辑
            const items = document.querySelectorAll('.shop-item');
            return Array.from(items).map(item => ({
                name: item.querySelector('.shop-name')?.textContent,
                rating: item.querySelector('.rating')?.textContent,
                // ...
            }));
        }
    """)
    
    # 7. 保存数据
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    """)
    
    print("\n⚠️ 注意:")
    print("- 实际使用时需要根据目标网站的具体页面结构调整选择器")
    print("- 建议先手动访问网站，使用浏览器开发者工具分析 DOM 结构")
    print("- 遵守网站的 robots.txt 和服务条款")
    print("- 控制请求频率，避免对服务器造成压力")
    
    print("\n✅ 演示 7 完成!")


def main():
    """主函数 - 运行所有演示"""
    print("\n" + "=" * 60)
    print("🚀 浏览器自动化工具 - 完整演示")
    print("=" * 60)
    
    demos = [
        ("基本导航", demo_basic_navigation),
        ("页面快照", demo_page_snapshot),
        ("表单交互", demo_form_interaction),
        ("JavaScript 执行", demo_javascript_execution),
        ("设备模拟", demo_device_emulation),
        ("网络监控", demo_network_monitoring),
        ("数据采集框架", demo_data_collection),
    ]
    
    print("\n可用演示:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. 运行所有演示")
    print("  q. 退出")
    
    choice = input("\n请选择要运行的演示 (0-7, q): ").strip()
    
    if choice == 'q':
        print("再见!")
        return
    
    if choice == '0':
        for name, func in demos:
            try:
                func()
            except Exception as e:
                print(f"\n❌ 演示 '{name}' 出错: {e}")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(demos):
                demos[idx][1]()
            else:
                print("无效选择")
        except ValueError:
            print("无效输入")
        except Exception as e:
            print(f"\n❌ 演示出错: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 演示结束!")
    print("=" * 60)


if __name__ == "__main__":
    main()
