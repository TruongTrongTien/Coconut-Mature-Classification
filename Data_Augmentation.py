import os
import random
from torchvision import transforms
from PIL import Image

original_dua_non_path = r"C:\Users\ACER\Desktop\Coconut-Mature-Classification\dua non"

# Số lượng ảnh bạn muốn tạo
num_augmented_images = 600

# Biến đổi dữ liệu
data_augmentation = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)), 
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),  #xoay ảnh một góc độ ngẫu nhiên (0 độ) và dịch ngẫu nhiên theo chiều ngang và chiều dọc (10% chiều rộng và chiều cao ).
    transforms.RandomPerspective(distortion_scale=0.2, p=0.5), 
])

# Lấy số cuối cùng trong tên ảnh gốc
last_image_number = max([int(file.split('.')[0]) for file in os.listdir(original_dua_non_path) if file.endswith('.jpg')], default=0)
image_count = last_image_number + 1
original_images = []
for file in os.listdir(original_dua_non_path):
    if file.endswith('.jpg'):
        original_images.append(file)

# Lặp để tạo thêm ảnh mới
for i in range(num_augmented_images):
    original_image_path = os.path.join(original_dua_non_path, random.choice(original_images))
    new_image_name = f'{image_count}.jpg'
    new_image_path = os.path.join(original_dua_non_path, new_image_name)
    image = Image.open(original_image_path)
    augmented_image = data_augmentation(image)
    augmented_image = augmented_image.convert('RGB')
    augmented_image.save(new_image_path, 'JPEG')
    image_count += 1

print("Finished")