#!/usr/bin/env python3
"""
deduplicate_logs.py
读取原始日志文件，对日志进行清洗、归一化和去重，输出 deduped_logs 文件，供后续数据分析使用。
"""

from pathlib import Path
from src.preprocessing.log_cleaner import normalize_line


def deduplicate_logs(log_file: str) -> list:
    unique_norm = {}
    deduped = []
    with Path(log_file).open("r", encoding="utf-8") as f:
        for line in f:
            orig = line.strip()
            if not orig:
                continue
            norm = normalize_line(orig)
            if norm not in unique_norm:
                unique_norm[norm] = True
                deduped.append(norm)
    print("原始：", orig)
    print("归一化：", norm)
    return deduped


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Deduplicate raw log file")
    parser.add_argument("-i", "--input", help="Input raw log file")
    parser.add_argument("-o", "--output", help="Output file for deduplicated logs")
    args = parser.parse_args()

    # 如果没有传参，则使用默认路径
    if not args.input or not args.output:
        # 获取当前脚本所在目录 → DNSLogIQ/src/preprocessing/
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent  # 回到项目根目录

        input_path = project_root / "data" / "raw_logs" / "demo.log"
        output_path = project_root / "data" / "processed_logs" / "step2_deduped.log"
    else:
        input_path = Path(args.input)
        output_path = Path(args.output)

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"输入路径: {input_path}")
    print(f"是否存在: {input_path.exists()}")
    print(f"输出路径: {output_path}")
    # 去重并写入文件
    deduped = deduplicate_logs(str(input_path))
    with output_path.open("w", encoding="utf-8") as f:
        for line in deduped:
            f.write(line + "\n")

    print(f"[Step2] 日志去重完成：{output_path}")
    print("[DEBUG] 去重后样本数：", len(deduped))
    print("[DEBUG] 样本预览（前5行）：")
    for line in deduped[:5]:
        print("  -", line)


if __name__ == "__main__":
    main()
