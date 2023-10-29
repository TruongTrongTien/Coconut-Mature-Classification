from flask import Flask, request, render_template
from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
import base64
import io
import torchvision.models as models

app = Flask(__name__)

# Function to load the DenseNet121 model
def load_model():
    model = models.densenet121(pretrained=False)  # Use a pre-trained model with weights
    model.classifier = nn.Linear(1024, 3)  # Modify the final fully connected layer for your classification task
    model.load_state_dict(torch.load("densenet121_model.pt", map_location=torch.device('cpu')))  # Load the model weights
    model.eval()  # Set the model to evaluation mode
    return model

# Load the model
model = load_model()

# Define a transform for image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
csv_file = "users.csv"

# Hàm kiểm tra đăng nhập
def is_authenticated(email, password):
    users_df = pd.read_csv(csv_file)
    return (email in users_df["email"].values) and (
        password == users_df.loc[users_df["email"] == email]["password"].values[0]
    )

# Function to predict coconut type
def predict_coconut_type(image, model):
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        output = model(image)
    predicted_class = torch.argmax(output).item()
    coconut_types = ['già', 'nạo', 'non']
    return coconut_types[predicted_class]
@app.route('/')
def index():
    return render_template('index.html')
@app.route("/products", methods=["GET", "POST"])
def products():
    coconut_type = None  # Khởi tạo coconut_type là None
    if request.method == "POST":
        file = request.files.get("file")
        captured_image_data = request.form.get("captured-image-data")

        if file:
            # Xử lý ảnh đã tải lên
            image = Image.open(file)
            coconut_type = predict_coconut_type(image, model)
        # Kiểm tra xem liệu có dữ liệu ảnh từ trường captured-image-data hay không
        elif captured_image_data:
            # Lấy dữ liệu ảnh từ trường captured-image-data
            image_data_uri = captured_image_data

            # Chuyển đổi dữ liệu ảnh dưới dạng URI thành đối tượng hình ảnh
            image_data = base64.b64decode(image_data_uri.split(',')[1])
            image = Image.open(io.BytesIO(image_data))

            # Thực hiện dự đoán
            coconut_type = predict_coconut_type(image, model)  # Truyền cả hai đối số

        # Nếu không có file và không có captured-image-data, gán giá trị "Không xác định"
        if coconut_type is None:
            coconut_type = "Không xác định"
    
    return render_template("products.html", coconut_type=coconut_type)
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'register' in request.form:
            # Nếu người dùng chọn đăng ký, chuyển hướng đến trang đăng ký
            return redirect(url_for('register'))

        email = request.form['email']  # Lấy email từ form
        password = request.form['password']

        users_df = pd.read_csv(csv_file)

        # Kiểm tra xem kết hợp email và mật khẩu có chính xác không
        if users_df[(users_df['email'] == email) & (users_df['password'] == password)].shape[0] > 0:
            session['email'] = email
            return redirect(url_for('index'))
        return 'Đăng nhập không thành công. <a href="/login">Thử lại</a>'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users_df = pd.read_csv(csv_file)

        # Kiểm tra xem email đã tồn tại chưa
        if email in users_df["email"].values:
            return 'Email đã tồn tại. <a href="/register">Thử lại</a>'

        # Thêm người dùng mới vào tệp CSV
        new_user = pd.DataFrame({"username": [username],"email": [email], "password": [password]})
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(csv_file, index=False)
        return 'Đăng ký thành công! <a href="/login">Đăng nhập</a>'
    return render_template('login.html')


if __name__ == "__main__":
    app.run()
