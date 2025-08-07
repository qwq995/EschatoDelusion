import os
import argparse
import sys
import re

def get_max_chapter_number(directory):
    """获取目录中已存在的最大章节号和位数"""
    max_chapter = 0
    max_digits = 0
    pattern = re.compile(r"第(\d+).*?\.txt$")
    
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            chapter_num = int(match.group(1))
            if chapter_num > max_chapter:
                max_chapter = chapter_num
            digits = len(match.group(1))
            if digits > max_digits:
                max_digits = digits
    return max_chapter, max_digits

def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='自动生成章节文件')
    parser.add_argument('directory', type=str, help='相对路径（将在当前工作目录下创建）')
    parser.add_argument('num_chapters', type=int, help='章节数目（1-1000）')
    parser.add_argument('base_string', type=str, help='文件名基础字符串')
    
    args = parser.parse_args()
    
    # 验证章节数目
    if not 1 <= args.num_chapters <= 1000:
        print("错误：章节数目必须在1-1000之间", file=sys.stderr)
        sys.exit(1)
    
    # 创建目标目录（如果不存在）
    target_dir = os.path.join(os.getcwd(), args.directory)
    os.makedirs(target_dir, exist_ok=True)
    
    # 确定所需数字位数（至少2位，超过99章用3位）
    required_digits = 3 if args.num_chapters > 99 else 2
    
    # 获取目录中已有的最大章节号和位数
    existing_max, existing_digits = get_max_chapter_number(target_dir)
    final_digits = max(required_digits, existing_digits)
    
    # 重命名位数不足的已有文件
    for filename in os.listdir(target_dir):
        match = re.match(r"第(\d+)(.*?\.txt)$", filename)
        if match:
            chapter_num = match.group(1)
            suffix = match.group(2)
            if len(chapter_num) < final_digits:
                new_num = chapter_num.zfill(final_digits)
                new_filename = f"第{new_num}{suffix}"
                old_path = os.path.join(target_dir, filename)
                new_path = os.path.join(target_dir, new_filename)
                os.rename(old_path, new_path)
                print(f"重命名对齐: {filename} -> {new_filename}")
    
    # 生成章节文件
    for i in range(1, args.num_chapters + 1):
        # 格式化章节数字
        formatted_num = str(i).zfill(final_digits)
        filename = f"第{formatted_num}{args.base_string}--.txt"
        filepath = os.path.join(target_dir, filename)
        
        # 仅当文件不存在时创建空文件
        if not os.path.exists(filepath):
            open(filepath, 'w').close()
            print(f"创建文件: {filename}")
        else:
            print(f"文件已存在，跳过: {filename}")

if __name__ == "__main__":
    main()