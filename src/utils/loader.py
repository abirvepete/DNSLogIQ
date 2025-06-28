# src/utils/loader.py
"""
在直接运行脚本或 module 方式运行时，
都能自动把 src/ 加入 sys.path，
确保后续 from preprocessing/... 能正确 import。
"""
import sys
from pathlib import Path

def init_paths():
    # __file__ → .../src/utils/loader.py
    this = Path(__file__).resolve()
    # project_root = src/ 上两级
    project_root = this.parents[2]
    # 将 src/ 目录插到 sys.path[0]
    src_dir = project_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))