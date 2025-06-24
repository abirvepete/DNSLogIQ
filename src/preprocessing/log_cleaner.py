#!/usr/bin/env python3
"""
Step 1: 去头模块
去掉原始日志行前面的 timestamp、level、连接码等冗余信息
"""

import re
import argparse
from pathlib import Path

def normalize_line(line: str) -> str:
    # 用正则一把清理前缀：
    # +0800 2025-06-22 07:27:53 INFO [2174766721 0ms] → 空
    cleaned = re.sub(
        r'^\s*\+?\d{4}\s+\d{4}-\d{2}-\d{2}\s+'
        r'\d{2}:\d{2}:\d{2}\s+\S+\s+\[[^\]]+\]\s*',
        '',
        line
    )
    return cleaned.strip()

def main():
    from pathlib import Path

    # 获取当前脚本文件的绝对路径
    current_file = Path(__file__).resolve()
    # 获取项目根目录（根据层级调整）
    project_root = current_file.parent.parent.parent

    print(f"项目根目录: {project_root}")

    # 构建输入输出路径
    input_path = project_root / "data" / "raw_logs" / "demo.log"
    output_path = project_root / "data" / "processed_logs" / "step1_cleaned.log"

    print(f"输入路径: {input_path}")
    print(f"是否存在: {input_path.exists()}")

    if not input_path.exists():
        print("❌ 错误：输入文件不存在！")
        return

    # 创建输出目录
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 处理逻辑
    with input_path.open("r", encoding="utf-8") as fin, output_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            cleaned = normalize_line(line.rstrip("\n"))
            if cleaned:
                fout.write(cleaned + "\n")

    print(f"[Step1] 去头完成：{output_path}")

if __name__ == "__main__":
    main()