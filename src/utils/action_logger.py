import logging
import sys
from functools import wraps
from pathlib import Path
import time
from src.utils.common_logger import setup_logger

def setup_action_logger(log_dir="data/action_logs"):
    """
    初始化操作日志系统
    :param log_dir: 日志存储目录
    """
    return setup_logger("action_logger", log_dir=log_dir)

# 全局日志记录器
ACTION_LOGGER = setup_action_logger()

def log_action(func):
    """
    自动记录操作动作的装饰器，使用函数名作为 action 标识
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取当前函数名称
        action_name = func.__name__
        
        # 重定向标准输出
        class PrintToLogger:
            def write(self, buf):
                for line in buf.rstrip().splitlines():
                    ACTION_LOGGER.info(f"{line}", extra={'action': action_name})

        # 备份原始 stdout 并替换为我们的 logger
        old_stdout = sys.stdout
        sys.stdout = PrintToLogger()
        
        try:
            result = func(*args, **kwargs)
            ACTION_LOGGER.info(f"执行结果: {result}", extra={'action': action_name})
            return result
        finally:
            # 恢复原始 stdout
            sys.stdout = old_stdout

    return wrapper