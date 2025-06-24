from dataclasses import dataclass
from datetime import datetime

@dataclass
class BaseTable:
    id: str               # 信息唯一标识，由内部生成
    timestamp: datetime   # 日志事件时间
    level: str            # 日志级别，例如 INFO、DEBUG
    category: str         # 主要类别（例如 dns）
    raw: str              # 原始日志（去除 ts、level 部分）
    subcategory: str      # 次要类别（如 dns cached）；为空的归入 unmatched