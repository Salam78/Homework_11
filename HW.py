from tkinter import Tk, Label, Entry, Button
import concurrent
import time
import random
import threading
import multiprocessing
import asyncio
import requests
import aiohttp
import time
import aiofiles

url = "https://picsum.photos/320/240/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                  'Chrome/102.0.0.0 Safari/537.36'
}


def sync_download_one_image():
    response = requests.get(url=url, headers=headers)
    with open(f"temp/image{random.randint(1, 10000000)}.jpg", "wb") as opened_file:
        opened_file.write(response.content)


def sync_download_mass_image():
    start_time = time.perf_counter()
    for i in range(1, 10 + 1):
        sync_download_one_image()

    print(f'Задача закончила работу за {round(time.perf_counter() - start_time, 5)}')


def threading_download_mass_image():
    start_time = time.perf_counter()

    thread = threading.Thread(target=sync_download_one_image, args=(), kwargs={})
    thread.start()

    for i in range(1, 9 + 1):
        thread_list = []
    for i in range(1, 9 + 1):
        thread_list.append(threading.Thread(target=sync_download_one_image, args=(), kwargs={}))
    for thread in thread_list:
        thread.start()

    print(f'Задача закончила работу за {round(time.perf_counter() - start_time, 5)}')


def processing_download_mass_image():
    start_time = time.perf_counter()
    #
    process = multiprocessing.Process(target=sync_download_one_image, args=(), kwargs={})
    process.start()

    for i in range(1, 9 + 1):
        process_list = []
    for i in range(1, 9 + 1):
        process_list.append(multiprocessing.Process(target=sync_download_one_image, args=(), kwargs={}))
    for process in process_list:
        process.start()

    print(f'Задача закончила работу за {round(time.perf_counter() - start_time, 5)}')


async def async_download_one_image():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            data = await response.read()
            with open(f"temp/image{random.randint(1, 10000000)}.jpg", "wb") as opened_file:
                opened_file.write(data)


def async_task():
    start_time = time.perf_counter()

    async def async_task_inline():
        await asyncio.gather(*[async_download_one_image() for _ in range(1, 10 + 1)])

    asyncio.run(async_task_inline())

    print(f'Задача закончила работу за {round(time.perf_counter() - start_time, 5)}')

if __name__ == '__main__':
    sync_download_mass_image()
    # threading_download_mass_image()
    # processing_download_mass_image()
    # async_task()

window = Tk()
window.title("Загрузчик картинок")
window.geometry('300x150')

# Кнопка для синхронной загрузки
save_button = Button(window, text="Синхронная загрузка", command=sync_download_mass_image)
save_button.pack()

# Кнопка для многопоточной загрузки
save_button = Button(window, text="Многопоточная загрузка", command=threading_download_mass_image)
save_button.pack()

# Кнопка для мультипроцессорной загрузки
save_button = Button(window, text="Мультипроцессорная загрузка", command=processing_download_mass_image)
save_button.pack()

# Кнопка для асинхронной загрузки
save_button = Button(window, text="Асинхронная загрузка", command=lambda: async_task())
save_button.pack()

window.mainloop()
input("press any key to close window")
