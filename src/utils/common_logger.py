import logging
from pathlib import Path

def setup_logger(logger_name: str, log_dir="test/action_logs"):
    """
    创建并配置一个通用日志记录器
    :param logger_name: 日志记录器名称（即代码模块名）
    :param log_dir: 日志存储目录
    :return: 配置好的日志记录器
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)  # 创建日志目录

    # 获取或创建日志记录器
    logger = logging.getLogger(logger_name)
    
    # 如果已经存在处理器，直接返回
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # 创建文件处理器（统一写入 project_logs.log）
    handler = logging.FileHandler(log_path / "project_logs.log", encoding='utf-8')
    handler.setLevel(logging.INFO)

    # 设置日志格式，包含模块名
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(action)s - %(message)s')
    handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(handler)
    return logger