import os
from urllib.parse import urlparse

from aioredis import Redis

from utils.singleton import SingletonMeta
from utils.crypto import decrypt


def _parse_url(url: str, encrypt_key: str = None) -> dict:
    url = urlparse(url)
    port = int(url.port or 6379)
    db = int(url.path[1:] or 0)
    data = {
        'host': url.hostname,
        'port': port,
        'db': db,
        'scheme': url.scheme
    }
    if url.password:
        password = decrypt(url.password, encrypt_key) if encrypt_key else url.password
        data['password'] = password

    query = url.query
    if query:
        query = dict(q.split('=') for q in query.split('&'))
        if query.get('ssl'):
            data['ssl'] = True
    return


class RedisClient(metaclass=SingletonMeta):
    def __init__(
            self,
            url: str,
            db: str,
            encrypt_key: str = None
    ):
        self.url = os.path.join(url, db)
        redis_config = _parse_url(self.url, encrypt_key)
        self.client = Redis(
            host=redis_config.get('host'),
            port=redis_config.get('port'),
            db=redis_config.get('db'),
            password=redis_config.get('password'),
            decode_responses=True
        )
