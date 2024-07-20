"""
Задание №4
� Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
� Используйте потоки.
"""

import requests
import threading
from pathlib import Path
import os
count = 0


def process_file(file_path):
    global count
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
        print(f'{f.name} содержит {len(contents.split())} слов')
        count += len(contents.split())


def path_lib():
    path_list = []
    dir_path = Path('file')
    file_paths = os.walk(dir_path)
    for root, dirs, files in file_paths:
        for file in files:
            path_list.append(Path(root) / file)
    return path_list


threads = []
if __name__ == '__main__':
    for i in path_lib():
        thread = threading.Thread(target=process_file, args=[i])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Общее количество слов = {count}')
