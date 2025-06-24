#!/usr/bin/env python3
"""
clustering_analysis.py
实现日志的 TF-IDF 向量化及 K-Means 聚类分析。
"""

import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

def load_texts(input_file):
    texts = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            texts.append(line.strip())
    return texts

def perform_clustering(texts, n_clusters=5):
    vectorizer = TfidfVectorizer(min_df=2, stop_words='english', ngram_range=(1,2))
    X = vectorizer.fit_transform(texts)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    labels = kmeans.labels_
    return labels, kmeans, vectorizer

def main():
    # …现有 argparse 代码
    texts = load_texts(args.input)
    print(f"Loaded {len(texts)} samples for clustering")    # ← 加这个
    labels, kmeans, vectorizer = perform_clustering(texts, n_clusters=args.n_clusters)
    print("Cluster labels:", labels)                        # ← 加这个

    # 评估一下 Silhouette Score
    X = vectorizer.transform(texts)
    score = silhouette_score(X, labels)
    print(f"Silhouette Score: {score:.4f}")                # ← 加这个

    # 输出每条日志及其簇号
    for idx, (txt, lab) in enumerate(zip(texts, labels)):
        print(f"{idx:3d} → cluster {lab} : {txt}")


if __name__ == "__main__":
    main()