import re
from pathlib import Path
# 引入新的通用模块
from src.utils.action_logger import log_action
from src.utils.performance_monitor import performance_monitor

# 定义全局路径
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # 项目根目录


# ========== 日志清洗函数 ==========
def clean_prefix_of_line(log_line: str) -> list:
    """
    使用' '分割日志信息内容
    截掉时间戳等前缀，保留 level 和后续内容
    :param log_line:
    :return: 清洗后的日志列表
    """
    parts = log_line.split(' ')

    if len(parts) > 5:
        # 检查第4个字段是否包含 '['，第5个是否包含 ']'
        if re.search(r"\[", parts[4]) and re.search(r"\]", parts[5]):
           del parts[4:6]  # 删除方括号及其中的内容字段
        return parts[3:]
    else:
        print(f"无法处理日志行：{log_line}")
        exit(1)

def write_cleaned_logs(input_path, output_path):
    """
    读取原始日志文件并清洗后写入新文件

    :param input_path: 输入日志文件路径
    :param output_path: 输出清洗后日志文件路径
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
                open(output_path, 'w', encoding='utf-8') as outfile:

            # 打印调试信息
            print(f"开始处理: {input_path.resolve()}")
            print(f"输出到: {output_path.resolve()}")

            # 检查文件是否存在
            if not input_path.exists():
                print(f"错误：输入文件 {input_path} 不存在")
                exit(1)


            # 使用缓冲区批量写入
            buffer = []
            BUFFER_SIZE = 100  # 根据实际情况调整这个值

            for line_number, line in enumerate(infile, start=1):
                # 清洗日志内容
                cleaned = clean_prefix_of_line(line)

                # 跳过空行
                if not cleaned:
                    continue

                # 添加到缓冲区
                buffer.append(' '.join(cleaned) + '\n')

                # 批量写入
                if len(buffer) >= BUFFER_SIZE:
                    outfile.writelines(buffer)
                    buffer.clear()

            # 写入剩余内容
            if buffer:
                outfile.writelines(buffer)

    except FileNotFoundError as e:
        print(f"文件未找到错误: {e}")
    except PermissionError as e:
        print(f"权限错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    else:
        print(f"日志清洗完成&去头了{line_number}条日志")
    finally:
        print("写入操作结束")


# ========== 主程序入口 ==========
@log_action
@performance_monitor
def main():
    """
    后续优化：加入try进行错误异常控制
    或者加入完全独立的错误检查
    """
    root_dir = Path(__file__).resolve().parents[2]
    print(root_dir)
    original_file = root_dir /'data'/'raw_logs'/'demo.log'
    print(f"找到 {original_file} 原始日志文件")
    del_prefix_file = root_dir  /'data'/'processed_logs'/'nonprefix.log'
    write_cleaned_logs(original_file, del_prefix_file)


if __name__ == '__main__':
    main()

