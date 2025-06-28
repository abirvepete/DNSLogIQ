import cProfile
from pathlib import Path

# 确保 snakeviz 存放目录存在
OUTPUT_DIR = Path("test/action_logs/snakeviz")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def performance_monitor(func):
    """
    装饰器：为被装饰函数生成 SnakeViz 可读的 .prof 文件。
    文件自动保存在 test/action_logs/snakeviz/ 目录下，文件名基于函数名自动生成。
    """
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()

        # 根据函数名生成文件路径
        func_name = func.__name__
        filename = OUTPUT_DIR / f"{func_name}.prof"

        # 保存性能数据到文件
        profiler.dump_stats(str(filename))

        return result
    return wrapper
