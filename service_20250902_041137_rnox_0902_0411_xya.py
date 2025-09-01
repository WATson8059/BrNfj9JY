# 代码生成时间: 2025-09-02 04:11:37
# folder_structure Organizer.py
# 该脚本用于整理文件夹结构。

from os import path, listdir, mkdir
from os import walk as os_walk
from shutil import move
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def organize_folder_structure(source_folder, destination_folder, file_extension=None):
    """
    整理指定文件夹中文件的结构。
    
    参数:
    source_folder (str): 源文件夹路径
    destination_folder (str): 目标文件夹路径
    file_extension (str, optional): 需要整理的文件扩展名，默认为None，即整理所有文件
    """
    try:
        # 确保目标文件夹存在，不存在则创建
        if not path.exists(destination_folder):
            mkdir(destination_folder)
            logging.info(f'目标文件夹 {destination_folder} 已创建。')
        
        # 遍历源文件夹中的所有文件和子文件夹
        for root, dirs, files in os_walk(source_folder):
            for file in files:
                # 检查文件扩展名是否匹配
                if file_extension is None or file.endswith(file_extension):
                    source_file_path = path.join(root, file)
                    relative_path = path.relpath(root, source_folder)
                    
                    # 创建目标文件夹结构
                    target_folder = path.join(destination_folder, relative_path)
                    if not path.exists(target_folder):
                        mkdir(target_folder)
                        logging.info(f'目标文件夹 {target_folder} 已创建。')
                    
                    # 移动文件到目标位置
                    target_file_path = path.join(target_folder, file)
                    move(source_file_path, target_file_path)
                    logging.info(f'文件 {file} 已移动到 {target_file_path}')
    except Exception as e:
        logging.error(f'发生错误：{e}')
        raise

if __name__ == '__main__':
    # 示例用法
    source_folder = '/path/to/source/folder'
    destination_folder = '/path/to/destination/folder'
    file_extension = '.txt'  # 可选，只整理.txt文件
    organize_folder_structure(source_folder, destination_folder, file_extension)