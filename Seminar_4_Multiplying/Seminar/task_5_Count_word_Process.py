"""
Задание №5
� Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
� Используйте процессы.
"""
import multiprocessing
from multiprocessing import Process
from pathlib import Path
import os
count = multiprocessing.Value('i', 0)


def process_file(file_path, count):
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
        print(f'{f.name} содержит {len(contents.split())} слов')
        with count.get_lock():
            count.value += len(contents.split())


def path_lib():
    path_list = []
    dir_path = Path('file')
    file_paths = os.walk(dir_path)
    for root, dirs, files in file_paths:
        for file in files:
            # Получаем полный путь к файлу
            full_path = Path(root) / file
            path_list.append(full_path)
    return path_list


processes = []

if __name__ == '__main__':
    for i in path_lib():
        process = Process(target=process_file, args=(i, count))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'Общее количество слов = {count.value:_}')
