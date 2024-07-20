"""
Задание №7
� Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
� Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
� Массив должен быть заполнен случайными целыми числами
от 1 до 100.
� При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
� В каждом решении нужно вывести время выполнения
вычислений.
"""

import asyncio
import multiprocessing
from multiprocessing import Process
import threading
import time
import random
import numpy as np

total_sum = 0


def create_list(count_stream):
    list_num = []
    for _ in range(1, 1000001):
        list_num.append(random.randint(1, 100))
    return np.array_split(list_num, count_stream)


def sum_number(num):
    global total_sum
    sum_num = sum(num)
    total_sum += sum_num


threads = []
start_time = time.time()

count_stream = 4
list_number = create_list(count_stream)

# Многопоточное вычисление
if __name__ == '__main__':
    for i in list_number:
        thread = threading.Thread(target=sum_number, args=[i])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Сумма элементов при Многопоточном вычислении = {total_sum}. Время затрачено: {time.time() - start_time:.5f} секунд.')