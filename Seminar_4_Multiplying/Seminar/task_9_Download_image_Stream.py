"""
Задание №9
� Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
� Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
image1.jpg
� Программа должна использовать многопоточный, многопроцессорный и
асинхронный подходы.
� Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
� Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы.
"""
import argparse

import requests
import threading
import time


default_urls = ['https://cdn.pixabay.com/photo/2024/04/21/14/13/pelican-8710717_640.jpg',
        'https://cdn.pixabay.com/photo/2024/06/18/13/16/oceans-view-8838022_640.jpg',
        'https://cdn.pixabay.com/photo/2024/02/09/13/26/ai-generated-8563109_640.jpg',
        'https://cdn.pixabay.com/photo/2017/08/01/11/38/sea-2564601_640.jpg',
        'https://cdn.pixabay.com/photo/2024/06/29/06/30/forest-8860740_640.png'
        ]


def download(url, path):
    response = requests.get(url)
    filename = f'{path}/' + url.split('?')[0].split('/')[-1]
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


threads = []
start_time = time.time()

if __name__ == '__main__':
    path = 'image'
    parser = argparse.ArgumentParser(description="Скачивание изображений из URLs")
    parser.add_argument('urls', nargs='*', help='Список изображений с URLs')
    parser.add_argument('--save_dir', default='image',
                        help='Папка для сохранения изображений')

    args = parser.parse_args()
    urls = args.urls if args.urls else default_urls
    path = args.save_dir

    for url in urls:
        thread = threading.Thread(target=download, args=[url, path])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Скачивание завершено. Общее время выполнения - {time.time() - start_time:.2f}')