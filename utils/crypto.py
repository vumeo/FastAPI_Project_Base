import re
import random
import string

from cryptography.fernet import Fernet
from passlib.context import CryptContext


def generate_key() -> str:
    key = Fernet.generate_key().decode().replace('@', '')
    key = key.replace(':', '')
    return key

def encrypt(data: str, key: str) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def decrypt(encrypt_data: str, key: str) -> str:
    try:
        f = Fernet(key)
        return f.decrypt(encrypt_data.encode()).decode()
    except Exception as e:
        return encrypt_data


def hash_data(data: str, salt: str) -> str:
    data_with_salt = f'{data}_{salt}'
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return context.hash(data_with_salt)


def verify_data(data: str, salt: str, hashed_data: str) -> bool:
    data_with_salt = f'{data}_{salt}'
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return context.verify(data_with_salt, hashed_data)


def is_strength_password(password: str) -> bool:
    pattern = r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})'
    regex = re.compile(pattern)
    return re.search(regex, password)


def generate_password(length: int = 4):
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%"

    password = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(special_characters),
    ]

    all_characters = lowercase_letters + uppercase_letters + digits + special_characters
    password += random.sample(all_characters, length)
    random.shuffle(password)
    return ''.join(password)