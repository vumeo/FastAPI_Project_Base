from urllib.parse import urlparse, quote_plus

from pymongo import MongoClient

from utils.singleton import SingletonMeta
from utils.crypto import decrypt


def _normalize_url(url: str, encrypt_key: str = None) -> str:
    url = urlparse(url)
    username = quote_plus(url.username)
    password = url.password
    if encrypt_key:
        password = decrypt(password, encrypt_key)

    password = quote_plus(password)
    hostname = url.hostname
    port = url.port
    db_name = url.path[1:]

    if username and password:
        db_url = f'mongodb://{username}:{password}@{hostname}:{port}/{db_name}'
    else:
        db_url = f'mongodb://{hostname}:{port}/{db_name}'

    if url.query:
        db_url += f'?{url.query}'

    return db_url


class MongoDBClient(metaclass=SingletonMeta):
    def __init__(
            self,
            url: str,
            db_name: str,
            encrypt_key: str = None,
            max_pool_size: int = 100,
            min_pool_size: int = 5
    ):
        self.url = _normalize_url(url, encrypt_key)
        self.client = MongoClient(self.url, maxPoolSize=max_pool_size, minPoolSize=min_pool_size)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close(self):
        self.client.close()