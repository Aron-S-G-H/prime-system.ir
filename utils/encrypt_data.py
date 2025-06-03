from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import uuid


SECRET_KEY = b'Sixteen byte key'  # 16 bytes
IV = b'Sixteen byte ivv'  # 16 bytes


def encrypt_data(data: dict) -> str:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    plaintext = "&".join([f"{key}={value}" for key, value in data.items()])
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.urlsafe_b64encode(ciphertext).decode('utf-8')


def is_valid_uuid(value: str) -> bool:
    try:
        uuid_obj = uuid.UUID(value, version=4)  # بررسی نسخه 4 UUID
        return str(uuid_obj) == value
    except ValueError:
        return False
