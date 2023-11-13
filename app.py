from flask import Flask, request, render_template, redirect, url_for, session

import os
import base64
import io
from PIL import Image
from utils import *
from configs import *

app = Flask(__name__)
app.secret_key = "your_secret_key"
 
@app.route("/")
def index():
    return render_template("index.html")

current_id = read_current_id()

@app.route("/products", methods=["GET", "POST"])
def products():
    if "email" in session:
        global current_id

        class_name = None
        class_score = 0
        captured_image_data = None

        if request.method == "POST":
            file = request.files.get("file")
            captured_image_data = request.form.get("captured-image-data")

            if file:
                # Xử lý ảnh đã tải lên
                image = Image.open(file)
                class_name, class_score = predict(image)

                # Tạo tên tệp ảnh dựa trên ID và lưu ảnh vào thư mục predict
                image_filename = os.path.join(SAMPLE_FOLDER, "image", f"{current_id}.jpg")
                image.save(image_filename)

                # Tạo tên tệp txt chung để lưu kết quả dự đoán
                result_filename = os.path.join(SAMPLE_FOLDER, "results.txt")
                with open(result_filename, "a", encoding="utf-8") as result_file:
                    result_file.write(f"ID: {current_id}, Coconut Type: {class_name}\n")

                # Tăng ID lên để sử dụng cho lần tải lên tiếp theo
                current_id += 1

                # Cập nhật giá trị mới của current_id vào tệp
                update_current_id(current_id)
            elif captured_image_data:
                # Lấy dữ liệu ảnh từ trường captured-image-data
                image_data_uri = captured_image_data

                # Chuyển đổi dữ liệu ảnh dưới dạng URI thành đối tượng hình ảnh
                image_data = base64.b64decode(image_data_uri.split(",")[1])
                file = io.BytesIO(image_data)
                image = Image.open(file)

                # Thực hiện dự đoán
                class_name, class_score = predict(image)

                # Tạo tên tệp ảnh dựa trên ID và lưu ảnh vào thư mục predict
                image_filename = os.path.join(SAMPLE_FOLDER, "image", f"{current_id}.jpg")
                image.save(image_filename)

                # Tạo tên tệp txt chung để lưu kết quả dự đoán
                result_filename = os.path.join(SAMPLE_FOLDER, "results.txt")
                with open(result_filename, "a", encoding="utf-8") as result_file:
                    result_file.write(f"ID: {current_id}, Coconut Type: {class_name}\n")

                # Tăng ID lên để sử dụng cho lần tải lên tiếp theo
                current_id += 1

                # Cập nhật giá trị mới của current_id vào tệp
                update_current_id(current_id)

            if class_name is None:
                class_name = "Không xác định"
        return render_template("products.html", captured_image_data=captured_image_data, class_name=class_name, class_score=class_score)
    else:
        return redirect(url_for("login"))
    

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    mess = ""

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
            mess = "Đăng nhập không thành công. Thử lại."

    return render_template("login.html", mess=mess)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    success = False

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        users_df = pd.read_csv(USERS_FILE, dtype={"password": str})

        if email in users_df["email"].values:
            message = "Email đã tồn tại. Thử lại."
        else:
            new_user = pd.DataFrame({"username": [username], "email": [email], "password": [password]})
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv(USERS_FILE, index=False)
            message = "Đăng ký thành công!"
            success = True

    return render_template("login.html", message=message, success=success,isRegisterShown=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
