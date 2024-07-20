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
import time
import random
import numpy as np

total_sum = 0


def create_list(count_stream):
    list_num = []
    for _ in range(1, 1000001):
        list_num.append(random.randint(1, 100))
    return np.array_split(list_num, count_stream)


async def sum_number(num):
    global total_sum
    sum_num = sum(num)
    total_sum += sum_num


threads = []
start_time = time.time()

count_stream = 4


# Асинхронное вычисление
async def main():
    tasks = []
    list_task = create_list(count_stream)
    for num in list_task:
        task = asyncio.ensure_future(sum_number(num))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    asyncio.run(main())

    print(f'Сумма элементов при Многопоточном вычислении = {total_sum}. Время затрачено: {time.time() - start_time:.5f} секунд.')
