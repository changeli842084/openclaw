#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小可用解析器（MVP）
功能：将混乱中文日报按“单行单记录”解析为结构化 JSON 数组。
仅使用 Python 标准库。
"""

import argparse
import json
import re
import sys
from typing import Dict, List


PROJECT_PATTERNS = [
    re.compile(r"【\s*([^】]+?)\s*】"),
    re.compile(r"#([^\s#【】:：;,，；|]+)"),
    re.compile(r"^\s*项目\s*[:：]\s*([^\s;；,，|]+)"),
]


def extract_project(line: str) -> str:
    """项目名识别优先级： 【项目名】 > #项目名 > 项目:前缀"""
    for pattern in PROJECT_PATTERNS:
        m = pattern.search(line)
        if m:
            return m.group(1).strip()
    return ""


def extract_progress(line: str) -> str:
    """进展状态映射：阻塞 > 已完成 > 进行中 > 未开始"""
    if any(k in line for k in ["阻塞", "卡住", "失败"]):
        return "阻塞"
    if any(k in line for k in ["完成", "已上线"]):
        return "已完成"
    if any(k in line for k in ["进行中", "联调", "排查"]):
        return "进行中"
    return "未开始"


def _extract_desc_after_keyword(line: str, keywords: List[str]) -> str:
    """
    提取“关键词后的描述”：
    - 支持“关键词:描述”或“关键词 描述”
    - 截断到句号/分号（。；;）
    """
    pattern = re.compile(r"(?:" + "|".join(keywords) + r")\s*[:：]?\s*([^。；;]+)")
    m = pattern.search(line)
    if not m:
        return ""
    return m.group(1).strip(" ，,:：")


def extract_risk(line: str) -> str:
    """risk 字段：提取风险关键词后的描述"""
    return _extract_desc_after_keyword(line, ["风险", "问题", "阻塞", "异常", "失败"])


def extract_todo(line: str) -> str:
    """todo 字段：提取待办关键词后的描述（优先待办/下一步，再明天）"""
    desc = _extract_desc_after_keyword(line, ["待办", "下一步"])
    if desc:
        return desc
    return _extract_desc_after_keyword(line, ["明天"])


def clean_task(line: str) -> str:
    """
    task 清洗：
    - 移除项目标记
    - 移除显式标签段（风险:xxx / 待办:xxx / 下一步:xxx）
    - 保留主动作内容
    """
    text = line

    # 移除项目标记
    text = re.sub(r"【\s*[^】]+\s*】", "", text)
    text = re.sub(r"#([^\s#【】:：;,，；|]+)", "", text)
    text = re.sub(r"^\s*项目\s*[:：]\s*([^\s;；,，|]+)", "", text)

    # 仅移除显式标签段，避免过度清洗
    text = re.sub(r"(?:风险|问题|阻塞|异常|失败)\s*[:：]\s*[^。；;]*", "", text)
    text = re.sub(r"(?:待办|下一步)\s*[:：]\s*[^。；;]*", "", text)

    # 清理分隔符与多余空白
    text = re.sub(r"[；;|]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" ，,。；;:-")

    return text


def parse_raw_text(raw_text: str) -> List[Dict[str, str]]:
    """按换行切分，每行最多生成 1 条结构化记录"""
    records: List[Dict[str, str]] = []

    for idx, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        record = {
            "line_no": idx,
            "project": extract_project(line),
            "task": clean_task(line),
            "progress": extract_progress(line),
            "risk": extract_risk(line),
            "todo": extract_todo(line),
        }
        records.append(record)

    return records


def load_input_text(args: argparse.Namespace) -> str:
    """输入优先级：--raw-text > --input-file > stdin"""
    if args.raw_text:
        return args.raw_text

    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            return f.read()

    return sys.stdin.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="混乱中文日报最小可用解析器")
    parser.add_argument("--raw-text", type=str, default="", help="原始日报全文")
    parser.add_argument("--input-file", type=str, default="", help="原始日报文件路径")
    parser.add_argument("--report-date", type=str, default="", help="日报日期（选填，YYYY-MM-DD）")
    parser.add_argument("--reporter", type=str, default="", help="提交人（选填）")
    args = parser.parse_args()

    raw_text = load_input_text(args)
    if not raw_text.strip():
        print("[]")
        return

    records = parse_raw_text(raw_text)
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
