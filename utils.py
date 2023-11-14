import os
import torch
import torchvision.transforms as transforms
import onnxruntime as ort
import pandas as pd
from configs import *

def create_account_file():

    """
    Creates a user account file if it does not already exist.

    Checks if the specified user account file (USERS_FILE) exists. If the file does not exist,
    it creates an empty DataFrame with columns for "username," "email," and "password," and
    saves it as a CSV file.

    This function is typically called at the initialization of the application to ensure the
    existence of the user account file.

    Returns:
    - None
    """

    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["username","email", "password"])
        df.to_csv(USERS_FILE, index=False)

def is_authenticated(email, password):

    """
    Checks if the provided email and password match any user in the user account file.

    Parameters:
    - email (str): The email address provided for authentication.
    - password (str): The password provided for authentication.

    Returns:
    - Tuple[bool, Union[str, None]]: A tuple containing a boolean indicating whether the authentication is successful,
      and the username associated with the provided email if authentication is successful, or None if unsuccessful.
    """

    users_df = pd.read_csv(USERS_FILE, dtype={"password": str})
    if (email in users_df["email"].values) and (
        password == users_df.loc[users_df["email"] == email]["password"].values[0]
    ):
        username = users_df.loc[users_df["email"] == email]["username"].values[0]
        return True, username
    return False, None

def read_current_id():

    """
    Reads the current image ID from the file.

    Reads the value of the current image ID from the file specified by IMAGE_ID_FILE.
    If the file exists, the function returns the integer value of the current image ID;
    otherwise, it returns the default value of 1.

    Returns:
    - int: The current image ID.
    """

    if os.path.exists(IMAGE_ID_FILE):
        with open(IMAGE_ID_FILE, "r") as file:
            return int(file.read())
    else:
        return 1

def update_current_id(new_id):

    """
    Updates the current image ID in the file.

    Writes the provided new image ID to the file specified by IMAGE_ID_FILE.

    Parameters:
    - new_id (int): The new image ID to be written to the file.

    Returns:
    - None
    """

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

    """
    Performs coconut type prediction on the provided image using an ONNX model.

    Parameters:
    - image (PIL.Image.Image): The input image for coconut type prediction.

    Returns:
    - Tuple[str, float]: A tuple containing the predicted coconut type (class_name) and
      the confidence score associated with the prediction (class_score).
    """

    image = transform(image)
    image = image.unsqueeze(0)
    onnx_input = {onnx_session.get_inputs()[0].name: image.numpy()}
    onnx_output = onnx_session.run(None, onnx_input)[0][0]
    predicted_class = torch.argmax(torch.tensor(onnx_output)).item()
    class_score = torch.softmax(torch.tensor(onnx_output), dim=0)[predicted_class].item()
    class_name = CLASSNAME[predicted_class]

    return class_name, class_score

def reset_current_id():

    """
    Resets the current image ID if both the results folder and image folder are empty.

    Checks if the "results.txt" file in the SAMPLE_FOLDER is empty and if the "image" folder
    within the SAMPLE_FOLDER is empty. If both conditions are met, it resets the current image ID to 1.

    This function is typically used to reset the image ID when the application is in a state where
    no results are present, and the image folder is empty.

    Returns:
    - None
    """

    result_folder_empty = not os.path.exists(os.path.join(SAMPLE_FOLDER, "results.txt")) or os.stat(os.path.join(SAMPLE_FOLDER, "results.txt")).st_size == 0
    image_folder_empty = not os.listdir(os.path.join(SAMPLE_FOLDER, "image"))

    
    if result_folder_empty and image_folder_empty:
        update_current_id(1)

# Ban đầu, đọc giá trị hiện tại của current_id từ tệp và kiểm tra để reset nếu cần
current_id = read_current_id()
reset_current_id()