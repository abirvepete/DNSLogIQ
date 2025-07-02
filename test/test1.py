from pathlib import Path
import threading
import hashlib
from concurrent.futures import ThreadPoolExecutor


# 定义相似度阈值
threshold = 0.95

# 用于控制文件写入的锁
write_lock = threading.Lock()

def set_globals():
    global root_dir
    root_dir = Path(__file__).resolve().parents[1]
    global lens_set
    lens_set  = set()

def get_line_hash(line: str):
    """计算每行的 MD5 哈希值"""
    return hashlib.md5(line.encode('utf-8')).hexdigest()

def read_log_file(filepath: Path, executor: ThreadPoolExecutor):
    """读取日志文件并将每行数据的长度添加到 lens_set 中"""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            tmp = line.strip().split(" ")
            lens_set.add(len(tmp))
            #executor.submit(write_to_buffer, tmp, len(tmp))
    print("现在开始进入多线程环节\n")
    threading_all_buffers()

def write_to_buffer(line: list, lens: int):
    """将处理后的每行数据写入到对应的缓冲文件中"""
    buffer_path = root_dir / "data" / "processed_logs" / "buffer" / f"buffer{lens}.log"
    with write_lock:
        with open(buffer_path, 'a', encoding='utf-8') as f:
            f.write(' '.join(line) + '\n')


def threading_all_buffers():
    """多线程独立分析所有的 buffer 文件"""
    print("开始多线程")
    with ThreadPoolExecutor(max_workers=len(lens_set)) as executor:
        executor.map(overwrite_file_with_no_similar_lines, lens_set)
        print("启动")
    print("所有 buffer 文件处理完毕")

def overwrite_file_with_no_similar_lines(i: int):
    """
    删除大量重复日志（相似度高的行），
    优化方法：通过哈希值快速去重，减少相似度计算的次数
    """
    operated_file = root_dir / "data" / "processed_logs" / "buffer" / f"buffer{i}.log"
    print(f"正在处理buffer{i}文件\n")

    unique_lines = []
    seen_hashes = set()

    # 逐行读取文件并去重
    with open(operated_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and get_line_hash(line) not in seen_hashes:
                seen_hashes.add(get_line_hash(line))
                unique_lines.append(line)

    # 批量写入优化：将所有不重复的行缓存到内存，最后一次性写入文件
    with open(operated_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_lines) + '\n')

    print(f"buffer{i}文件处理完毕，删除了{len(f.readlines()) - len(unique_lines)}行\n")

def sort_lines(filepath: Path, i: int):
    """
    计算位置相似度并去重位置完全相同的信息
    """
    pass

# 示例用法

def main():  # 使用通用模块获取项目根目录，不同的级别需要修改parent级别
    set_globals()
    input_path = root_dir / "data" / "processed_logs" / "nonprefix.log"
    # 创建线程池，最大线程数设为 4（可以根据需要调整）
    with ThreadPoolExecutor(max_workers=4) as executor:
        read_log_file(input_path, executor)

if __name__ == '__main__':
    main()
