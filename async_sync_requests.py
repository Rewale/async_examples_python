from time import time

import requests
from requests import Response

url = 'https://loremflickr.com/320/240'
base_dir = 'IMAGES/'


def get_file(url: str) -> Response:
    response = requests.get(url, allow_redirects=True)
    return response


def write_file(response: Response):
    filename = response.url.split('/')[-1]
    with open(base_dir+filename, 'wb') as file:
        file.write(response.content)


def sync():
    t0 = time()

    for i in range(0, 10):
        write_file(get_file(url))

    print(f'{time() - t0}')


import asyncio
import aiohttp


def write_image(data: bytes):
    filename = f'IMAGES/file-{int(time() * 1000)}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url: str, session: aiohttp.ClientSession):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main_async():
    tasks = []

    async with aiohttp.ClientSession() as session:
        # Создаем десять задач
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        # wait
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    sync()
    t0 = time()
    asyncio.run(main_async())
    print(time() - t0)

