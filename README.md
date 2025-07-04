# 🔐 Trình Quản Lý Mật Khẩu Đơn Giản

Đây là một ứng dụng web đơn giản cho phép bạn quản lý các tài khoản đăng nhập vào các trang web khác nhau một cách an toàn, bằng cách mã hoá thông tin với **Fernet Encryption** và lưu trữ trong **SQLite**.

---

## 🧰 Tính năng

- ✅ Thêm tài khoản với website, username, password
- ✅ Mã hoá tài khoản và mật khẩu bằng Fernet
- ✅ Hiển thị danh sách tài khoản (sau khi nhập mật khẩu chính)
- ✅ Sửa hoặc xoá tài khoản đã lưu
- ✅ Xác thực bằng **mật khẩu chính (Master Password)**
- ✅ Giao diện tiếng Việt đẹp mắt, đồng bộ bằng `style.css`

---

## 🗂️ Cấu trúc thư mục
📁 password_manager/
├── app.py
├── db.py
├── crypto_utils.py
├── passwords.db
├── key.key
├── templates/
│ ├── index.html
│ ├── danhsach.html
│ ├── edit.html
│ ├── xacnhan.html
│ └── login.html
├── static/
│ └── style.css
└── README.md