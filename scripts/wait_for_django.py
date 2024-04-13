import time

import requests
from environs import Env

env = Env()
env.read_env()


def wait_for_django_to_come_up():
    deadline = time.time() + 120
    while time.time() < deadline:
        try:
            url = f'{env.str("DJANGO_API_HOST")}/api/v1/docs/'
            return requests.get(url, verify=not env.bool('DJANGO_DEBUG'))
        except requests.ConnectionError:
            time.sleep(0.5)
    raise Exception('Django never came up')


if __name__ == '__main__':
    wait_for_django_to_come_up()
