import sqlite3
from db import insert_account, get_all_accounts, DB_FILE
from crypto_utils import encrypt, decrypt

def add_account(data, cipher):
    site = input("Nhập tên trang web: ")
    username = input("Tên tài khoản: ")
    password = input("Mật khẩu: ")

    encrypted_username = encrypt(username, cipher)
    encrypted_password = encrypt(password, cipher)

    insert_account(site, encrypted_username, encrypted_password)
    print("Đã thêm tài khoản.")

def show_accounts(data, cipher):
    records = get_all_accounts()
    if not records:
        print("Không có tài khoản nào.")
        return

    for i, (site, encrypted_username, encrypted_password) in enumerate(records, 1):
        username = decrypt(encrypted_username, cipher)
        password = decrypt(encrypted_password, cipher)
        print(f"#{i} {site} | {username} : {password}")

def delete_account(data, cipher):
    site = input("Nhập tên website: ")
    username = input("Nhập tên tài khoản muốn xoá: ")

    encrypted_username = encrypt(username, cipher)

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM accounts WHERE site = ? AND username = ?", (site, encrypted_username))
        if c.rowcount > 0:
            conn.commit()
            print("Đã xoá tài khoản.")
        else:
            print("Không tìm thấy tài khoản.")

def edit_account(data, cipher):
    site = input("Nhập tên website cần sửa: ")
    username = input("Nhập tên tài khoản muốn sửa: ")

    encrypted_username = encrypt(username, cipher)

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, password FROM accounts WHERE site = ? AND username = ?", (site, encrypted_username))
        result = c.fetchone()

        if result:
            account_id, current_encrypted_password = result
            new_username = input("Tên mới (Enter để giữ nguyên): ")
            new_password = input("Mật khẩu mới (Enter để giữ nguyên): ")

            if new_username:
                encrypted_username = encrypt(new_username, cipher)
            if new_password:
                encrypted_password = encrypt(new_password, cipher)
            else:
                encrypted_password = current_encrypted_password

            c.execute("UPDATE accounts SET username = ?, password = ? WHERE id = ?",
                      (encrypted_username, encrypted_password, account_id))
            conn.commit()
            print("Đã cập nhật tài khoản.")
        else:
            print("Không tìm thấy tài khoản.")

def search_account(data, cipher):
    keyword = input("Nhập từ khoá tìm kiếm (website hoặc username): ").lower()
    found = False

    records = get_all_accounts()
    for site, encrypted_username, encrypted_password in records:
        username = decrypt(encrypted_username, cipher)
        password = decrypt(encrypted_password, cipher)

        if keyword in site.lower() or keyword in username.lower():
            print(f"{site} | {username} | {password}")
            found = True

    if not found:
        print("Không tìm thấy kết quả.")
