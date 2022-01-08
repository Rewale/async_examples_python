from collections import namedtuple
import time
import asyncio
from concurrent.futures import FIRST_COMPLETED
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    async with aiohttp.ClientSession() as session:
        async with session.get(service.url) as response:
            json_response = await response.json()
            ip = json_response[service.ip_attr]

    response.close()
    return '{} finished with result: {}, took: {:.2f} seconds'.format(
        service.name, ip, time.time() - start)


async def asynchronous():
    tasks = [asyncio.create_task(fetch_ip(service)) for service in SERVICES]
    done, pending = await asyncio.wait(
        tasks, return_when=FIRST_COMPLETED)

    print(len(done))
    print(done.pop().result())


asyncio.run(asynchronous())
