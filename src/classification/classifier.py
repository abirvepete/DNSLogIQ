#!/usr/bin/env python3
"""
Step 3: 模糊分类模块
对去重后的日志进行子类别 fuzzy match 分组
（在 PyCharm 中 Run File，并在 Run/Debug Configuration → Script parameters 填写 -i … -o … -t …）
"""

import re
import argparse
from pathlib import Path
from difflib import SequenceMatcher

# --------------------------------------------------------------------------------------------------
# 分类键提取：按冒号前关键字分类，比如 "dns:"、"inbound/tproxy:" 等
def extract_class_key(line: str) -> str:
    m = re.match(r'^\s*([^:\s]+):', line)
    return m.group(1) if m else "unknown"

# 文件名安全化：把 / [ ] 空格等非法字符替换成下划线
def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:\*\?"<>\|\[\]\s]+', '_', name).strip('_')

# --------------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Step3: 模糊分类")
    parser.add_argument("-i", "--input",      help="Step2 去重后日志文件路径")
    parser.add_argument("-o", "--output_dir", help="分类输出目录")
    parser.add_argument("-t", "--threshold",  type=float, default=0.6,
                        help="模糊去重阈值（两个样本相似度大于此即认为重复）")
    args = parser.parse_args()

    # —— 确定路径（可传参，也可使用默认项目结构） ——
    current_file   = Path(__file__).resolve()
    project_root   = current_file.parents[2]  # 父级回到 DNSLogIQ/
    input_path     = Path(args.input) \
                     if args.input else project_root / "data" / "processed_logs" / "step2_deduped.log"
    output_dir     = Path(args.output_dir) \
                     if args.output_dir else project_root / "data" / "classified_logs"
    threshold      = args.threshold

    print(f"输入文件：{input_path}")
    print(f"存在？  {input_path.exists()}")
    print(f"输出目录：{output_dir}")
    if not input_path.exists():
        print("❌ 输入文件找不到，退出。")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # —— 1. 读去重文件，按分类键分桶 ——
    buckets = {}
    for line in input_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        key = extract_class_key(line)
        buckets.setdefault(key, []).append(line)

    # —— 2. 对每个桶做 模糊去重 & 写文件 ——
    for key, lines in buckets.items():
        unique = []
        for ln in lines:
            # 如果与 already in unique 的任意一条相似度 > threshold，就认为重复
            if not any(SequenceMatcher(None, ln, ex).ratio() > threshold for ex in unique):
                unique.append(ln)

        safe_key = sanitize_filename(key)
        fout = output_dir / f"{safe_key}.log"
        fout.parent.mkdir(parents=True, exist_ok=True)
        fout.write_text("\n".join(unique), encoding="utf-8")

        print(f"[Step3] 类别 '{key}' → 共 {len(unique)} 条  写入  {fout.name}")

if __name__ == "__main__":
    main()