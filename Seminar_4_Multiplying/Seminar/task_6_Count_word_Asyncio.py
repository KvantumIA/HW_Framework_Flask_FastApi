"""
Задание №6
� Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
� Используйте асинхронный подход.
"""
import asyncio
from pathlib import Path
import os
count = 0


async def process_file(file_path):
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
            full_path = Path(root) / file
            path_list.append(full_path)
    return path_list


async def main():
    tasks = []
    path_list = path_lib()
    for path in path_list:
        task = asyncio.ensure_future(process_file(path))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    print(f'Общее количество слов = {count}')
