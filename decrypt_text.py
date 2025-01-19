import os
import sys
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

encrypted_text = sys.argv[1]

fernet = Fernet(os.environ['ENCRYPTION_KEY'].encode())
text = fernet.decrypt(encrypted_text.encode())

print(text.decode())
