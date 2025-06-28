#!/usr/bin/env python3
"""
Step3-v3: 按词组匹配度 & 顺序匹配度对每个桶内日志排序

调用方式（均在项目根 DNSLogIQ/ 下）：
1) PyCharm Run File：直接运行此脚本，Script parameters 可填：
     -i data/processed_logs/step2_deduped.log -o data/classified_sorted_v3
2) 脚本调用：
     python src/classification/classifier_v3.py \
       -i data/processed_logs/step2_deduped.log \
       -o data/classified_sorted_v3
3) 模块模式：
     python -m src.classification.classifier_v3 \
       -i data/processed_logs/step2_deduped.log \
       -o data/classified_sorted_v3
"""

# —— 智能加载 src/ 到 sys.path, 保证无论在哪运行都能 import 本包内部模块 ——
import sys
from pathlib import Path

_this = Path(__file__).resolve()
# project_root = DNSLogIQ/src/classification/../../..
_project_root = _this.parents[2]
_src_dir = _project_root / "src"
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))

# —— 业务逻辑 ——
import argparse, re
from collections import defaultdict
from difflib import SequenceMatcher

IP_PORT_RE = re.compile(r'^\d+\.\d+\.\d+\.\d+:\d+$')

def tokenize(line: str):
    # 去掉前置时间/级别/连接码
    body = re.sub(
        r'^\s*\S+\s+\d{4}-\d{2}-\d{2}\s+\S+\s+\[[^\]]+\]\s*',
        '', line
    ).strip()
    return body.split()

def phrase_match(tokens1, tokens2):
    # 共同 token 数 / min(长度)
    s1, s2 = set(tokens1), set(tokens2)
    if not s1 or not s2:
        return 0.0
    common = s1 & s2
    return len(common) / min(len(tokens1), len(tokens2))

def order_match(tokens1, tokens2):
    return SequenceMatcher(None, tokens1, tokens2).ratio()
    best, best_sum = None, -1
    for i, si in enumerate(seqs):
        total = sum(
            phrase_match(si, sj) + order_match(si, sj)
            for j, sj in enumerate(seqs) if j != i
        )
        if total > best_sum:
            best_sum, best = total, i
    return best

def main():
    # 获取项目根目录
    _this = Path(__file__).resolve()
    project_root = _this.parents[2]

    # 定义默认路径
    DEFAULT_INPUT = project_root / "data" / "processed_logs" / "step2_deduped.log"
    DEFAULT_OUTPUT_DIR = project_root / "data" / "classified_sorted_v3"

    parser = argparse.ArgumentParser(description="Step3-v3：相似度排序")
    parser.add_argument("-i","--input",     default=DEFAULT_INPUT,
                        help="step2 去重后日志")
    parser.add_argument("-o","--output_dir",
                        default=DEFAULT_OUTPUT_DIR,
                        help="排序后输出目录")
    args = parser.parse_args()

    inp  = Path(args.input)
    outd = Path(args.output_dir); outd.mkdir(parents=True, exist_ok=True)

    print(f"输入路径: {inp.resolve()}")
    print(f"是否存在: {inp.exists()}")
    print(f"输出目录: {outd.resolve()}")

    if not inp.exists():
        print("❌ 输入文件不存在：", inp)
        return

    # 1. 分桶：按第一个 token.split("/")[0]
    buckets = defaultdict(list)
    for ln in inp.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln: continue
        toks = tokenize(ln)
        key = toks[0].split("/")[0]
        buckets[key].append((ln, toks))

    # 2. 每桶 medoid + 排序 + 输出
    for key, items in buckets.items():
        logs, seqs = zip(*items)
        medoid_idx = find_medoid(seqs)
        medoid_log = logs[medoid_idx]
        medoid_seq = seqs[medoid_idx]

        scored = []
        for ln, toks in items:
            p = phrase_match(medoid_seq, toks)
            o = order_match(medoid_seq, toks)
            scored.append((p, o, ln))

        scored.sort(key=lambda x: (x[0], x[1]), reverse=True)

        outf = outd / f"{key}.log"
        with outf.open("w", encoding="utf-8") as f:
            f.write(f"# Medoid: {medoid_log}\n")
            f.write(f"# Columns: phrase_match, order_match, original_log\n")
            for p, o, ln in scored:
                f.write(f"{p:.3f}\t{o:.3f}\t{ln}\n")

        print(f"[{key}] Medoid idx={medoid_idx}, wrote {len(scored)} lines to {outf}")

if __name__=="__main__":
    main()