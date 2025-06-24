#!/usr/bin/env python3
"""
pattern_generator.py
基于去重后的样本日志生成通配符/正则模板，用于候选匹配规则的自动生成。
"""

import re
import difflib
from pathlib import Path
import argparse

def deduplicate_logs(log_file: str) -> list:
    unique_lines = set()
    samples = []
    with Path(log_file).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and line not in unique_lines:
                unique_lines.add(line)
                samples.append(line)
    return samples

def generate_regex_for_two(s1: str, s2: str, wildcard: str = ".*") -> str:
    matcher = difflib.SequenceMatcher(None, s1, s2)
    pattern = ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            pattern += re.escape(s1[i1:i2])
        else:
            pattern += wildcard
    return pattern

def generate_common_regex(samples: list, wildcard: str = ".*") -> str:
    if not samples:
        return ""
    pattern = samples[0]
    for sample in samples[1:]:
        pattern = generate_regex_for_two(pattern, sample, wildcard)
    return pattern

def main():
    parser = argparse.ArgumentParser(
        description="根据输入样本日志生成候选通配符/正则规则模板。"
    )
    parser.add_argument("-i", "--input", required=True, help="输入样本日志文件")
    parser.add_argument("-d", "--dedup_output", required=True, help="输出文件保存去重后的样本")
    parser.add_argument("-w", "--wildcard_output", required=True, help="输出文件保存生成的正则模板")
    parser.add_argument("-n", "--num", type=int, default=10, help="采样生成模板的样本数")
    args = parser.parse_args()

    samples = deduplicate_logs(args.input)
    print(f"去重后共有 {len(samples)} 个样本。")

    with open(args.dedup_output, "w", encoding="utf-8") as df:
        for line in samples:
            df.write(line + "\n")
    print(f"去重样本保存至 {args.dedup_output}")

    selected_samples = samples[:args.num]
    regex_pattern = generate_common_regex(selected_samples)
    print("生成的正则模板：")
    print(regex_pattern)

    with open(args.wildcard_output, "w", encoding="utf-8") as wf:
        wf.write(regex_pattern + "\n")
    print(f"正则模板保存至 {args.wildcard_output}")

if __name__ == "__main__":
    main()