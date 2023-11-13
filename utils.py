import os
import torch
import torchvision.transforms as transforms
import onnxruntime as ort
import pandas as pd
from configs import *

def create_account_file():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["username","email", "password"])
        df.to_csv(USERS_FILE, index=False)

def is_authenticated(email, password):
    users_df = pd.read_csv(USERS_FILE, dtype={"password": str})
    if (email in users_df["email"].values) and (
        password == users_df.loc[users_df["email"] == email]["password"].values[0]
    ):
        username = users_df.loc[users_df["email"] == email]["username"].values[0]
        return True, username
    return False, None

def read_current_id():
    if os.path.exists(IMAGE_ID_FILE):
        with open(IMAGE_ID_FILE, "r") as file:
            return int(file.read())
    else:
        return 1

def update_current_id(new_id):
    with open(IMAGE_ID_FILE, "w") as file:
        file.write(str(new_id))

providers = ["CPUExecutionProvider", "CUDAExecutionProvider"]
onnx_session = ort.InferenceSession(MODEL_PATH, providers=providers)

transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict(image):
    image = transform(image)
    image = image.unsqueeze(0)
    onnx_input = {onnx_session.get_inputs()[0].name: image.numpy()}
    onnx_output = onnx_session.run(None, onnx_input)[0][0]
    predicted_class = torch.argmax(torch.tensor(onnx_output)).item()
    class_score = torch.softmax(torch.tensor(onnx_output), dim=0)[predicted_class].item()
    class_name = CLASSNAME[predicted_class]

    return class_name, class_score

