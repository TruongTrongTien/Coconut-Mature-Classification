import torch
import torchvision.transforms as transforms
import onnxruntime as ort
from configs import *


providers = ["CPUExecutionProvider", "CUDAExecutionProvider"]
onnx_session = ort.InferenceSession("model.onnx", providers=providers)

transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict(image):
    image = transforms(image).unsqueeze(0)
    onnx_input = {onnx_session.get_inputs()[0].name: image.numpy()}
    onnx_output = onnx_session.run(None, onnx_input)[0]
    predicted_class = torch.argmax(torch.tensor(onnx_output)).item()
    class_score = torch.softmax(torch.tensor(onnx_output), dim=0)[predicted_class].item()
    class_name = CLASSNAME[predicted_class] if class_score >= THRESHOLD else "Không xác định"

    return class_name, class_score

users_df = pd.read_csv(CSV_FILE, dtype={"password": str})