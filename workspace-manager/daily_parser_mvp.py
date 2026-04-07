#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
混乱中文日报最小可用解析器（MVP）
- 仅使用 Python 标准库
- 支持三种输入：--raw-text / --input-file / stdin
- 输出 JSON 数组
"""

import argparse
import json
import re
import sys
from typing import Dict, List


def extract_project(line: str) -> str:
    """项目识别优先级：【项目名】 > #项目名 > 项目:前缀"""
    m = re.search(r"【\s*([^】]+?)\s*】", line)
    if m:
        return m.group(1).strip()

    m = re.search(r"#([^\s#【】:：;,，；|]+)", line)
    if m:
        return m.group(1).strip()

    m = re.search(r"^\s*项目\s*[:：]\s*([^\s；;，,|]+)", line)
    if m:
        return m.group(1).strip()

    return ""


def extract_progress(line: str) -> str:
    """
    进展状态映射，按优先级判断：
    阻塞 > 已完成 > 进行中 > 未开始
    """
    if any(k in line for k in ["阻塞", "卡住", "失败", "异常"]):
        return "阻塞"
    if any(k in line for k in ["完成", "上线", "已解决"]):
        return "已完成"
    if any(k in line for k in ["进行中", "联调", "排查"]):
        return "进行中"
    return "未开始"


def extract_labeled_text(line: str, keywords: List[str]) -> str:
    """
    仅提取显式标签后的文本，避免误判普通动作描述：
    例如：风险：xxx / 待办:xxx / 下一步：xxx / 明天计划:xxx
    """
    pattern = re.compile(
        r"(?:"
        + "|".join(map(re.escape, keywords))
        + r")\s*[:：]\s*([^。；;\n]+)"
    )
    m = pattern.search(line)
    if not m:
        return ""
    return m.group(1).strip(" ，,:：")


def extract_risk(line: str) -> str:
    """仅提取显式风险标签后的文本"""
    return extract_labeled_text(line, ["风险", "问题", "阻塞", "异常", "失败"])


def extract_todo(line: str) -> str:
    """仅提取显式待办标签后的文本"""
    return extract_labeled_text(line, ["待办", "下一步", "明天计划"])


def clean_task(line: str) -> str:
    """
    task 清洗：
    1) 去掉项目标记
    2) 去掉显式风险/待办标签段
    3) 保留主事项文本
    """
    text = line

    # 去项目标记
    text = re.sub(r"【\s*[^】]+\s*】", "", text)
    text = re.sub(r"#([^\s#【】:：;,，；|]+)", "", text)
    text = re.sub(r"^\s*项目\s*[:：]\s*([^\s；;，,|]+)", "", text)

    # 去显式标签段
    text = re.sub(r"(?:风险|问题|阻塞|异常|失败)\s*[:：]\s*[^。；;\n]*", "", text)
    text = re.sub(r"(?:待办|下一步|明天计划)\s*[:：]\s*[^。；;\n]*", "", text)

    # 统一分隔符与空白
    text = re.sub(r"[；;|]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip(" ，,。；;:-")

    return text


def parse_raw_text(raw_text: str) -> List[Dict[str, object]]:
    """按行切分文本，每个非空行最多生成 1 条记录"""
    records: List[Dict[str, object]] = []

    for i, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        record = {
            "line_no": i,
            "project": extract_project(line),
            "task": clean_task(line),
            "progress": extract_progress(line),
            "risk": extract_risk(line),
            "todo": extract_todo(line),
        }
        records.append(record)

    return records


def read_input(args: argparse.Namespace) -> str:
    """输入优先级：--raw-text > --input-file > stdin"""
    if args.raw_text:
        return args.raw_text

    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            return f.read()

    return sys.stdin.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="混乱中文日报最小可用解析器")
    parser.add_argument("--raw-text", type=str, default="", help="原始日报文本")
    parser.add_argument("--input-file", type=str, default="", help="日报文本文件路径")
    parser.add_argument("--report-date", type=str, default="", help="日报日期（选填，YYYY-MM-DD）")
    parser.add_argument("--reporter", type=str, default="", help="提交人（选填）")
    args = parser.parse_args()

    raw_text = read_input(args)
    if not raw_text.strip():
        print("[]")
        return

    result = parse_raw_text(raw_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
