import requests
from time import time
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


if __name__ == '__main__':
    sync()

