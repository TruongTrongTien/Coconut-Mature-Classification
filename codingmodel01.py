# -*- coding: utf-8 -*-
"""CodingModel01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EBOa9ts5seHV8o7TWyEb_Zf7Jwq21Bgs
"""

## Connect to gg drive
from google.colab import drive
drive.mount('/content/drive')

pwd

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/Coconut-Mature-Classification-Final

"""## 1. EDA and Data Preprocessing"""

# import os
# import shutil
# import random

# # Đường dẫn đến thư mục chứa dữ liệu hình ảnh
# data_dir = '/content/drive/.shortcut-targets-by-id/1HvKsQz_kawTxU0oxq_tOAwR0xJkB5XMs/dataset/mature_processed'

# # Đường dẫn đến thư mục chứa tập dữ liệu huấn luyện, kiểm tra và kiểm định
# train_dir = '/content/drive/MyDrive/ColabNotebooks/coconut_project/train/mature'
# val_dir = '/content/drive/MyDrive/ColabNotebooks/coconut_project/val/mature'
# test_dir = '/content/drive/MyDrive/ColabNotebooks/coconut_project/test/mature'

# # Tạo thư mục nếu chưa tồn tại
# os.makedirs(train_dir, exist_ok=True)
# os.makedirs(val_dir, exist_ok=True)
# os.makedirs(test_dir, exist_ok=True)

# # Lấy danh sách tất cả các tệp hình ảnh trong thư mục dữ liệu
# image_files = os.listdir(data_dir)

# # Xáo trộn danh sách tệp hình ảnh
# random.shuffle(image_files)

# # Tính số lượng tệp cho mỗi phần
# total_images = len(image_files)
# train_split = int(0.8 * total_images)
# val_split = int(0.1 * total_images)

# # Chia tệp hình ảnh thành các phần
# train_files = image_files[:train_split]
# val_files = image_files[train_split:train_split + val_split]
# test_files = image_files[train_split + val_split:]

# # Di chuyển các tệp hình ảnh vào các thư mục tương ứng
# for file in train_files:
#     src = os.path.join(data_dir, file)
#     dst = os.path.join(train_dir, file)
#     shutil.copy(src, dst)

# for file in val_files:
#     src = os.path.join(data_dir, file)
#     dst = os.path.join(val_dir, file)
#     shutil.copy(src, dst)

# for file in test_files:
#     src = os.path.join(data_dir, file)
#     dst = os.path.join(test_dir, file)
#     shutil.copy(src, dst)

# print("Finished")

import os
import plotly.express as px

base_folder = '/content/drive/MyDrive/Coconut-Mature-Classification-Final'
data_sets = ['train', 'test', 'val']
data = {'Set': [], 'Class': [], 'Number of images': []}

for data_set in data_sets:
    dataset_folder = os.path.join(base_folder, data_set)

    for class_folder in os.listdir(dataset_folder):
        class_path = os.path.join(dataset_folder, class_folder)
        if os.path.isdir(class_path):
            data['Set'].append(data_set)
            data['Class'].append(class_folder)
            data['Number of images'].append(len(os.listdir(class_path)))

fig = px.bar(data, x='Class', y='Number of images', color='Set',
             title='Class distribution')
fig.show()

import torch
import torchvision
from torchvision import transforms
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import torch.optim as optim
from glob import glob
from tqdm import tqdm
import random
from torch.utils.data import DataLoader

# import imgaug.augmenters as iaa
# import cv2

# # Define the augmentation pipeline
# augmentation = iaa.Sequential([
#     iaa.Fliplr(0.5),
#     iaa.Affine(rotate=(-20, 20), mode='reflect')
# ])

# # Define input and output directories
# input_dir = '/content/drive/MyDrive/ColabNotebooks/coconut_project/train/young'
# output_dir = '/content/drive/MyDrive/ColabNotebooks/coconut_project/train/young_augmented'

# # Create the output directory if it doesn't exist
# os.makedirs(output_dir, exist_ok=True)

# # List all image files in the input directory
# image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

# # Perform data augmentation for each image in the input directory
# for filename in image_files:
#     # Load an image
#     image = cv2.imread(os.path.join(input_dir, filename))
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB format

#     # Create an empty list to store augmented images
#     augmented_images = []

#     # Perform data augmentation and generate 4 different augmentations for each image
#     for _ in range(4):
#         augmented_image = augmentation.augment_image(image)
#         augmented_images.append(augmented_image)

#     # Save augmented images to the output directory
#     for i, augmented_image in enumerate(augmented_images):
#         output_filename = f'augmented_{i}_{filename}'
#         output_path = os.path.join(output_dir, output_filename)
#         augmented_image_bgr = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)
#         cv2.imwrite(output_path, augmented_image_bgr)

