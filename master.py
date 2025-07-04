import hashlib

def save_master_password():
    password = input("Tạo mật khẩu chính: ")
    hashed = hashlib.sha256(password.encode()).hexdigest()

    with open("master.key", "w") as f:
        f.write(hashed)

    print("✅ Mật khẩu chính đã được lưu.")

if __name__ == "__main__":
    save_master_password()