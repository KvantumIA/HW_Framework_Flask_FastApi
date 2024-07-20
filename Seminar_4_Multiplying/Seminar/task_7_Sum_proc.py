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

import multiprocessing
from multiprocessing import Process
import time
import random
import numpy as np

total_sum = multiprocessing.Value('i', 0)


def create_list(count_stream):
    list_num = []
    for _ in range(1, 1000001):
        list_num.append(random.randint(1, 100))
    return np.array_split(list_num, count_stream)


def sum_number(num, total_sum):
    sum_num = sum(num)
    with total_sum.get_lock():
        total_sum.value += sum_num


start_time = time.time()

count_stream = 4
list_number = create_list(count_stream)

# Многопроцессорное вычисление
processes = []

if __name__ == '__main__':
    for j in list_number:
        process = Process(target=sum_number, args=(j, total_sum))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(
        f'Сумма элементов при Многопроцессорном вычислении = {total_sum.value:_}. Время затрачено: {time.time() - start_time:.5f} секунд.')

