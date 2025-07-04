from flask import Flask, render_template, request, redirect, session, url_for
from db import init_db, get_all_accounts, insert_account
from crypto_utils import get_cipher, encrypt, decrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"
cipher = get_cipher()
init_db()

MASTER_PASSWORD = "123456"

# Trang chính chỉ để thêm tài khoản
@app.route("/")
def index():
    return render_template("index.html")

# Thêm tài khoản
@app.route("/them", methods=["POST"])
def add_account():
    site = request.form["site"]
    username = request.form["username"]
    password = request.form["password"]

    encrypted_username = encrypt(username, cipher)
    encrypted_password = encrypt(password, cipher)

    insert_account(site, encrypted_username, encrypted_password)
    return redirect("/")

# Xoá tài khoản
@app.route("/xoa", methods=["POST"])
def delete_account():
    site = request.form["site"]
    encrypted_username = request.form["username"]
    with sqlite3.connect("passwords.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM accounts WHERE site = ? AND username = ?", (site, encrypted_username))
        conn.commit()
    return redirect("/danhsach")

# Sửa tài khoản
@app.route("/sua", methods=["GET", "POST"])
def edit_account():
    if request.method == "GET":
        return render_template("edit.html",
                               site=request.args["site"],
                               username_plain=request.args["username"],
                               username_enc=request.args["username_enc"])

    site = request.form["site"]
    encrypted_old_username = request.form["old_username"]
    new_username = request.form["new_username"]
    new_password = request.form["new_password"]

    encrypted_new_username = encrypt(new_username, cipher)
    encrypted_new_password = encrypt(new_password, cipher)

    with sqlite3.connect("passwords.db") as conn:
        c = conn.cursor()
        c.execute("UPDATE accounts SET username = ?, password = ? WHERE site = ? AND username = ?",
                  (encrypted_new_username, encrypted_new_password, site, encrypted_old_username))
        conn.commit()

    return redirect("/danhsach")  # QUAY VỀ TRANG DANH SÁCH

# Trang nhập mật khẩu chính để xem danh sách
@app.route("/xacnhan", methods=["GET", "POST"])
def confirm_master_password():
    if request.method == "POST":
        if request.form["master_password"] == MASTER_PASSWORD:
            session["logged_in"] = True
            return redirect("/danhsach")
        else:
            return render_template("xacnhan.html", error="Sai mật khẩu chính.")
    return render_template("xacnhan.html")

# Trang xem danh sách tài khoản
@app.route("/danhsach")
def view_accounts():
    if not session.get("logged_in"):
        return redirect("/xacnhan")

    records = get_all_accounts()
    accounts = []
    for site, username_enc, password_enc in records:
        accounts.append({
            "site": site,
            "username_plain": decrypt(username_enc, cipher),
            "username_enc": username_enc,
            "password_plain": decrypt(password_enc, cipher)
        })
    return render_template("danhsach.html", accounts=accounts)

# Đăng xuất
@app.route("/dangxuat")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
