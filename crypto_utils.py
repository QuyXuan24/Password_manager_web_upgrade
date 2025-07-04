from cryptography.fernet import Fernet

KEY_FILE = "key.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def get_cipher():
    try:
        key = load_key()
    except FileNotFoundError:
        key = generate_key()
    return Fernet(key)

def encrypt(text, cipher):
    return cipher.encrypt(text.encode()).decode()

def decrypt(text, cipher):
    return cipher.decrypt(text.encode()).decode()