# print("Augmentation complete.")

folder_path = '/content/drive/MyDrive/Coconut-Mature-Classification-Final/train/dua non'
files = os.listdir(folder_path)
num_files = len(files)
print(f"Number of files in the folder: {num_files}")

# source_folder = '/content/drive/MyDrive/ColabNotebooks/coconut_project/train/young_augmented'
# destination_folder = '/content/drive/MyDrive/ColabNotebooks/coconut_project/train/young'

# # Get a list of all files in the source folder
# files = os.listdir(source_folder)

# # Loop through the files and move each one to the destination folder
# for file in files:
#     source_file = os.path.join(source_folder, file)
#     destination_file = os.path.join(destination_folder, file)
#     shutil.move(source_file, destination_file)

train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


train_data = torchvision.datasets.ImageFolder(root='/content/drive/MyDrive/Coconut-Mature-Classification-Final/train', transform=train_transforms)
val_data = torchvision.datasets.ImageFolder(root='/content/drive/MyDrive/Coconut-Mature-Classification-Final/val', transform=val_transforms)

num_classes = len(train_data.classes)
classes_name = train_data.classes
classes2idx = train_data.class_to_idx

print(f"Number of classes: {num_classes}")
print(f"Classes names: {classes_name}")
print(f"Labels mapping: {classes2idx}")
print("Number of train: ", len(train_data))
print("Number of val: ", len(val_data))

all_class = glob("/content/drive/MyDrive/Coconut-Mature-Classification-Final/train/*")
train_class_counts =  {}
for folder_class in tqdm(all_class, desc='run'):
    name = folder_class.split('/')[-1]
    train_class_counts[name] = len(glob(f"{folder_class}/*"))
train_class_counts = dict(sorted(train_class_counts.items(), key=lambda item: item[0]))

plt.figure(figsize=(10, 5))
plt.bar(list(train_class_counts.keys()), list(train_class_counts.values()))
plt.title('Train set distribution')
plt.xlabel('Class')
plt.ylabel('#')
plt.xticks(rotation=45)
plt.show()

all_class = glob("/content/drive/MyDrive/Coconut-Mature-Classification-Final/test/*")
train_class_counts =  {}
for folder_class in tqdm(all_class, desc='run'):
    name = folder_class.split('/')[-1]
    train_class_counts[name] = len(glob(f"{folder_class}/*"))
train_class_counts = dict(sorted(train_class_counts.items(), key=lambda item: item[0]))

plt.figure(figsize=(10, 5))
plt.bar(list(train_class_counts.keys()), list(train_class_counts.values()))
plt.title('Val set distribution')
plt.xlabel('Class')
plt.ylabel('#')
plt.xticks(rotation=45)
plt.show()

"""## 2. Modeling"""

import torch
import torch.nn as nn
import torchvision.models as models
from sklearn.metrics import confusion_matrix, f1_score, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import copy

import torch.nn as nn
import torchvision.models as models

# Load Densenet-121 model
model = models.densenet121(pretrained=True)  # Sử dụng pretrained weights hoặc pretrained=False nếu không muốn

num_classes = 3
model.classifier = nn.Linear(model.classifier.in_features, num_classes)

for param in model.features.parameters():
    param.requires_grad = False

random_image = torch.rand(1, 3, 224, 224)
model(random_image).shape

print("# Parameters", sum(p.numel() for p in model.parameters()))

"""## 3. Training model"""

import torch.optim as optim
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EPOCHS = 30
BATCH_SIZE = 64

# Create data loaders
TRAINLOADER = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
TESTLOADER = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)
DEVICE

model.to(DEVICE)

!pip install lion-pytorch
from lion_pytorch import Lion

# Loss
criterion = nn.CrossEntropyLoss()
# Optimizer and Scheduler
optimizer = Lion(model.parameters(), lr=1e-4, weight_decay=1e-2)

# Define a filename for saving the model
model_save_path = 'densenet121_model.pt'

# Define early stopping parameters
patience = 5
best_validation_loss = float('inf')
no_improvement_count = 0

