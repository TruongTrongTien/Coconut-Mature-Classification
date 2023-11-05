from flask import Flask, request, render_template, redirect, url_for, session
from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
import base64
import io
import torchvision.models as models
import pandas as pd
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to load the DenseNet121 model
# Function to load the DenseNet121 model
def load_mobilenet_model(model_path):
    model = models.mobilenet_v2(pretrained=False)  # Tạo mô hình MobileNetV2 không được huấn luyện trước
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, 3)  # Thay đổi lớp fully connected cuối cùng cho bài toán phân loại 3 lớp
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))  # Nạp trọng số từ tệp model_path
    model.eval()  # Đặt mô hình ở chế độ đánh giá
    return model

model = load_mobilenet_model("MobileNet_v2_model.pt")


# Define a transform for image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
csv_file = "users.csv"
users_df = pd.read_csv(csv_file, dtype={"password": str})
# Kiểm tra xem tệp CSV có tồn tại không
if not os.path.exists(csv_file):
    # Nếu không tồn tại, tạo một tệp trống
    df = pd.DataFrame(columns=["username","email", "password"])
    df.to_csv(csv_file, index=False)
    
# Hàm kiểm tra đăng nhập
def is_authenticated(email, password):
    users_df = pd.read_csv(csv_file, dtype={"password": str})
    if (email in users_df["email"].values) and (
        password == users_df.loc[users_df["email"] == email]["password"].values[0]
    ):
        username = users_df.loc[users_df["email"] == email]["username"].values[0]
        return True, username
    return False, None

# Function to predict coconut type
def predict_coconut_type(image, model):
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        output = model(image)
    predicted_class = torch.argmax(output).item()
    coconut_types = ['Dừa già', 'Dừa nạo', 'Dừa non']
    return coconut_types[predicted_class]
@app.route('/')
def index():
    return render_template('index.html')
# Đường dẫn đến thư mục predict
predict_folder = "predict"

# Hàm để đọc giá trị hiện tại của current_id từ tệp
def read_current_id():
    if os.path.exists("current_id.txt"):
        with open("current_id.txt", "r") as file:
            return int(file.read())
    else:
        return 1

# Hàm để cập nhật và lưu giá trị current_id vào tệp
def update_current_id(new_id):
    with open("current_id.txt", "w") as file:
        file.write(str(new_id))

# Ban đầu, đọc giá trị hiện tại của current_id từ tệp
current_id = read_current_id()

@app.route("/products", methods=["GET", "POST"])
def products():
    if 'email' in session:
        global current_id  # Sử dụng biến global để theo dõi ID hiện tại

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
                result_filename = os.path.join(predict_folder, "results.txt")
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
                image_data = base64.b64decode(image_data_uri.split(',')[1])
                image = Image.open(io.BytesIO(image_data))

                # Thực hiện dự đoán
                coconut_type = predict_coconut_type(image, model)

                # Tạo tên tệp ảnh dựa trên ID và lưu ảnh vào thư mục predict
                image_filename = os.path.join("predict\\image", f"{current_id}.jpg")
                image.save(image_filename)

                # Tạo tên tệp txt chung để lưu kết quả dự đoán
                result_filename = os.path.join(predict_folder, "results.txt")
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
        return redirect(url_for('login'))

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    mess = ''  # Khởi tạo thông báo là chuỗi trống

    if request.method == 'POST':
        if 'register' in request.form:
            # Nếu người dùng chọn đăng ký, chuyển hướng đến trang đăng ký
            return redirect(url_for('register'))

        email = request.form['email']  # Lấy email từ form
        password = request.form['password']
        authenticated, username = is_authenticated(email, password)

        if authenticated:
            session['email'] = email
            session['username'] = username  # Set the username in the session
            return redirect(url_for('products'))
        else:
            mess = 'Đăng nhập không thành công. Thử lại.'  # Đặt thông báo không thành công

    return render_template('login.html', mess=mess)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    success = False  # Thêm biến để chỉ định thành công

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users_df = pd.read_csv(csv_file, dtype={"password": str})

        if email in users_df["email"].values:
            message = 'Email đã tồn tại. Thử lại.'
        else:
            new_user = pd.DataFrame({"username": [username], "email": [email], "password": [password]})
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv(csv_file, index=False)
            message = 'Đăng ký thành công!'
            success = True

    return render_template('login.html', message=message, success=success,isRegisterShown=True)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True) 
