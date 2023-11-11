from flask import Flask, request, render_template, redirect, url_for, session

import os
import base64
import io
from PIL import Image
import pandas as pd
from utils import *
from configs import *


app = Flask(__name__)
app.secret_key = "your_secret_key"



# Kiểm tra xem tệp CSV có tồn tại không
if not os.path.exists(CSV_FILE):
    # Nếu không tồn tại, tạo một tệp trống
    df = pd.DataFrame(columns=["username","email", "password"])
    df.to_csv(CSV_FILE, index=False)
    
# Hàm kiểm tra đăng nhập
def is_authenticated(email, password):
    users_df = pd.read_csv(CSV_FILE, dtype={"password": str})
    if (email in users_df["email"].values) and (
        password == users_df.loc[users_df["email"] == email]["password"].values[0]
    ):
        username = users_df.loc[users_df["email"] == email]["username"].values[0]
        return True, username
    return False, None


  
@app.route("/")
def index():
    return render_template("index.html")

def read_current_id():
    if os.path.exists("current_id.txt"):
        with open("current_id.txt", "r") as file:
            return int(file.read())
    else:
        return 1

def update_current_id(new_id):
    with open("current_id.txt", "w") as file:
        file.write(str(new_id))

current_id = read_current_id()



@app.route("/products", methods=["GET", "POST"])
def products():
    if "email" in session:
        global current_id

        coconut_type = None
        captured_image_data = None

        if request.method == "POST":
            file = request.files.get("file")
            captured_image_data = request.form.get("captured-image-data")

            if file:
                # Xử lý ảnh đã tải lên
                image = Image.open(file)
                coconut_type = predict_coconut_type(image, model)

                # Tạo tên tệp ảnh dựa trên ID và lưu ảnh vào thư mục predict
                image_filename = os.path.join("predict\\image", f"{current_id}.jpg")
                image.save(image_filename)

                # Tạo tên tệp txt chung để lưu kết quả dự đoán
                result_filename = os.path.join(SAMPLE_FOLDER, "results.txt")
                with open(result_filename, "a", encoding="utf-8") as result_file:
                    result_file.write(f"ID: {current_id}, Coconut Type: {coconut_type}\n")

                # Tăng ID lên để sử dụng cho lần tải lên tiếp theo
                current_id += 1

                # Cập nhật giá trị mới của current_id vào tệp
                update_current_id(current_id)
            elif captured_image_data:
                # Lấy dữ liệu ảnh từ trường captured-image-data
                image_data_uri = captured_image_data

                # Chuyển đổi dữ liệu ảnh dưới dạng URI thành đối tượng hình ảnh
                image_data = base64.b64decode(image_data_uri.split(",")[1])
                image = Image.open(io.BytesIO(image_data))

                # Thực hiện dự đoán
                coconut_type = predict_coconut_type(image, model)

                # Tạo tên tệp ảnh dựa trên ID và lưu ảnh vào thư mục predict
                image_filename = os.path.join("predict\\image", f"{current_id}.jpg")
                image.save(image_filename)

                # Tạo tên tệp txt chung để lưu kết quả dự đoán
                result_filename = os.path.join(SAMPLE_FOLDER, "results.txt")
                with open(result_filename, "a", encoding="utf-8") as result_file:
                    result_file.write(f"ID: {current_id}, Coconut Type: {coconut_type}\n")

                # Tăng ID lên để sử dụng cho lần tải lên tiếp theo
                current_id += 1

                # Cập nhật giá trị mới của current_id vào tệp
                update_current_id(current_id)

            # Nếu không có file và không có captured-image-data, gán giá trị "Không xác định"
            if coconut_type is None:
                coconut_type = "Không xác định"
        return render_template("products.html", captured_image_data=captured_image_data, coconut_type=coconut_type)
    else:
        return redirect(url_for("login"))
    


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    mess = ""  # Khởi tạo thông báo là chuỗi trống

    if request.method == "POST":
        if "register" in request.form:
            # Nếu người dùng chọn đăng ký, chuyển hướng đến trang đăng ký
            return redirect(url_for("register"))

        email = request.form["email"]  # Lấy email từ form
        password = request.form["password"]
        authenticated, username = is_authenticated(email, password)

        if authenticated:
            session["email"] = email
            session["username"] = username  # Set the username in the session
            return redirect(url_for("products"))
        else:
            mess = "Đăng nhập không thành công. Thử lại."  # Đặt thông báo không thành công

    return render_template("login.html", mess=mess)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    success = False  # Thêm biến để chỉ định thành công

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        users_df = pd.read_csv(CSV_FILE, dtype={"password": str})

        if email in users_df["email"].values:
            message = "Email đã tồn tại. Thử lại."
        else:
            new_user = pd.DataFrame({"username": [username], "email": [email], "password": [password]})
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv(CSV_FILE, index=False)
            message = "Đăng ký thành công!"
            success = True

    return render_template("login.html", message=message, success=success,isRegisterShown=True)



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True) 
