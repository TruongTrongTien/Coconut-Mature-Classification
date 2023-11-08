import os
import shutil
import random

data_dir = r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\dua nao'

train_dir = r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\train\dua nao'
val_dir = r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\val\dua nao'
test_dir = r'C:\Users\ACER\Desktop\Coconut-Mature-Classification\test\dua nao'

# Tạo thư mục nếu chưa tồn tại
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
image_files = os.listdir(data_dir) # Lấy danh sách tất cả các tệp hình ảnh trong thư mục dữ liệu
# Xáo trộn danh sách
random.shuffle(image_files)

# Tính số lượng tệp cho mỗi phần
total_images = len(image_files)
train_split = int(0.8 * total_images)
val_split = int(0.1 * total_images)

# Chia tệp 
train_files = image_files[:train_split]
val_files = image_files[train_split:train_split + val_split]
test_files = image_files[train_split + val_split:]

# Di chuyển vào mục tương ướng
for file in train_files:
     src = os.path.join(data_dir, file)
     dst = os.path.join(train_dir, file)
     shutil.copy(src, dst)

for file in val_files:
     src = os.path.join(data_dir, file)
     dst = os.path.join(val_dir, file)
     shutil.copy(src, dst)

for file in test_files:
     src = os.path.join(data_dir, file)
     dst = os.path.join(test_dir, file)
     shutil.copy(src, dst)

print("Finished")