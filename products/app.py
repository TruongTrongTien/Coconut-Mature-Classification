from flask import Flask, request, render_template
from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
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

# Function to predict coconut type
def predict_coconut_type(image, model):
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        output = model(image)
    predicted_class = torch.argmax(output).item()
    coconut_types = ['già', 'nạo', 'non']
    return coconut_types[predicted_class]

@app.route("/", methods=["GET", "POST"])
def index():
    coconut_type = None  # Khởi tạo coconut_type là None
    if request.method == "POST":
        if "predict" in request.form:  # Kiểm tra xem yêu cầu POST có xuất phát từ nút "Dự đoán" hay không
            if "file" not in request.files:
                return "Không có phần tệp nào được chọn"
            file = request.files["file"]
            if file.filename == "":
                return "Không có tệp nào được chọn"
            if file:
                # Xử lý ảnh đã tải lên
                image = Image.open(file)
                coconut_type = predict_coconut_type(image, model)
    return render_template("products.html", coconut_type=coconut_type)



if __name__ == "__main__":
    app.run()