loss_train = []
loss_test = []
f1_train = []
f1_test = []

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    predictions_train = []
    true_labels_train = []

    for i, data in tqdm(enumerate(TRAINLOADER), desc='train'):
        inputs, labels = data
        inputs = inputs.to(DEVICE)
        labels = labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        predictions_train.extend(predicted.tolist())
        true_labels_train.extend(labels.tolist())

    train_loss = running_loss / len(TRAINLOADER)
    train_f1 = f1_score(true_labels_train, predictions_train, average='weighted')

    loss_train.append(train_loss)
    f1_train.append(train_f1)

    model.eval()
    test_loss_val = 0.0
    predictions = []
    true_labels = []

    with torch.no_grad():
        for data in TESTLOADER:
            # Validation steps as in your code
            inputs, labels = data
            inputs = inputs.to(DEVICE)
            labels = labels.to(DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            test_loss_val += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            predictions.extend(predicted.tolist())
            true_labels.extend(labels.tolist())

    test_loss_val /= len(TESTLOADER)
    test_f1_val = f1_score(true_labels, predictions, average='weighted')

    loss_test.append(test_loss_val)
    f1_test.append(test_f1_val)
    print(f'Epoch [{epoch + 1}/{EPOCHS}]  - Train Loss: {train_loss:.4f} - Train F1: {train_f1:.4f} - Test Loss: {test_loss_val:.4f} - Test F1: {test_f1_val:.4f}')

    # Check if validation loss has improved
    if test_loss_val < best_validation_loss:
        best_validation_loss = test_loss_val
        no_improvement_count = 0

        # Save the model when validation loss improves
        torch.save(model.state_dict(), model_save_path)
    else:
        no_improvement_count += 1

    # If no improvement for 'early_stopping_patience' epochs, stop training
    if no_improvement_count >= patience:
        print(f'Early stopping after {epoch + 1} epochs due to no improvement in validation loss.')
        break

print('Finished Training')

# Plotting the metrics
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(loss_train, label='Train Loss')
plt.plot(loss_test, label='Val Loss')
plt.title('Loss over epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(f1_train, label='Train F1 Score')
plt.plot(f1_test, label='Val F1 Score')
plt.title('F1 Score over epochs')
plt.xlabel('Epochs')
plt.ylabel('F1 Score')
plt.legend()

plt.tight_layout()
plt.show()

"""## 4. Evaluating"""

model = models.densenet121(num_classes=3)
model.load_state_dict(torch.load("/content/drive/MyDrive/Coconut-Mature-Classification-Final/densenet121_model.pt"))

model.to(DEVICE)
model.eval()
all_predictions = []
all_true_labels = []

with torch.no_grad():
    for data in TESTLOADER:
        inputs, labels = data
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        all_predictions.extend(predicted.cpu().tolist())
        all_true_labels.extend(labels.cpu().tolist())


# Compute confusion matrix
cm = confusion_matrix(all_true_labels, all_predictions)

# Plot confusion matrix using Seaborn
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes_name, yticklabels=classes_name)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

f1 = f1_score(all_true_labels, all_predictions, average='weighted')
print("Weighted F1 Score:", f1)

print(classification_report(all_true_labels, all_predictions, target_names=classes_name))

"""##5. Inference"""

from PIL import Image

model = models.densenet121(num_classes=3)
model.load_state_dict(torch.load("/content/drive/MyDrive/Coconut-Mature-Classification-Final/densenet121_model.pt"))
model.eval()

# Load your image and preprocess it
image_path = '/content/drive/MyDrive/Coconut-Mature-Classification-Final/test/dua nao/1049.jpg'
image = Image.open(image_path)
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
input_data = preprocess(image).unsqueeze(0)  # Add a batch dimension

# Perform inference
with torch.no_grad():
    output = model(input_data)

# Post-process the output to get class probabilities
probabilities = torch.softmax(output, dim=1)

# Get the predicted class (class with the highest probability)
predicted_class = torch.argmax(probabilities, dim=1)

# Print or use the predicted class
print("Predicted Class:", predicted_class.item())

import matplotlib.pyplot as plt

# Define a list of class names in the order they correspond to the model's output
class_names = ["dừa già", "dừa nạo", "dừa non"]

# Load your image and preprocess it
image_path = '/content/drive/MyDrive/Coconut-Mature-Classification-Final/test/dua gia/205.jpg'
image = Image.open(image_path)
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
input_data = preprocess(image).unsqueeze(0)  # Add a batch dimension

# Perform inference
with torch.no_grad():
    output = model(input_data)

# Post-process the output to get class probabilities
probabilities = torch.softmax(output, dim=1)

# Get the predicted class (class with the highest probability)
predicted_class = torch.argmax(probabilities, dim=1)

# Use the predicted class to get the class name
predicted_class_index = predicted_class.item()
predicted_class_name = class_names[predicted_class_index]

# Display the image with the predicted class name
plt.imshow(image)
plt.title("Predicted Class: " + predicted_class_name)
plt.axis('off')  # Turn off axis labels and ticks
plt.show()