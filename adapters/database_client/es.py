import os

import elasticsearch

from utils.singleton import SingletonMeta
from utils.crypto import decrypt


class ElasticsearchClient(metaclass=SingletonMeta):
    def __init__(
            self,
            host: str,
            username: str,
            password: str,
            encrypt_key: str = None,
            cert_path: str = None
    ):
        password = decrypt(password, encrypt_key) if encrypt_key else password
        version = int(elasticsearch.__version__[0])
        if version == 7:
            self.client = elasticsearch.Elasticsearch(
                host,
                http_auth=(username, password),
                request_timeout=180,
                max_retries=10
            )
        else:
            if not cert_path:
                raise ValueError('cert_path is required for elasticsearch version 8')
            if not os.path.exists(cert_path):
                raise ValueError(f'cert_path {cert_path} does not exist')

            self.client = elasticsearch.Elasticsearch(
                host,
                basic_auth=(username, password),
                ca_certs=cert_path,
                verify_certs=True,
                request_timeout=180,
                max_retries=10
            )

    def get_client(self) -> elasticsearch.Elasticsearch:
        return self.client

    def close(self):
        self.client.close()