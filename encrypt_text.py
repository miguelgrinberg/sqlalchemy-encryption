import os
import sys
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

encryption_key = os.environ['ENCRYPTION_KEY']
text_to_encrypt = sys.argv[1]

fernet = Fernet(encryption_key.encode())
encrypted = fernet.encrypt(text_to_encrypt.encode())

print(encrypted.decode())
