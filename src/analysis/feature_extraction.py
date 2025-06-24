#!/usr/bin/env python3
import argparse

def prepare_samples_for_clustering(input_file: str, output_file: str):
    with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
        for line in f_in:
            # 这里简单地将归一化的文本全部小写写入
            text = line.strip().lower()
            f_out.write(text + "\n")
    print(f"Clustering samples saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare samples for clustering analysis")
    parser.add_argument("--input", required=True, help="Path to input deduped log file")
    parser.add_argument("--output", required=True, help="Path to output clustering samples file")
    args = parser.parse_args()
    prepare_samples_for_clustering(args.input, args.output)