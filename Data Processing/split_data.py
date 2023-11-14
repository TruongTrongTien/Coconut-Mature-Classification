"""
split_data

This module splits the data into training, validation, and test sets.
"""

import os
import shutil
import random

# Đường dẫn đến thư mục chứa ảnh gốc
DATA_DIR = "" #Add your original data directory.

TRAIN_DIR = "" #Add your train data directory
VAL_DIR = "" #Add your val data directory
TEST_DIR = "" #Add your test data directory

# Create directory if it doesn't exist
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

# Get a list of all image files in the data directory
IMAGE_FILES = os.listdir(DATA_DIR)

# Shuffle the list
random.shuffle(IMAGE_FILES)

# Calculate the number of files for each section
TRAIN_RATE = "" # add scale for train dataset. Example: 0.8
VAL_RATE = "" # add scale for val dataset. Example: 0.8
TOTAL_IMAGES = len(IMAGE_FILES)
TRAIN_SPLIT = int(TRAIN_RATE * TOTAL_IMAGES)
VAL_SPLIT = int(VAL_RATE * TOTAL_IMAGES)

# Split files
TRAIN_FILES = IMAGE_FILES[:TRAIN_SPLIT]
VAL_FILES = IMAGE_FILES[TRAIN_SPLIT:TRAIN_SPLIT + VAL_SPLIT]
TEST_FILES = IMAGE_FILES[TRAIN_SPLIT + VAL_SPLIT:]

# Move to the corresponding item
for file in TRAIN_FILES:
    src = os.path.join(DATA_DIR, file)
    dst = os.path.join(TRAIN_DIR, file)
    shutil.copy(src, dst)

for file in VAL_FILES:
    src = os.path.join(DATA_DIR, file)
    dst = os.path.join(VAL_DIR, file)
    shutil.copy(src, dst)

for file in TEST_FILES:
    src = os.path.join(DATA_DIR, file)
    dst = os.path.join(TEST_DIR, file)
    shutil.copy(src, dst)

print("Finished")
